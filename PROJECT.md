# SPECTOR — Project Status & Roadmap 

**Last updated:** June 24, 2026 (deployment confirmed live)
**Repository:** [github.com/hydrogenbondss/SPECTOR](https://github.com/hydrogenbondss/SPECTOR)  
**Live URL:** [spector-plum.vercel.app](https://spector-plum.vercel.app)  
**Latest commit:** `760e788` (main)

---

## Executive summary

SPECTOR is a premium digital teleprompter positioned to outperform Meta’s built-in Ray-Ban glasses teleprompter — the same way Google Maps wins against Apple Maps: deeper workflow, not default placement.

Meta announced new smart glasses starting at **$299** (June 23, 2026), which will bring millions of new users who need rehearsal tools *before* HUD teleprompter features mature. SPECTOR targets that wave with phone/PWA rehearsal today and a portable `SpectorCore` engine ready for Meta’s rumored glasses app store (late 2026–early 2027).

---

## What we have done

### Product & UX (shipped in code)

| Area | Status | Details |
|------|--------|---------|
| **Script library** | Done | `localStorage` persistence, save/load, file upload on landing |
| **Adaptive pacing** | Done | Hybrid chunking, `getMs()` by mode/speed/punctuation |
| **Comfort spatial** | Done | Kalman filtering, breathing/drift in Comfort mode, haptics |
| **Player modes** | Done | Comfort / Focus / Presentation + Slow/Normal/Fast |
| **Customization** | Done | Text size, leading, Compact HUD toggle |
| **Mirror mode** | Done | Toggle for camera/mirror-facing setups |
| **Cue markers** | Done | `**emphasis**`, `[pause]`, `[pause:3s]` inline syntax |
| **Rehearsal analytics** | Done | End-screen pacing %, hesitations, slowest chunk |
| **PWA / offline** | Done | `manifest.json`, `sw.js` v3, offline shell verified |
| **iOS motion fix** | Done | `motionReadyForPlay()` skips re-prompt when already granted |
| **Meta positioning** | Done | Landing “Glasses & Future” section, $299 market note |
| **Modular core** | Done | `window.SpectorCore` — chunk registry, hooks, `createMotion()` |

### Infrastructure & quality

| Area | Status | Details |
|------|--------|---------|
| **Static hosting** | Done | `vercel.json` → `public/` output directory |
| **Canonical assets** | Done | Single `public/style.css` (no `styles.css` split) |
| **Verification** | Done | `tests/run_verification.py` — single entry point, 15 artifacts |
| **GitHub** | Done | `main` pushed with full revamp + merge of prior remote history |
| **Git identity** | Done | Global email set to `jeffreynicholas.t@gmail.com` |

### Competitive positioning (vs Meta teleprompter)

- **Meta today:** Paste in Meta AI app → basic scroll/cards → manual Neural Band advance  
- **SPECTOR:** Script library → adaptive auto-pace → comfort spatial effects → cue markers → rehearsal analytics → PWA install for daily use  

**Device coverage:** Ray-Ban Meta Display (primary HUD path), Gen 1/2 (phone companion rehearsal), and any smart-glasses user via web + PWA — not Ray-Ban exclusive.

---

## Deployment status (verified June 24, 2026)

| Check | Result |
|-------|--------|
| URL responds | **Yes** — `https://spector-plum.vercel.app` returns HTTP 200 |
| Hosted on Vercel | **Yes** — `X-Vercel-Id` header present |
| Serving latest code | **Yes** — verified live (revamp build) |

**Verified on production:**

- `href="style.css"` (canonical asset path)
- Saved Scripts library, hero badge, $299 market note
- GitHub → Vercel auto-deploy connected and working

**Live:** [spector-plum.vercel.app](https://spector-plum.vercel.app)

---

## Plan moving forward

### Phase 1 — Ship & validate (now → 2 weeks)

- [x] **Redeploy Vercel** to latest `main` and verify live matches GitHub
- [ ] **Set `git config --global user.name`** for commit attribution (email already set)
- [ ] **Beta test on real glasses** via Developer Mode ([TESTING.md](./TESTING.md))
- [ ] **Gather feedback** on mirror mode, cue syntax, analytics usefulness

### Phase 2 — Creator essentials (2–6 weeks)

- [ ] **Mirror mode polish** — optional horizontal flip only for text, preserve controls UI
- [ ] **Cue marker editor** — visual toolbar to insert `**emphasis**` / `[pause]` without typing syntax
- [ ] **Rehearsal analytics v2** — per-run history in `localStorage`, trend chart (pacing over sessions)
- [ ] **Section bookmarks** — `## Section` headers → jump list in player
- [ ] **Export/share** — copy script + stats summary for collaborators

### Phase 3 — Mass-market $299 wave (Q3–Q4 2026)

- [ ] **Onboarding flow** — first-run tour for new glasses owners (“rehearse on phone → perform on glasses”)
- [ ] **Preset scripts** — demo keynotes/interviews for instant wow
- [ ] **Neural Band gesture map** — when Meta exposes APIs: tap = next, double = rewind
- [ ] **Landing refresh** — social proof, short demo video, comparison table vs Meta teleprompter

### Phase 4 — App store founding developer (late 2026–2027)

- [ ] **Port `SpectorCore`** to Meta glasses SDK / native wrapper when store opens
- [ ] **One-tap “Send to glasses”** from script library
- [ ] **Optional cloud sync** — scripts across phone ↔ glasses (accounts + thin API)
- [ ] **Plugin marketplace** — third-party chunk strategies, ASR hooks, language packs

### Explicit non-goals (for now)

- Native App Store / Play Store binaries  
- Server backend or user accounts (until app store requires it)  
- Direct Bluetooth / Neural Band proprietary protocols (unavailable today)  
- Video recording / multi-device director mode  

---

## Technical reference

```
SPECTOR/
├── public/
│   ├── index.html      # Landing, script library, positioning
│   ├── app.html        # Player + SpectorCore + ?test harness
│   ├── style.css       # Canonical styles (landing + glasses mode)
│   ├── manifest.json   # PWA manifest
│   ├── sw.js           # Service worker v3
│   └── sw-prime.html   # SW registration helper
├── tests/
│   └── run_verification.py
├── vercel.json         # { "outputDirectory": "public" }
├── TESTING.md          # Real glasses Developer Mode guide
└── PROJECT.md          # This file
```

**Run verification locally:**

```bash
python tests/run_verification.py
```

**Run unit tests in browser:**

```
https://spector-plum.vercel.app/app.html?test
```
(After redeploy — should show `SpectorTest: ALL PASS` with 27+ assertions)

---

## Cue marker syntax (quick reference)

| Syntax | Effect |
|--------|--------|
| `**word or phrase**` | Visual emphasis + slightly longer hold |
| `[pause]` | Inserts a ~2.8s pause chunk |
| `[pause:3s]` | Inserts a 3-second pause chunk |

---

## Contact & links

- **GitHub:** https://github.com/hydrogenbondss/SPECTOR  
- **Live:** https://spector-plum.vercel.app
- **Competition:** Meta Ray-Ban teleprompter (in-app, paste + manual advance)  
- **Market event:** Meta smart glasses from $299 — June 23, 2026  

---

*This document should be updated after each major release or deployment verification.*
