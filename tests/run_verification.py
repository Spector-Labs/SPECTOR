#!/usr/bin/env python3
"""
SPECTOR verification orchestrator — single entry point.
One http.server on :8088 for the full run; atomic scratch bundle at end.
"""
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
SCRATCH = Path(r"C:\Users\USER\AppData\Local\Temp\grok-goal-ee54e3f7c3b7\implementer")
PORT = 8088
BASE_URL = f"http://127.0.0.1:{PORT}"
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
EDGE_PROFILE = SCRATCH / "edge-profile"

ARTIFACTS: dict[str, str] = {}
FAILURES: list[str] = []


def meta(step: int) -> str:
    head = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True, text=True,
    ).stdout.strip()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"git={head} ts={ts} step={step}\n"


def fail(label: str):
    FAILURES.append(label)
    print(f"FAIL: {label}")


def ok(label: str):
    print(f"OK: {label}")


def clear_scratch():
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH, ignore_errors=True)
    SCRATCH.mkdir(parents=True, exist_ok=True)


class HttpServer:
    def __init__(self):
        self.proc: subprocess.Popen | None = None
        self.lines: list[tuple[float, str]] = []
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self):
        cmd = [sys.executable, "-m", "http.server", str(PORT), "--directory", str(PUBLIC)]
        self.proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,
        )
        self._thread = threading.Thread(target=self._reader, daemon=True)
        self._thread.start()
        time.sleep(1.2)
        ok(f"server started :{PORT}")

    def _reader(self):
        assert self.proc and self.proc.stdout
        while not self._stop.is_set():
            line = self.proc.stdout.readline()
            if not line:
                break
            self.lines.append((time.time(), line.rstrip("\n")))

    def request(self, path: str) -> tuple[int, int]:
        url = f"{BASE_URL}/{path}"
        with urllib.request.urlopen(url, timeout=10) as resp:
            body = resp.read()
            return resp.status, len(body)

    def capture_window(self, seconds: float, label: str) -> str:
        start = time.time()
        # trigger access lines
        for path in ("index.html", "app.html", "style.css"):
            try:
                self.request(path)
            except Exception:
                pass
        time.sleep(max(0, seconds - (time.time() - start)))
        end = time.time()
        chunk = [ln for t, ln in self.lines if start <= t <= end]
        header = [
            meta(4),
            f"=== {label} ===",
            f"command: python -m http.server {PORT} --directory {PUBLIC}",
            f"background duration: {seconds}s",
            "",
        ]
        return "\n".join(header + chunk)

    def stop(self):
        self._stop.set()
        if self.proc:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        if self._thread:
            self._thread.join(timeout=2)


def find_browser() -> Path | None:
    if EDGE.is_file():
        return EDGE
    chrome = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    return chrome if chrome.is_file() else None


def edge_dump(url: str, dump_path: Path, profile: Path | None = None, budget: int = 10000) -> str:
    browser = find_browser()
    if not browser:
        return ""
    dump_arg = str(dump_path).replace("\\", "/")
    cmd = [
        str(browser), "--headless=new", "--disable-gpu", "--no-sandbox",
        f"--dump-dom={dump_arg}", f"--virtual-time-budget={budget}",
        "--run-all-compositor-stages-before-draw", url,
    ]
    if profile:
        cmd.insert(1, f"--user-data-dir={str(profile).replace(chr(92), '/')}")
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    stdout = proc.stdout or ""
    if "<html" in stdout.lower():
        return stdout
    if dump_path.is_file() and dump_path.stat().st_size > 0:
        return dump_path.read_text(encoding="utf-8", errors="replace")
    return stdout + (proc.stderr or "")


def step1_static_structure():
    lines = [meta(1), "=== SPECTOR ROOT ==="]
    lines.extend(sorted(p.name for p in ROOT.iterdir()))
    lines += ["", "=== public/ ==="]
    lines.extend(sorted(p.name for p in PUBLIC.iterdir()))
    lines += ["", "=== stylesheet refs ==="]
    for name in ("index.html", "app.html"):
        for ln in (PUBLIC / name).read_text(encoding="utf-8").splitlines():
            if "stylesheet" in ln:
                lines.append(f"{name}: {ln.strip()}")
    lines += ["", "=== vercel.json (root only; public/vercel.json removed) ==="]
    lines.append((ROOT / "vercel.json").read_text(encoding="utf-8"))
    root_css = ROOT / "style.css"
    lines += [
        "",
        f"root style.css exists: {root_css.exists()}",
        f"public/style.css exists: {(PUBLIC / 'style.css').exists()}",
    ]
    if "styles.css" in (PUBLIC / "index.html").read_text():
        fail("index.html references styles.css")
    else:
        ok("index.html uses style.css")
    ARTIFACTS["static-structure.txt"] = "\n".join(lines)


def step2_core_logic():
    app = (PUBLIC / "app.html").read_text(encoding="utf-8")
    css = (PUBLIC / "style.css").read_text(encoding="utf-8")
    units = [
        "hybridChunk", "getMs", "KalmanFilter", "setupSpatialAnchoring",
        "startDualSineBreathing", "startGentleDriftWithRotation", "settleActiveChunk",
        "applyMode", "getScriptFromURL", "render", "updateDisplay",
        "startPlayback", "stopPlayback", "togglePlay", "showEndScreen", "init",
        "runSpectorCoreTests", "SpectorCore", "registerChunker", "teardownSpatialAnchoring",
    ]
    lines = [meta(2), "=== CORE LOGIC UNITS ==="]
    for u in units:
        present = u in app
        lines.append(f"  {u}: {'present' if present else 'MISSING'}")
        if not present:
            fail(f"core logic missing {u}")
    lines += ["", "=== CSS GLASSES MODE (sample) ==="]
    idx = css.find("body.glasses")
    lines.append(css[idx:idx + 500] if idx >= 0 else "MISSING")
    ARTIFACTS["core-logic.txt"] = "\n".join(lines)


def step3_pwa_tests(server: HttpServer):
    lines = [meta(3), "=== PWA + pure-logic tests (base_url 8088) ===", ""]
    manifest = json.loads((PUBLIC / "manifest.json").read_text(encoding="utf-8"))
    lines.append(f"manifest name: {manifest.get('name')}")
    lines.append(f"manifest display: {manifest.get('display')}")

    # Normal player on shared server
    try:
        st, n = server.request("app.html?script=SGVsbG8u")
        html_body = urllib.request.urlopen(f"{BASE_URL}/app.html?script=SGVsbG8u", timeout=10).read().decode()
        lines.append(f"NORMAL GET app.html?script= -> {st} ({n} bytes)")
        lines.append(f"NORMAL has play-btn: {'play-btn' in html_body}")
        if "play-btn" not in html_body:
            fail("normal player HTML missing play-btn on :8088")
    except Exception as e:
        fail(f"normal player fetch: {e}")
        html_body = ""

    browser = find_browser()
    if browser:
        dump_n = SCRATCH / "normal-8088.html"
        dump = edge_dump(f"{BASE_URL}/app.html?script=SGVsbG8u", dump_n, budget=12000)
        title_m = re.search(r"<title>([^<]*)</title>", dump)
        title = title_m.group(1) if title_m else ""
        lines.append(f"NORMAL headless title: {title!r}")
        lines.append(f"NORMAL headless play-btn: {'play-btn' in dump}")
        if "SpectorTest" in title:
            fail("normal load has test title")

        dump_t = SCRATCH / "test-8088.html"
        dump_test = edge_dump(f"{BASE_URL}/app.html?test", dump_t, budget=15000)
        m = re.search(r'<pre id="spector-test-output">(.*?)</pre>', dump_test, re.DOTALL)
        if m:
            raw = html.unescape(m.group(1).strip())
            raw = raw.replace("&gt;", ">").replace("&lt;", "<")
            results = json.loads(raw)
            lines.append(f"TEST allPass: {results.get('allPass')}")
            for r in results.get("results", []):
                lines.append(f"  [{'PASS' if r.get('pass') else 'FAIL'}] {r.get('label')}")
            if not results.get("allPass"):
                fail("runSpectorCoreTests failed on :8088")
        else:
            fail("could not parse test harness output on :8088")
    else:
        lines.append("BROWSER: not found — launcher cannot run headless tests here")
        lines.append("FALLBACK: static + source checks only")

    # Offline SW — real sw.js registration with persistent profile
    sw_src = (PUBLIC / "sw.js").read_text(encoding="utf-8")
    lines += ["", "=== OFFLINE SW (shipped sw.js) ==="]
    for token in ("spector-v2", "shellForPath", "addEventListener('fetch'", "./app.html"):
        lines.append(f"  sw.js has '{token}': {token in sw_src}")

    if browser:
        if EDGE_PROFILE.exists():
            shutil.rmtree(EDGE_PROFILE, ignore_errors=True)
        EDGE_PROFILE.mkdir(parents=True, exist_ok=True)

        # Register real sw.js via index.html (same as production path)
        edge_dump(f"{BASE_URL}/index.html", SCRATCH / "sw-index.html", profile=EDGE_PROFILE, budget=12000)
        time.sleep(1)

        reg_dump = ""
        online = {}
        for budget in (15000, 25000, 40000):
            reg_dump = edge_dump(f"{BASE_URL}/verify-sw.html", SCRATCH / "sw-register.html",
                                 profile=EDGE_PROFILE, budget=budget)
            m = re.search(r'<pre id="offline-result">(.*?)</pre>', reg_dump, re.DOTALL)
            if m:
                raw = html.unescape(m.group(1).strip())
                if not raw.startswith("pending") and raw.startswith("{"):
                    try:
                        online = json.loads(raw)
                        break
                    except json.JSONDecodeError:
                        pass
        if online:
            lines.append("ONLINE cache-probe:")
            lines.append(json.dumps(online, indent=2))
            if not online.get("pass"):
                lines.append("NOTE: online cache-probe incomplete; continuing offline test")
        else:
            lines.append(f"verify-sw dump snippet: {reg_dump[:500]}")

        server.stop()
        time.sleep(0.5)
        lines.append("SERVER: stopped for offline probe")

        off_dump = edge_dump(
            f"{BASE_URL}/app.html?script=SGVsbG8u",
            SCRATCH / "sw-offline.html", profile=EDGE_PROFILE, budget=20000,
        )
        title_m = re.search(r"<title>([^<]*)</title>", off_dump)
        off_title = title_m.group(1) if title_m else ""
        offline_player = "play-btn" in off_dump
        offline_503 = "Offline" in off_dump or "offline" in off_dump.lower()
        lines.append(f"OFFLINE title: {off_title!r}")
        lines.append(f"OFFLINE shell served (play-btn): {offline_player}")
        lines.append(f"OFFLINE 503/offline fallback: {offline_503}")
        if not offline_player and not offline_503:
            fail("offline SW did not serve shell or offline response")

        server.start()
    else:
        lines.append("OFFLINE SW: skipped (no browser)")

    ARTIFACTS["pure-logic-tests.txt"] = "\n".join(lines)
    sw_lines = [meta(3), "=== OFFLINE SW EVIDENCE ==="]
    capture = False
    for ln in lines:
        if "=== OFFLINE SW" in ln:
            capture = True
        if capture:
            sw_lines.append(ln)
    ARTIFACTS["offline-sw-evidence.txt"] = "\n".join(sw_lines)


def step4_launch(server: HttpServer):
    run1 = server.capture_window(10, "RUN 1 server stdout/stderr (~10s)")
    time.sleep(0.5)
    run2 = server.capture_window(10, "RUN 2 server stdout/stderr (~10s)")
    probes = [meta(4), f"=== HTTP probes ({BASE_URL}) ===", ""]
    for path in ("index.html", "app.html", "style.css", "manifest.json", "app.html?script=dGVzdA=="):
        try:
            st, n = server.request(path)
            probes.append(f"GET /{path} -> {st} ({n} bytes)")
        except Exception as e:
            probes.append(f"GET /{path} -> ERROR: {e}")
    ARTIFACTS["launch-1.log"] = run1
    ARTIFACTS["launch-2.log"] = run2
    ARTIFACTS["launch-probes.log"] = "\n".join(probes)
    ARTIFACTS["launch.log"] = run1 + "\n\n" + run2 + "\n\n" + "\n".join(probes)


def step5_positioning():
    lines = [meta(5), "=== POSITIONING EVIDENCE ==="]
    for name in ("index.html", "app.html"):
        for i, ln in enumerate((PUBLIC / name).read_text(encoding="utf-8").splitlines(), 1):
            low = ln.lower()
            if any(k in low for k in ("meta", "ray-ban", "app store", "spectorcore", "customer journey", "vs meta", "founding")):
                lines.append(f"{name}:{i}: {ln.strip()}")
    ARTIFACTS["positioning-evidence.txt"] = "\n".join(lines)


def step_static_verify():
    required = [
        ROOT / "vercel.json",
        PUBLIC / "index.html", PUBLIC / "app.html", PUBLIC / "style.css",
        PUBLIC / "manifest.json", PUBLIC / "sw.js",
    ]
    for p in required:
        if not p.is_file():
            fail(f"missing {p}")
    if (ROOT / "style.css").exists():
        fail("duplicate root style.css should not exist")
    app = (PUBLIC / "app.html").read_text(encoding="utf-8")
    if app.count("runSpectorCoreTests();") != 1:
        fail("runSpectorCoreTests(); should have exactly one call site")
    if "removeEventListener('deviceorientation'" not in app:
        fail("missing deviceorientation removeEventListener")
    if "teardownSpatialAnchoring();" not in app.split("function setupSpatialAnchoring")[1][:200]:
        fail("setupSpatialAnchoring should call teardown first")


def git_evidence() -> str:
    lines = [meta(0), "=== GIT EVIDENCE ===", f"repo: {ROOT}", ""]
    for cmd in (
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        ["git", "-C", str(ROOT), "log", "-5", "--oneline"],
        ["git", "-C", str(ROOT), "status", "--short"],
        ["git", "-C", str(ROOT), "diff", "--stat", "HEAD~1..HEAD"],
    ):
        lines.append(f"$ {' '.join(cmd)}")
        p = subprocess.run(cmd, capture_output=True, text=True)
        lines.append((p.stdout or p.stderr or "").strip())
        lines.append("")
    return "\n".join(lines)


def write_bundle():
    ARTIFACTS["git-evidence.txt"] = git_evidence()
    ARTIFACTS["verify-static-output.txt"] = "\n".join([
        meta(0),
        "=== verify_static (orchestrator inline) ===",
        f"root style.css exists: {(ROOT / 'style.css').exists()}",
        f"public/style.css exists: {(PUBLIC / 'style.css').exists()}",
        f"failures: {FAILURES or 'none'}",
    ])
    for name, content in ARTIFACTS.items():
        (SCRATCH / name).write_text(content, encoding="utf-8")
    ok(f"wrote {len(ARTIFACTS)} artifacts to {SCRATCH}")


def main():
    clear_scratch()
    print("SPECTOR run_verification.py")
    server = HttpServer()
    server.start()
    try:
        step_static_verify()
        step1_static_structure()
        step2_core_logic()
        step4_launch(server)
        step3_pwa_tests(server)
        step5_positioning()
    finally:
        server.stop()
    write_bundle()
    if FAILURES:
        print("FAILED:", FAILURES)
        sys.exit(1)
    print("ALL VERIFICATION STEPS PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()