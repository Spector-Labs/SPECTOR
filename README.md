# Spector™ • Eyes Forward

**Auto-paced, comfort-tuned teleprompter for smart glasses and serious rehearsal.**

[![Live Demo](https://img.shields.io/badge/Live-spectorlabs.io-000?style=flat-square)](https://spectorlabs.io)
[![PWA](https://img.shields.io/badge/PWA-Installable-000?style=flat-square)](https://spectorlabs.io)
[![GitHub](https://img.shields.io/badge/GitHub-Spector-Labs/SPECTOR-000?style=flat-square)](https://github.com/Spector-Labs/SPECTOR)

**Current live:** https://spectorlabs.io

**Rehearse on your phone. Perform with confidence on glasses.**

Spector is a premium digital teleprompter PWA (software only). It gives creators, speakers, and presenters a dramatically better rehearsal experience than basic paste-and-scroll tools — plus a modular engine built for the coming smart glasses platforms.

> Not affiliated with Meta, Ray-Ban, or any glasses manufacturer. Works with any smart-glasses workflow.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute, testing instructions, and development notes.

License: [MIT](LICENSE)

---

## Live Demo & Install

**Try it instantly:** [https://spectorlabs.io](https://spectorlabs.io) — no account needed.

- Paste or drop a .txt script
- Hit **Launch Teleprompter**
- Choose Comfort / Focus / Presentation + Slow/Normal/Fast
- Use cue syntax for emphasis and pauses
- Get rehearsal analytics (pacing %, hesitations, slowest chunk) at the end
- **Install as PWA** for offline daily use (Add to Home Screen)

**Install button** is prominent on the landing. One-tap PWA install where supported (Chrome/Edge); clear guidance for iOS and others. Full offline support via service worker.

---

## See It In Action

The best way to experience Spector is directly on the site:

- Load one of the sample scripts (they include real cue syntax)
- Use the cue toolbar buttons to insert **emphasis** or pauses
- Watch the live word count and estimated duration
- Launch the player for adaptive pacing, Comfort spatial mode, and the hardware controls info (including right-temple button guidance for Ray-Ban Meta Display)

Real screenshots, usage photos, and a screen-recorded demo will be added after beta feedback from actual hardware. The assets/ folder currently contains early concept renders.

---

## Key Features

| Area                  | What Spector Delivers                              |
|-----------------------|----------------------------------------------------|
| **Script Library**    | Save, load, delete; localStorage; 20 recent max; file upload + drag/drop |
| **Adaptive Pacing**   | Hybrid chunking (sentences → ~6-word groups), punctuation-aware timing, speed presets |
| **Comfort Spatial**   | Kalman-filtered device motion → subtle head-tilt translation/rotation/scale + breathing & drift animations (Comfort mode only) |
| **Cue Markers**       | `**emphasis**` (stronger hold + styling), `[pause]`, `[pause:3s]` inline syntax |
| **Player Modes**      | Comfort (spatial + breathing), Focus (static & crisp), Presentation (larger, bold) |
| **Mirror Mode**       | Horizontal flip for camera-facing / mirror setups |
| **Customization**     | Live text size, leading, Compact HUD toggle |
| **Analytics**         | End screen: chunks, time, avg WPM, pacing consistency %, hesitations, slowest moment |
| **PWA + Offline**     | Full installable PWA, service worker v4 (network-first shells for updates), verified offline |
| **Haptics**           | Subtle vibration feedback on play, mode change, advance, etc. (where supported) |
| **Portable Core**     | `window.SpectorCore` exposed — chunking, timing, motion factory, analytics — designed for future SDK port |

**Keyboard:** Space / K = play/pause, R = rewind 3 chunks.

**Tap anywhere** (outside controls) to toggle playback.

---

## Cue Syntax Quick Reference

| Syntax              | Effect                                      |
|---------------------|---------------------------------------------|
| `**word or phrase**` | Visual emphasis + ~12% longer hold time    |
| `[pause]`           | ~2.8s pause chunk (or 1.8s mid-sentence)   |
| `[pause:3s]`        | Explicit N-second pause                    |

Cues are processed in `hybridChunkWithCues` and respected by `getMs()` timing.

---

## How It Compares to Meta's Current Teleprompter

| Aspect                    | Meta (today)                              | Spector                                      |
|---------------------------|-------------------------------------------|----------------------------------------------|
| Input                     | Paste in Meta AI app                      | Paste / .txt upload / saved library          |
| Pacing                    | Manual (Neural Band taps / swipe)         | Auto-adaptive + manual override              |
| Comfort / Presence        | Basic scroll or cards                     | Spatial anchoring + breathing/drift (Comfort) + haptics |
| Script reuse              | None                                      | Persistent library + one-tap launch          |
| Rehearsal feedback        | None                                      | Full analytics (pacing, hesitations, slowest) |
| Offline / Daily use       | Requires app connection                   | Full PWA install, offline shell              |
| Future glasses path       | In-app only                               | Modular SpectorCore ready for app store      |

**Primary use case for Ray-Ban Meta users today:** Use Spector on phone (non-Display Gen 1/2 or Display/HUD models) to perfect delivery before stepping in front of the camera or relying on the lighter in-app teleprompter. On Display models, the right-temple button/touchpad (and future Neural Band) can control script navigation when events are exposed.

---

## Quick Start (Phone or Desktop)

1. Open https://spectorlabs.io
2. Paste text, drop a `.txt`, or click one of the sample scripts
3. (Optional) Title it and **Save** to your library
4. Hit **Launch Teleprompter**
5. Choose mode (try Comfort), speed, and text size
6. Tap Play (or press Space / tap the screen)
7. (In Comfort) Move your head gently — the text responds with subtle spatial movement
8. When done, review your pacing, hesitations, and slowest chunk on the end screen

**On real glasses:**
Rehearse on phone with pro tools (library, auto-pacing, cues, analytics). Perform on glasses with the right-temple button (and future Neural Band gestures) for advance/pause.

Works on Ray-Ban Meta Display/HUD + Gen 1/2, and other brands (XREAL, Viture, etc.) via PWA.

See [TESTING.md](TESTING.md) for Developer Mode + "Add a Web App" on Ray-Ban Meta.

---

## Beta Program

The web player + PWA is fully live and usable today for phone rehearsal (install it, use the samples, try Comfort mode, etc.). We're recruiting testers with real smart glasses (Ray-Ban Meta Display, Gen 1/2, XREAL, Viture, Brilliant Labs, etc.) to validate the right-temple button, touch/gestures, Comfort spatial effects on actual HUD, and the complete flow.

**Hardware beta testers get:**
- Direct input on button and Neural Band mappings
- Early feedback loops on real-device experience
- Influence on glasses-specific features

Sign up via the form on the landing (powered by Formspree, endpoint configured, notifications to hello@spectorlabs.io) or email hello@spectorlabs.io directly.

---

## Source Code & Repository

The source is available on GitHub under the Spector-Labs organization: https://github.com/Spector-Labs/SPECTOR

**Repo status:** Public under the Spector-Labs org (https://github.com/Spector-Labs/SPECTOR). 

This makes the work visible to creators, hardware devs, and potential partners while keeping your personal profile clean. The live site (spectorlabs.io) + beta process + real hardware validation are the defensible "product" layer on top of the open code.

---

## For Developers & Future Smart Glasses

- `SpectorCore` is the pure logic layer: `chunk()`, `getMs()`, `buildRehearsalAnalytics()`, `createMotion()`, KalmanFilter, cue handling, etc.
- Fully testable (run `?test` on app.html or use the committed test harnesses in `tests/`).
- Zero dependencies. Static hosting only today.
- Designed to be portable to a glasses SDK / native wrapper when app stores open.

See `public/app.html` for the full implementation + in-browser tests (search for `runSpectorCoreTests`).

---

## Project Status & Roadmap

See [PROJECT.md](PROJECT.md) for detailed shipped items, verification status, and phased plan:

- **Phase 1 (now):** Beta test on real glasses, gather feedback, polish mirror + cues.
- **Phase 2:** Cue editor toolbar, analytics history/trends, section bookmarks, export/share.
- **Phase 3:** Onboarding flow, preset scripts, landing improvements (samples, install, demo video), Neural Band gesture mapping when exposed.
- **Phase 4:** App store founding developer (SpectorCore port, one-tap send to glasses, optional sync).

Explicit non-goals for now: native mobile binaries, accounts/backend, proprietary Bluetooth protocols, video recording.

---

## Development & Verification

- All changes should keep the single `public/` output dir (see `vercel.json`).
- Run the full verifier locally: `python tests/run_verification.py` (spins up http.server + exercises browser automation for PWA/SW/tests).
- In-browser core tests: visit `app.html?test` (expects "SpectorTest: ALL PASS").
- Service worker helpers: `sw-prime.html`, `verify-sw.html`.

---

## Assets & Branding

- Logo / wordmark: text "Spector™" (premium minimal).
- PWA icons: inline SVG "S" (192/512) in `manifest.json`.
- Early concept renders live in `assets/`. Real device screenshots and usage photos will be added after beta feedback.

---

## Contributing

This is early. Issues and PRs welcome once public. Focus areas right now: real-glasses feedback, cue authoring UX, analytics depth, and making the "why Spector" story instantly clear to new visitors.

---

## License & Disclaimer

*(License to be added in next commit — currently MIT intent for ecosystem friendliness.)*

Spector sells **teleprompter software only**. Not smart glasses, not Meta hardware, not affiliated with Meta Platforms, EssilorLuxottica, or Ray-Ban.

---

**Built for the moment before built-in HUD teleprompters become truly great.**

Live: https://spectorlabs.io
Status: [PROJECT.md](PROJECT.md)  
Testing on glasses: [TESTING.md](TESTING.md)  
Source: [github.com/Spector-Labs/SPECTOR](https://github.com/Spector-Labs/SPECTOR)

*Last updated: June 2026 (README refresh for visibility + education).*