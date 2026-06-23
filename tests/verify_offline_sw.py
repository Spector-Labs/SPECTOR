#!/usr/bin/env python3
"""
Verify shipped sw.js offline shell strategy:
1) Structural audit of sw.js fetch handler
2) Execute shellForPath extracted from shipped sw.js via headless Edge
"""
import html
import json
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
SW = PUBLIC / "sw.js"
SCRATCH = Path(r"C:\Users\USER\AppData\Local\Temp\grok-goal-ee54e3f7c3b7\implementer")
SCRATCH.mkdir(parents=True, exist_ok=True)
OUT = SCRATCH / "offline-sw-evidence.txt"
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")


def pick_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def extract_shell_for_path(sw_source):
    m = re.search(r"function shellForPath\(pathname\) \{.*?\n\}", sw_source, re.DOTALL)
    return m.group(0) if m else None


def main():
    lines = ["=== Offline SW evidence (shipped sw.js) ===", ""]
    sw_source = SW.read_text(encoding="utf-8")

    lines.append("--- structural audit ---")
    struct_ok = all([
        "spector-v2" in sw_source,
        "function shellForPath" in sw_source,
        "pathname.endsWith('app.html')" in sw_source,
        "./app.html" in sw_source,
        "addEventListener('fetch'" in sw_source,
    ])
    for token in ["spector-v2", "shellForPath", "app.html", "fetch"]:
        lines.append(f"  sw.js contains '{token}': {token in sw_source}")
    lines.append(f"structural audit: {'PASS' if struct_ok else 'FAIL'}")

    shell_fn = extract_shell_for_path(sw_source)
    if not shell_fn:
        lines.append("FAIL: could not extract shellForPath from sw.js")
        OUT.write_text("\n".join(lines), encoding="utf-8")
        print("\n".join(lines))
        sys.exit(1)

    if not EDGE.is_file():
        lines.append("BROWSER: not found — structural audit only")
        OUT.write_text("\n".join(lines), encoding="utf-8")
        print("\n".join(lines))
        sys.exit(0 if struct_ok else 1)

    harness = PUBLIC / "sw-shell-exec.html"
    harness.write_text(
        f"""<!DOCTYPE html><html><body><pre id="out"></pre><script>
{shell_fn}
const cases = [
  ['/app.html', './app.html'],
  ['/index.html', './index.html'],
  ['/foo', null]
];
const results = cases.map(([p, exp]) => ({{ path: p, got: shellForPath(p), exp, ok: shellForPath(p) === exp }}));
const pass = results.every(r => r.ok);
document.getElementById('out').textContent = JSON.stringify({{ pass, results }}, null, 2);
document.title = pass ? 'SWShell: PASS' : 'SWShell: FAIL';
</script></body></html>""",
        encoding="utf-8",
    )

    port = pick_port()
    url = f"http://127.0.0.1:{port}/sw-shell-exec.html"
    lines.append(f"PORT: {port}")
    lines.append(f"exec URL: {url}")

    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--directory", str(PUBLIC)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    time.sleep(1.2)

    dump_path = SCRATCH / "sw-shell-dump.html"
    proc = subprocess.run(
        [
            str(EDGE), "--headless=new", "--disable-gpu", "--no-sandbox",
            f"--dump-dom={str(dump_path).replace(chr(92), '/')}",
            "--virtual-time-budget=5000", url,
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )

    dump = dump_path.read_text(encoding="utf-8", errors="replace") if dump_path.is_file() else (proc.stdout or "")
    lines.append(f"dump bytes: {len(dump)}")

    exec_pass = False
    m = re.search(r'<pre id="out">(.*?)</pre>', dump, re.DOTALL)
    if m:
        payload = json.loads(html.unescape(m.group(1).strip()))
        lines.append(f"shellForPath exec pass: {payload.get('pass')}")
        lines.append(json.dumps(payload, indent=2))
        exec_pass = payload.get("pass") is True
    else:
        lines.append("FAIL: could not parse shell exec output")
        lines.append(f"snippet: {dump[:800]}")

    server.terminate()
    passed = struct_ok and exec_pass
    lines.append(f"OVERALL: {'PASS' if passed else 'FAIL'}")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()