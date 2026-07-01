# Spector — Brand Guidelines

The single source of truth for how Spector looks and sounds. These values are
the ones actually implemented in `public/style.css` (`:root` design tokens) and
across the landing + player — keep this doc and the CSS in lock-step.

> Spector sells **teleprompter software only**. Not smart glasses, not Meta
> hardware. Not affiliated with Meta Platforms, EssilorLuxottica, or Ray-Ban.

---

## 1. Name & wordmark

- **Name:** Spector (stylized `Spector™` in product UI; `SPECTOR` in the nav
  wordmark and repo).
- **Tagline:** **Eyes Forward.** — "Forward" is set in the accent purple.
- **One-liner:** *The auto-paced teleprompter built for smart glasses. Rehearse
  on your phone, perform on glasses.*
- Always write **Spector**, never "the Spector app" or "Spector Labs product."
  Footer entity line: `© Spector Labs`.

---

## 2. Color

Dark-first. Black canvas, white text, a single purple accent. No second accent.

### Core tokens (`:root`)

| Token | Hex / value | Use |
|-------|-------------|-----|
| `--bg` | `#000000` | Page background |
| `--bg-elevated` | `#0A0A0A` | Cards, panels |
| `--bg-card` | `#080808` | Nested/inset surfaces |
| `--text` | `#FFFFFF` | Primary text, active teleprompter line |
| `--text-muted` | `#A1A1AA` | Secondary copy |
| `--text-dim` | `#71717A` | Labels, captions, metadata |
| `--accent` | `#7C3AED` | Primary purple — CTAs, links, emphasis |
| `--accent-hover` | `#6D28D9` | Hover / gradient end |
| `--accent-subtle` | `rgba(124,58,237,0.10)` | Tinted fills |
| `--accent-glow` | `rgba(124,58,237,0.25)` | Focus glow, shadows |
| `--border` | `#1A1A1A` | Hairline borders |
| `--border-hover` | `#2A2A2A` | Border on hover |
| Light purple | `#A78BFA` | Active button labels, end-screen headings, stat values |

### Rules

- **One accent only.** Purple (`#7C3AED`). The lighter `#A78BFA` is a tint of
  it for active states — not a separate brand color.
- The **active reading line** in the player is white (`--text`) for maximum
  legibility; purple is reserved for emphasis, glow, and controls.
- Success/confirmation uses green (`#22c55e`) sparingly (beta form only).
- Never introduce warm/tan tones — an earlier iteration used a beige accent
  (`rgba(232,213,183,…)`); it has been fully retired. If you see it, it's a bug.

---

## 3. Typography

- **Typeface:** [Inter](https://fonts.google.com/specimen/Inter) — weights
  `400, 500, 600, 700, 900`. System fallback:
  `system-ui, -apple-system, sans-serif`.
- **Hero headline:** heavy (900), tight tracking (`letter-spacing: -0.03em`).
- **Body:** 400–500, `--text-muted` for secondary copy.
- **Teleprompter chunk:** `--chunk-size: 31px`, `--chunk-leading: 1.55`
  (user-adjustable 22–42px / 1.3–2.0 in the player).
- Numbers in the player (timer, stats) use `font-variant-numeric: tabular-nums`.

---

## 4. Shape, depth & motion

- **Radii:** `--radius: 16px`, `--radius-lg: 24px`, `--radius-pill: 9999px`
  (all buttons/chips are pills).
- **Surfaces:** subtle glassmorphism — low-opacity white fills
  (`rgba(255,255,255,0.03–0.08)`) with `backdrop-filter: blur()`.
- **Easing:** `--transition-smooth: cubic-bezier(0.23, 1, 0.32, 1)` for the
  premium settle; 0.2–0.25s for hovers.
- **Motion is meaningful, not decorative:** scroll reveals on the landing;
  Comfort-mode breathing/drift + Kalman-smoothed spatial anchoring in the player.
- Always respect `prefers-reduced-motion` (already wired in CSS + JS).

---

## 5. Feel & voice

- **Feel:** premium, calm, editorial. Confident but honest — no vanity metrics,
  no fake screenshots. "Early, live, and open."
- **Voice:** direct, second-person, short sentences. Lead with the benefit
  ("Eyes up, no script-face"), not the mechanism.
- **Haptics + audio:** subtle vibration and a soft click on interaction give the
  "liquid glass" tactile feel — keep them understated.

---

## 6. Assets

- **Logo mark:** `public/images/logo-mark.png` (nav) · app icon
  `public/images/app-icon.png` · favicon `public/favicon.ico`.
- **PWA icons:** defined in `public/manifest.json`.
- **Social/OG card:** `public/images/og-card.png` (1200×630).
- **Theme color:** `#000000` (`<meta name="theme-color">`).

---

*Derived from `public/style.css`. When you change a token there, update this
file in the same commit.*
