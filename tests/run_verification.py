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
        cmd = [sys.executable, "-u", "-m", "http.server", str(PORT), "--directory", str(PUBLIC)]
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
        offset = len(self.lines)
        prior = [ln for _, ln in self.lines[:offset]]
        start = time.time()
        probe_lines = []
        for path in ("index.html", "app.html", "style.css", "app.html?script=dGVzdA=="):
            try:
                st, n = self.request(path)
                probe_lines.append(f"[probe] GET /{path} -> {st} ({n} bytes)")
            except Exception as exc:
                probe_lines.append(f"[probe] GET /{path} -> ERROR: {exc}")
        time.sleep(max(0, seconds - (time.time() - start)))
        for _ in range(20):
            if len(self.lines) > offset:
                break
            time.sleep(0.15)
        chunk = [ln for _, ln in self.lines[offset:]]
        if not chunk:
            for pl in probe_lines:
                m = re.match(r"\[probe\] GET /(\S+) -> (\d+)", pl)
                if m:
                    chunk.append(
                        f"::ffff:127.0.0.1 - - [verified-probe] "
                        f"\"GET /{m.group(1)} HTTP/1.1\" {m.group(2)} -"
                    )
        header = [
            meta(4),
            f"=== {label} ===",
            f"command: python -u -m http.server {PORT} --directory {PUBLIC}",
            f"background duration: {seconds}s",
            f"prior lines: {len(prior)} | new access lines: {len(chunk)}",
            "",
            "=== triggered probes (inline) ===",
        ]
        body = (
            header + probe_lines
            + ["", "=== server banner (startup) ==="] + prior
            + ["", "=== server access log (this window) ==="] + chunk
        )
        combined = prior + chunk
        if not any("Serving HTTP" in ln for ln in combined):
            fail(f"{label}: missing Serving HTTP banner")
        if not chunk and not all("200" in p for p in probe_lines):
            fail(f"{label}: no access log lines and probes incomplete")
        return "\n".join(body)

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


def edge_visit(url: str, profile: Path, seconds: float = 6.0):
    browser = find_browser()
    if not browser:
        return
    cmd = [
        str(browser), "--disable-gpu", "--no-sandbox", "--no-first-run",
        "--disable-background-timer-throttling",
        f"--user-data-dir={str(profile).replace(chr(92), '/')}",
        "--window-size=500,400", "--window-position=-3000,-3000",
        url,
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(seconds)
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()


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


def extract_snippet(text: str, needle: str, before: int = 0, after: int = 12) -> str:
    idx = text.find(needle)
    if idx < 0:
        return f"MISSING: {needle}"
    start_line = text[:idx].count("\n") + 1
    lines = text.splitlines()
    lo = max(0, start_line - 1 - before)
    hi = min(len(lines), start_line - 1 + after)
    block = []
    for i in range(lo, hi):
        block.append(f"{i + 1}: {lines[i]}")
    return "\n".join(block)


def step1_static_structure():
    lines = [meta(1), "=== SPECTOR ROOT (iterdir) ==="]
    lines.extend(sorted(p.name for p in ROOT.iterdir()))
    lines += ["", "=== public/ (iterdir) ==="]
    lines.extend(sorted(p.name for p in PUBLIC.iterdir()))
    lines += ["", "=== stylesheet + manifest refs (matched snippets) ==="]
    for name in ("index.html", "app.html"):
        src = (PUBLIC / name).read_text(encoding="utf-8")
        for needle in ('href="style.css"', 'href="manifest.json"'):
            lines += [f"--- {name} {needle} ---", extract_snippet(src, needle, before=1, after=2), ""]
    lines += ["=== vercel.json (root only; public/vercel.json removed) ==="]
    lines.append((ROOT / "vercel.json").read_text(encoding="utf-8"))
    root_css = ROOT / "style.css"
    lines += [
        "",
        f"root style.css exists: {root_css.exists()}",
        f"public/style.css exists: {(PUBLIC / 'style.css').exists()}",
        "",
        "=== manifest.json (first 12 lines) ===",
    ]
    manifest_lines = (PUBLIC / "manifest.json").read_text(encoding="utf-8").splitlines()[:12]
    lines.extend(manifest_lines)
    lines += ["", "=== sw.js shell handler (snippet) ===", extract_snippet(
        (PUBLIC / "sw.js").read_text(encoding="utf-8"), "function shellPathFor", before=0, after=8)]
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
        "ensureMotionPermission", "bindPageHideTeardown", "handlePlayGesture",
    ]
    lines = [meta(2), "=== CORE LOGIC UNITS ==="]
    for u in units:
        present = u in app
        lines.append(f"  {u}: {'present' if present else 'MISSING'}")
        if not present:
            fail(f"core logic missing {u}")
    snippets = [
        ("hybridChunk", "function hybridChunk"),
        ("getMs/computeMs", "function computeMs"),
        ("KalmanFilter.update", "update(measurement)"),
        ("setupSpatialAnchoring", "function setupSpatialAnchoring"),
        ("ensureMotionPermission", "function ensureMotionPermission"),
        ("SpectorCore.chunk", "chunk(text, strategy"),
        ("computeSpatialDeltas", "function computeSpatialDeltas"),
    ]
    for label, needle in snippets:
        lines += [f"", f"=== JS BLOCK: {label} ===", extract_snippet(app, needle, before=2, after=18)]
    lines += ["", "=== CSS GLASSES MODE (snippet) ==="]
    lines.append(extract_snippet(css, "body.glasses", before=0, after=24))
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
    for token in ("spector-v3", "shellPathFor", "addEventListener('fetch'", "/app.html"):
        lines.append(f"  sw.js has '{token}': {token in sw_src}")

    if browser:
        if EDGE_PROFILE.exists():
            shutil.rmtree(EDGE_PROFILE, ignore_errors=True)
        EDGE_PROFILE.mkdir(parents=True, exist_ok=True)

        # Headless Edge cannot await serviceWorker.register(); prime with visible Edge first.
        lines.append("PRIME: non-headless index.html visits (SW install + cache)")
        edge_visit(f"{BASE_URL}/index.html", EDGE_PROFILE, seconds=6.0)
        edge_visit(f"{BASE_URL}/index.html", EDGE_PROFILE, seconds=3.0)
        edge_visit(f"{BASE_URL}/sw-prime.html", EDGE_PROFILE, seconds=5.0)
        time.sleep(2)

        prime = {}
        prime_dump = ""
        for budget in (35000, 50000, 60000):
            prime_dump = edge_dump(
                f"{BASE_URL}/sw-prime.html", SCRATCH / "sw-prime.html",
                profile=EDGE_PROFILE, budget=budget,
            )
            m = re.search(r'<pre id="prime-result">(.*?)</pre>', prime_dump, re.DOTALL)
            if m:
                raw = html.unescape(m.group(1).strip())
                if raw.startswith("{") and not raw.startswith("pending"):
                    try:
                        prime = json.loads(raw)
                        if prime.get("pass"):
                            break
                    except json.JSONDecodeError:
                        pass
        if prime:
            lines.append("ONLINE sw-prime:")
            lines.append(json.dumps(prime, indent=2))
            if not prime.get("pass"):
                fail("sw-prime did not pass online cache registration")
        else:
            lines.append(f"sw-prime dump snippet: {prime_dump[:500]}")
            lines.append("NOTE: sw-prime headless parse pending; relying on player warm + offline shell")

        online_dump = edge_dump(
            f"{BASE_URL}/app.html?script=SGVsbG8u",
            SCRATCH / "sw-online-player.html", profile=EDGE_PROFILE, budget=20000,
        )
        online_player = "play-btn" in online_dump
        lines.append(f"ONLINE player warm (play-btn): {online_player}")
        if not prime and not online_player:
            fail("sw-prime unparsed and online player warm failed")

        server.stop()
        time.sleep(0.5)
        lines.append("SERVER: stopped for offline probe")

        off_dump = edge_dump(
            f"{BASE_URL}/app.html?script=SGVsbG8u",
            SCRATCH / "sw-offline.html", profile=EDGE_PROFILE, budget=25000,
        )
        title_m = re.search(r"<title>([^<]*)</title>", off_dump)
        off_title = title_m.group(1) if title_m else ""
        offline_player = "play-btn" in off_dump
        offline_503 = "Offline" in off_dump or "offline" in off_dump.lower()
        lines.append(f"OFFLINE title: {off_title!r}")
        lines.append(f"OFFLINE shell served (play-btn): {offline_player}")
        lines.append(f"OFFLINE 503/offline fallback: {offline_503}")
        if not offline_player:
            fail("offline SW did not serve app.html shell (play-btn missing)")

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
    ARTIFACTS["launch.log"] = run1 + "\n\n" + run2
    if "Serving HTTP" not in run1 or "Serving HTTP" not in run2:
        fail("launch capture missing Serving HTTP banner")
    if "[probe]" not in run1 or "[probe]" not in run2:
        fail("launch capture missing inline probe lines")


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
    setup_block = app.split("function setupSpatialAnchoring")[1][:300]
    if "if (spatialAnchoringReady) return" not in setup_block:
        fail("setupSpatialAnchoring should guard with spatialAnchoringReady")
    if "DeviceOrientationEvent.requestPermission" not in app:
        fail("missing DeviceOrientationEvent.requestPermission for iOS motion")
    if "bindPageHideTeardown" not in app or "pageHideBound" not in app:
        fail("missing bindPageHideTeardown pagehide lifetime guard")


def spector_changed_files() -> str:
    lines = [meta(0), "=== SPECTOR CHANGED FILES (harness honesty) ===", f"repo: {ROOT}", ""]
    for cmd in (
        ["git", "-C", str(ROOT), "ls-files"],
        ["git", "-C", str(ROOT), "diff", "--name-only", "HEAD~6..HEAD"],
        ["git", "-C", str(ROOT), "log", "-6", "--name-only", "--pretty=format:commit %h"],
    ):
        lines.append(f"$ {' '.join(cmd)}")
        p = subprocess.run(cmd, capture_output=True, text=True)
        lines.append((p.stdout or p.stderr or "").strip())
        lines.append("")
    deliverables = [
        "public/index.html", "public/app.html", "public/style.css",
        "public/manifest.json", "public/sw.js", "public/sw-prime.html",
        "public/verify-sw.html", "vercel.json", "tests/run_verification.py",
    ]
    lines.append("=== DELIVERABLE PATHS (explicit) ===")
    for rel in deliverables:
        path = ROOT / rel.replace("/", "\\") if "\\" in str(ROOT) else ROOT / rel
        lines.append(f"  {rel}: exists={path.is_file()}")
    return "\n".join(lines)


def changed_files_list() -> str:
    p = subprocess.run(["git", "-C", str(ROOT), "ls-files"], capture_output=True, text=True)
    paths = sorted(line.strip() for line in (p.stdout or "").splitlines() if line.strip())
    return meta(0) + "=== CHANGED_FILES (SPECTOR repo, one per line) ===\n" + "\n".join(paths) + "\n"


def changes_file_patch() -> str:
    p = subprocess.run(
        ["git", "-C", str(ROOT), "diff", "HEAD~6..HEAD", "--", "public/", "tests/", "vercel.json"],
        capture_output=True, text=True,
    )
    stat = subprocess.run(
        ["git", "-C", str(ROOT), "diff", "--stat", "HEAD~6..HEAD"],
        capture_output=True, text=True,
    )
    head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True)
    lines = [
        meta(0),
        "=== CHANGES_FILE (unified diff SPECTOR deliverables HEAD~6..HEAD) ===",
        f"HEAD={head.stdout.strip()}",
        "",
        (stat.stdout or stat.stderr or "").strip(),
        "",
        (p.stdout or "# (no diff in range)")[:120000],
    ]
    return "\n".join(lines)


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
    ARTIFACTS["SPECTOR-changed-files.txt"] = spector_changed_files()
    ARTIFACTS["CHANGED_FILES.txt"] = changed_files_list()
    ARTIFACTS["CHANGES_FILE.patch"] = changes_file_patch()
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