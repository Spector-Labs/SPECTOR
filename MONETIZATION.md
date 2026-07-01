# Spector — Monetization

How Spector makes money, and how to switch it on. The guiding rule: **the open-source
core stays free forever**; money comes from *hosted / account value* layered on top
(sync, history, support), never from gating the code itself.

> You do **not** need Meta, an app store, or a backend to get paid. Spector is a web
> app — you sell through a normal web checkout that pays out to your bank.

---

## How the money reaches you

1. A visitor clicks **Become a founding supporter** on the landing (`#support`).
2. They land on a checkout hosted by your payment provider (Lemon Squeezy / Gumroad / Stripe).
3. The provider charges the card and **deposits the money in your bank** on a payout schedule, minus their fee (~5% + processing).
4. The provider emails the buyer a **license key**.
5. They paste the key into the "Activate Pro" box; the app stores it and flips Pro on (localStorage).

No server of yours is required for the MVP. When you outgrow it, add a thin backend to validate keys server-side.

---

## Switch it on (≈30 minutes)

The buttons are already wired and ship in a safe "coming soon" state until you add URLs.

1. **Create a seller account.** Recommended: **[Lemon Squeezy](https://www.lemonsqueezy.com/)** — it's a *merchant of record*, so it handles global VAT/sales tax and license keys for you (a big deal for a solo seller). Alternatives: Gumroad (simplest), Stripe Payment Links (lowest fees, but you handle tax/keys).
2. Create a product: **"Spector Pro — Founding Supporter"**, one-time, ~**$34**. Enable **license keys**.
3. In [`public/index.html`](public/index.html), set the two constants near the top of the landing `<script>`:
   ```js
   const CHECKOUT_URL = 'https://YOURSTORE.lemonsqueezy.com/buy/XXXXXXXX';
   const SPONSOR_URL  = 'https://github.com/sponsors/hydrogenbondss'; // or a Ko-fi link
   ```
4. Commit, push, deploy. Done — the "Become a founding supporter" button now opens checkout, and pasted keys activate Pro.

### Optional: real key validation
The MVP accepts any well-formed key locally (see the `NOTE` in `initSupport()`). To actually enforce, validate before storing — Lemon Squeezy exposes a browser-callable endpoint:
```js
const res = await fetch('https://api.lemonsqueezy.com/v1/licenses/validate', {
    method: 'POST',
    headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
    body: JSON.stringify({ license_key: key })
});
const data = await res.json();
if (data.valid) { localStorage.setItem('spector_pro', key); }
```
This is fine for the browser (the endpoint is designed for it). It's not piracy-proof — a determined user can bypass client-side checks — but that's an acceptable trade for a supporter-oriented v1.

---

## Pricing

| Offer | Price | When |
|-------|-------|------|
| **Free core** | $0 | Now, forever — full teleprompter, Comfort mode, cues, analytics, PWA |
| **Founding supporter (lifetime Pro)** | ~$34 one-time | Now — funds the build, unlocks all future Pro |
| **Donations** | any | Now — GitHub Sponsors / Ko-fi as a floor |
| **Pro subscription** | ~$6/mo or ~$48/yr | Later — once a real Pro feature + traffic exist |

Founding beta hardware testers get Pro free for life (already promised on the landing) — honor that; sell the founding tier to everyone else.

---

## Free vs Pro (proposed split)

Keep the free tier genuinely useful; Pro is *extras*, not a paywall on the basics.

- **Free:** paste/upload scripts, all player modes, Comfort spatial, cue markers, end-of-run analytics, local library (cap ~20), PWA/offline.
- **Pro (as it ships):** cloud sync across devices, unlimited saved scripts, rehearsal **history & pacing trends**, script + stats **export/share**, priority input on glasses features.

None of the Pro features are built yet — that's deliberate. Don't build the subscription backend until traffic shows people want it.

---

## Other revenue (secondary)

- **Glasses affiliate:** Ray-Ban Meta / XREAL / Viture referral links, clearly disclosed. Modest, fast to add, mild tension with the "not a retailer" line — keep it honest.
- **Niche B2B / creator wedge:** a "team" or "pro creator" tier sold to people who present for a living (realtors, sales, YouTubers, keynote coaches). Higher price, but it's outreach, not a button.
- **App-store founding developer:** when/if Meta opens its glasses app store, that's an extra channel (Meta would take ~30%). Future upside, not near-term cash.

---

## The honest bottleneck

Revenue is gated by **traffic**, not payment mechanics. A real demo video + posting it to smart-glasses and creator communities will do more than any pricing tweak. Set the money rail up once (it's cheap), then spend your effort on distribution.

---

*Config lives in `public/index.html` (`CHECKOUT_URL`, `SPONSOR_URL`). This doc and that code should move together.*
