#!/usr/bin/env python3
"""
Verify shipped pure-logic test harness in app.html.
Browser execution required for full run; this script audits the test block
and validates algorithm constants match shipped source.
"""
import re
import sys
from pathlib import Path

APP = Path(__file__).resolve().parent.parent / "public" / "app.html"
source = APP.read_text(encoding="utf-8")
FAILURES = []


def check(label, cond):
    if not cond:
        FAILURES.append(label)
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")


print("SpectorCore pure-logic test harness audit")

check("runSpectorCoreTests defined", "function runSpectorCoreTests()" in source)
check("uses SpectorCore.chunk", "SpectorCore.chunk(sample" in source)
check("uses SpectorCore.getMs", "SpectorCore.getMs(" in source)
check("uses SpectorCore.KalmanFilter", "new SpectorCore.KalmanFilter()" in source)
check("uses computeSpatialDeltas", "SpectorCore.computeSpatialDeltas" in source)
check("uses registerPostChunkHook", "SpectorCore.registerPostChunkHook" in source)
check("sets __spectorTestResults", "window.__spectorTestResults" in source)
check("runs on init", "runSpectorCoreTests();" in source)
check("?test early exit", "has('test')" in source)

# Audit shipped algorithm constants (not reimplemented — read from source)
check("getMs base 2400", "let base = 2400" in source)
check("getMs min 1200", "Math.max(1200, base)" in source)
check("hybrid chunk word size 6", "i += 6" in source)
check("Kalman Q 0.0025", "0.0025" in source)

m = re.search(r"function runSpectorCoreTests\(\) \{([\s\S]*?)\n    \}", source)
check("test function extractable", m is not None)

print("\n--- RESULT ---")
if FAILURES:
    print("FAILURES:", FAILURES)
    sys.exit(1)
print("TEST HARNESS AUDIT PASS (execute in browser: app.html or app.html?test)")
sys.exit(0)