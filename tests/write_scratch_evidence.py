#!/usr/bin/env python3
"""Write verification plan scratch artifacts (static-structure, core-logic, positioning)."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
SCRATCH = Path(r"C:\Users\USER\AppData\Local\Temp\grok-goal-ee54e3f7c3b7\implementer")
SCRATCH.mkdir(parents=True, exist_ok=True)


def main():
    struct = SCRATCH / "static-structure.txt"
    lines = ["=== SPECTOR ROOT ===", *sorted(p.name for p in ROOT.iterdir()), "", "=== public/ ==="]
    lines.extend(sorted(p.name for p in PUBLIC.iterdir()))
    lines.append("")
    lines.append("=== stylesheet refs ===")
    for html in ["index.html", "app.html"]:
        text = (PUBLIC / html).read_text(encoding="utf-8")
        for ln in text.splitlines():
            if "stylesheet" in ln:
                lines.append(f"{html}: {ln.strip()}")
    lines.append("")
    lines.append("=== vercel.json ===")
    lines.append((ROOT / "vercel.json").read_text(encoding="utf-8"))
    struct.write_text("\n".join(lines), encoding="utf-8")

    core = SCRATCH / "core-logic.txt"
    app = (PUBLIC / "app.html").read_text(encoding="utf-8")
    markers = ["class KalmanFilter", "const SpectorCore", "function splitSentences",
               "function teardownSpatialAnchoring", "runSpectorCoreTests"]
    core_lines = ["=== CORE LOGIC MARKERS ==="]
    for m in markers:
        idx = app.find(m)
        core_lines.append(f"\n--- {m} @ {idx} ---")
        if idx >= 0:
            core_lines.append(app[idx:idx + 400])
    core.write_text("\n".join(core_lines), encoding="utf-8")

    pos = SCRATCH / "positioning-evidence.txt"
    pos_lines = ["=== POSITIONING ==="]
    for name in ["index.html", "app.html"]:
        for i, ln in enumerate((PUBLIC / name).read_text(encoding="utf-8").splitlines(), 1):
            low = ln.lower()
            if any(k in low for k in ["meta", "ray-ban", "app store", "spectorcore", "customer journey", "vs meta"]):
                pos_lines.append(f"{name}:{i}: {ln.strip()}")
    pos.write_text("\n".join(pos_lines), encoding="utf-8")

    git_out = SCRATCH / "git-evidence.txt"
    cmds = [
        ["git", "-C", str(ROOT), "log", "-5", "--oneline"],
        ["git", "-C", str(ROOT), "status", "--short"],
        ["git", "-C", str(ROOT), "ls-files"],
    ]
    g = ["=== GIT EVIDENCE ===", f"repo: {ROOT}", ""]
    for cmd in cmds:
        g.append(f"$ {' '.join(cmd)}")
        p = subprocess.run(cmd, capture_output=True, text=True)
        g.append(p.stdout or p.stderr or "")
        g.append("")
    git_out.write_text("\n".join(g), encoding="utf-8")
    print("Wrote scratch evidence to", SCRATCH)


if __name__ == "__main__":
    main()