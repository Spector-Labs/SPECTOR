# Spector — Go-Live Playbook

Everything left to take Spector from "deployed" to "getting users," in order.
Ticked items are already done in the codebase; unticked ones need **your**
accounts/logins (Google, a payment provider, your social handles) — no code.

---

## Status (done)

- [x] Live, honest landing + working player (the player CSS regression is fixed).
- [x] Re-heroed around **"one prompter, any glasses"**; competitive copy is accurate.
- [x] Real in-app demo on the site ("See it in action").
- [x] Lighthouse 90+ (desktop 100/95/96/100, mobile 98/95/96/100).
- [x] No-backend monetization rail wired (buttons show "coming soon" until you add URLs).
- [x] Per-device SEO pages: `/teleprompter-for-xreal`, `/teleprompter-for-viture`, `/ray-ban-meta-teleprompter`.
- [x] `sitemap.xml` + `robots.txt`.
- [x] Spector HUD overlay asset (`assets/spector-hud-overlay.svg` / `.png`) for branding video clips.

---

## 1. Turn on monetization (~15 min, no code from you)

1. Create a seller account — **[Lemon Squeezy](https://www.lemonsqueezy.com/)** recommended (merchant of record: handles global VAT + license keys).
2. Product: **"Spector Pro — Founding Supporter"**, one-time, ~**$34** (see [MONETIZATION.md](MONETIZATION.md) for the full pricing rationale).
3. Optional floor: enable **GitHub Sponsors** or a **Ko-fi** page.
4. In `public/index.html`, set the two constants near the top of the landing `<script>`:
   ```js
   const CHECKOUT_URL = 'https://YOURSTORE.lemonsqueezy.com/buy/XXXXXXXX';
   const SPONSOR_URL  = 'https://github.com/sponsors/hydrogenbondss';
   ```
   *(Paste these to me and I'll commit them, or edit + push yourself.)*

## 2. Get indexed by Google (~5 min, your login)

1. **search.google.com/search-console** → Add property → **URL prefix** `https://spectorlabs.io`.
2. Verify with the **HTML tag** method → paste me the `<meta google-site-verification>` snippet and I'll add it to the site; then click **Verify**.
3. **Sitemaps** → enter `sitemap.xml` → **Submit**.
4. **URL Inspection** → request indexing for each device page.

## 3. Launch for traffic (your accounts)

Post the drafts below. **Don't fire all three at once** — Show HN and Reddit do best when you're free to reply for the first hour. New Reddit account? Comment genuinely in the sub a few times first.

Recommended order over a week: **build-in-public teaser on X (day 1)** → **r/smartglasses (day 2–3)** → **Show HN (day 4, a weekday morning US time)**.

### Show HN
> **Title:** Show HN: Spector – Open-source teleprompter for smart glasses
>
> I built Spector, a free, open-source teleprompter aimed at smart glasses (Ray-Ban Meta, XREAL, Viture) that also works today on any phone or browser.
>
> The gap: glasses are selling fast, but there's almost no software for *speaking* on them. Meta's built-in prompter is manual and locked to its $799 Display; XREAL and Viture ship none. Spector is cross-brand — rehearse on your phone with adaptive, punctuation-aware pacing + `**emphasis**`/`[pause]` cues, then perform eyes-up on whatever glasses you have.
>
> Zero-dependency static PWA. The engine (hybrid chunking, adaptive timing, a Kalman-filtered "comfort" spatial mode off device orientation, post-run pacing analytics) is ~1k lines of vanilla JS with an in-browser test harness. No accounts, nothing uploaded.
>
> Live: https://spectorlabs.io · Code: https://github.com/hydrogenbondss/SPECTOR
>
> Would love feedback — especially from anyone with real glasses on how the on-lens reading feels.

### r/smartglasses
> **Title:** I made a free, open-source teleprompter that works on any smart glasses (XREAL, Viture, Ray-Ban Meta)
>
> I kept hitting the same wall: the glasses are here, but to actually *read a script* on them, XREAL and Viture ship no teleprompter, and Meta's is manual + locked to the $799 Display. So I built **Spector** — free, open source, cross-brand.
>
> Rehearse on your phone (adaptive pacing that speeds/slows with punctuation, emphasis/pause cues, pacing stats after each run), then perform eyes-up on whatever glasses you've got. No account, nothing uploaded, no watermark.
>
> Live in any browser: https://spectorlabs.io · Open source: https://github.com/hydrogenbondss/SPECTOR
>
> Genuinely after feedback from people who own glasses — does the reading experience hold up on your device? What's missing?

### X — build-in-public thread
> **1/** Smart glasses are selling millions of units. The software for *speaking* on them barely exists. So I built Spector — a free, open-source teleprompter for **any** smart glasses. 🧵
>
> **2/** Meta's built-in prompter is manual + locked to its $799 Display. XREAL and Viture ship none. Every option is single-brand. Spector works across all of them — and on your phone today.
>
> **3/** Rehearse on your phone with adaptive pacing (speeds up/slows with punctuation), drop in **emphasis** and [pause] cues, then perform eyes-up. No glancing down, no script-face.
>
> **4/** Zero-dependency PWA. No account, nothing uploaded — scripts stay in your browser. Fully open source, free core forever.
>
> **5/** After each run: pacing consistency, hesitations, your slowest moment. A rehearsal *coach*, not just a scroller.
>
> **6/** Try it (any browser): https://spectorlabs.io · code: https://github.com/hydrogenbondss/SPECTOR — building in public, feedback welcome, especially if you own glasses. 👓

---

## 4. SEO follow-through (once indexed)

- Add more long-tail device pages as demand shows (Rokid, Even Realities, Brilliant Labs) using the existing three as a template.
- Embed a short demo clip on each device page once you have one.
- Watch Search Console for which "teleprompter for X" queries land, and lean into the winners.

## 5. Metrics to watch (first 30 days)

- Enable **Vercel Web Analytics** in the Vercel dashboard (the script tag is already on the site).
- Track: visits → "Launch teleprompter" clicks → beta signups → founding-supporter purchases.
- The key early signal: do people who try it come back? Retention beats raw traffic.

---

*The product side is in good shape. From here, traction is a distribution problem — SEO pages + honest posts + real-glasses feedback. Everything above marked "your login" is a few minutes each; hand me any URLs/snippets and I'll wire them in.*
