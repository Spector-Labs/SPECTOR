#!/usr/bin/env python3
"""Static verification for SPECTOR — structural checks on shipped files."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
FAILURES = []


def check(label, condition):
    if not condition:
        FAILURES.append(label)
    return condition


def main():
    print("SPECTOR static verification")
    print("ROOT:", ROOT)

    required = [
        ROOT / "vercel.json",
        PUBLIC / "index.html",
        PUBLIC / "app.html",
        PUBLIC / "style.css",
        PUBLIC / "manifest.json",
        PUBLIC / "sw.js",
    ]
    for p in required:
        check(f"exists: {p.relative_to(ROOT)}", p.is_file())
        print(f"  {'OK' if p.is_file() else 'MISSING'}: {p}")

    check("no duplicate root style.css", not (ROOT / "style.css").exists())
    print(f"  root style.css absent: {not (ROOT / 'style.css').exists()}")

    for html in [PUBLIC / "index.html", PUBLIC / "app.html"]:
        text = html.read_text(encoding="utf-8")
        check(f"{html.name} uses style.css", 'href="style.css"' in text)
        check(f"{html.name} no styles.css", "styles.css" not in text)

    vercel = json.loads((ROOT / "vercel.json").read_text())
    check("vercel outputDirectory=public", vercel.get("outputDirectory") == "public")

    app = (PUBLIC / "app.html").read_text(encoding="utf-8")
    css = (PUBLIC / "style.css").read_text(encoding="utf-8")

    import re
    check("single runSpectorCoreTests() invocation", app.count("runSpectorCoreTests();") == 1)
    call_idx = app.find("runSpectorCoreTests();")
    init_idx = app.find("function init()")
    test_guard_idx = app.find("has('test')", init_idx)
    check("runSpectorCoreTests(); only inside ?test guard",
          call_idx > test_guard_idx > init_idx)
    check("app has teardownSpatialAnchoring", "function teardownSpatialAnchoring" in app)
    check("app removes deviceorientation listener", "removeEventListener('deviceorientation'" in app)

    core_units = [
        "class KalmanFilter", "function hybridChunk", "function getMs",
        "function setupSpatialAnchoring", "function startDualSineBreathing",
        "function startGentleDriftWithRotation", "function settleActiveChunk",
        "function applyMode", "function getScriptFromURL", "function render",
        "function updateDisplay", "function startPlayback", "function stopPlayback",
        "function togglePlay", "function showEndScreen", "function init",
        "runSpectorCoreTests", "SpectorCore", "registerChunker", "registerPostChunkHook",
    ]
    for unit in core_units:
        check(f"app.html contains {unit}", unit in app)

    css_rules = [
        "body.glasses", ".chunk.active", "#script-container", ".progress-fill",
        ".speed-presets", ".controls", ".mode-btn", ".end-screen", ".hidden",
        "comfort-mode", "prefers-reduced-motion",
    ]
    for rule in css_rules:
        check(f"style.css contains {rule}", rule in css)

    manifest = json.loads((PUBLIC / "manifest.json").read_text())
    check("manifest name", "Spector" in manifest.get("name", ""))
    check("manifest display standalone", manifest.get("display") == "standalone")

    check("index has library", "spector_scripts_v1" in (PUBLIC / "index.html").read_text())
    check("index has glasses-future", "glasses-future" in (PUBLIC / "index.html").read_text())
    check("app has WPM", "end-wpm" in app)
    check("app has customize", "customize-panel" in app)

    print("\n--- RESULT ---")
    if FAILURES:
        print("FAIL:", len(FAILURES))
        for f in FAILURES:
            print(" ", f)
        sys.exit(1)
    print("ALL STATIC CHECKS PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()