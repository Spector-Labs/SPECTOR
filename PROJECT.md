# SPECTOR — Project Status & Roadmap 

**Last updated:** June 24, 2026 (thorough pre-domain pass: punchier Glasses & Future, actionable beta form with mailto + model field, added TEDx preset, history note, consistent domain language across docs)
**Repository:** [github.com/hydrogenbondss/SPECTOR](https://github.com/hydrogenbondss/SPECTOR)  
**Live URL:** https://spector-plum.vercel.app (spector.com launching soon)  
**Latest commit:** current (see git log)

---

## Executive summary

SPECTOR is a premium digital teleprompter positioned to outperform Meta’s built-in Ray-Ban glasses teleprompter — the same way Google Maps wins against Apple Maps: deeper workflow, not default placement.

As smart glasses become more common, more people will need rehearsal tools *before* built-in HUD teleprompters mature. SPECTOR is a **teleprompter app** (not a glasses retailer) — phone/PWA rehearsal today, portable `SpectorCore` engine ready for Meta’s rumored glasses app store (late 2026–early 2027). Not affiliated with Meta or Ray-Ban.

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
| **iOS motion fix** | Done | `ensureMotionForPlayback()` skips motion setup when already bound |
| **Meta positioning** | Done | Landing “Glasses & Future” section; compatibility notes, not hardware sales |
| **Modular core** | Done | `window.SpectorCore` — chunk registry, hooks, `createMotion()` |
| **First-run coach + hardware legend** | Done | One-time toast auto-highlights Comfort + button note; persistent .glasses-hw-legend under modes with right-temple mappings |
| **Beta assets** | Done | Landing beta signup form + README Beta Program section focused on hardware testing |
| **End-screen reinforcement** | Done | Subtitle and analytics note tie rehearsal stats to real glasses button use |
| **Punchier positioning** | Done | Condensed “Glasses & Future” to benefit-led paragraphs |
| **Actionable beta + presets** | Done | Real mailto beta form with glasses model field; added Wedding Toast + Earnings Call presets |
| **History clarity** | Done | Local history with explicit note on future cloud sync |

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

**Device coverage:** 
- Ray-Ban Meta Display / HUD (primary: run on-glasses lens HUD; right temple button + touch + future Neural Band for control).
- Gen 1/2 and non-Display (phone companion rehearsal with haptics).
- Other brands (XREAL, Viture, Brilliant Labs, Even Realities, etc.): PWA on phone or browser. Varying input methods.
Not Ray-Ban exclusive. Web + PWA approach maximizes compatibility today.

---

## Deployment status (verified June 24, 2026)

| Check | Result |
|-------|--------|
| URL responds | **Yes** — https://spector-plum.vercel.app returns HTTP 200 |
| Hosted on Vercel | **Yes** — `X-Vercel-Id` header present |
| Serving latest code | **Yes** — verified live (full pass updates) |

**Verified on production:**

- `href="style.css"` (canonical asset path)
- Saved Scripts library, hero badge, teleprompter disclaimer
- GitHub → Vercel auto-deploy connected and working

**Live:** https://spector-plum.vercel.app (spector.com launching soon)

---

## Plan moving forward

### Phase 1 — Ship & validate (now → 2 weeks)

- [x] **Redeploy Vercel** to latest `main` and verify live matches GitHub
- [x] **Thorough pre-domain pass** (punchier copy, actionable beta, presets, history notes, button sim, consistent language)
- [ ] **Set `git config --global user.name`** for commit attribution (email already set)
- [ ] **Beta test on real glasses** via Developer Mode ([TESTING.md](./TESTING.md))
- [ ] **Gather feedback** on button mapping, Comfort on HUD, comparison to native teleprompter
- [ ] **Acquire spector.com** and run migration script + flip

### Phase 2 — Creator essentials (2–6 weeks)

- [ ] **Mirror mode polish** — optional horizontal flip only for text, preserve controls UI
- [ ] **Cue marker editor** — visual toolbar to insert `**emphasis**` / `[pause]` without typing syntax
- [ ] **Rehearsal analytics v2** — per-run history in `localStorage`, trend chart (pacing over sessions)
- [ ] **Section bookmarks** — `## Section` headers → jump list in player
- [ ] **Export/share** — copy script + stats summary for collaborators

### Phase 3 — Broader smart-glasses adoption (Q3–Q4 2026)

- [ ] **Onboarding flow** — first-run tour for new glasses owners (“rehearse on phone → perform on glasses”)
- [ ] **Preset scripts** — demo keynotes/interviews for instant wow
- [ ] **Hardware controls & gesture map** — right temple button/touch on Display models today (where events forward); Neural Band subtle gestures (pinch/advance/pause/rewind) when Meta exposes APIs. Support other brands' controllers/touch too.
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

### Strategic / Meta angle (4)

- **Real glasses testing:** Use TESTING.md to recruit Display + non-Display + other brand users. Focus feedback on button usability, HUD readability, Comfort spatial on glasses vs phone, comparison to Meta's built-in teleprompter (now available on Display models).
- **Meta decision:** This validates demand for pro rehearsal tooling. Options: 1) Rapidly enhance native Meta AI / glasses teleprompter with library, auto-pace, cues, analytics, button mapping, Comfort-like presence. 2) Open primitives (button events, HUD rendering, Neural Band) earlier to enable third-party like SPECTOR as complements. 3) Feature high-quality apps in the ecosystem.
- **Adoption:** Track via future anonymous events or manual (samples used, Comfort tried, end reached, beta signups). Use to decide native vs platform investment. SPECTOR can serve as reference implementation or acquisition target if traction on real hardware.

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
https://spector-plum.vercel.app/app.html?test (same on spector.com after migration)
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
- **Live:** https://spector-plum.vercel.app (spector.com launching soon)
- **Competition:** Meta Ray-Ban teleprompter (in-app, paste + manual advance)  
- **Note:** SPECTOR sells teleprompter software only — not smart glasses or Meta hardware
- **Pre-domain status:** Thorough pass complete (see DOMAIN.md checklist). Ready for purchase + migration.

---

*This document should be updated after each major release or deployment verification.*
