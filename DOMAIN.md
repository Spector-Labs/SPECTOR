# Spector Domain Acquisition & Migration Checklist

**Goal:** Move from temporary `spector-plum.vercel.app` to `spector.com` (or `spector.app`) for professional branding, SEO, and trust.

## 1. Before You Buy (This Week)
- Search trademark databases (USPTO, EUIPO, etc.) for "Spector" in software, productivity, or wearable categories. Consider "Spector Teleprompter" or similar.
- Check social handles (@spector, spector.app on X/Instagram/TikTok).
- Decide primary domain: `spector.com` (premium) or `spector.app` (tech feel). Buy both + common misspellings if budget allows.
- Verify the seller (avoid aftermarket scams).

## 2. Purchase
- Recommended registrars: Namecheap, Google Domains (if available), Porkbun, or direct via a broker for premium .com.
- Enable auto-renew + privacy protection.
- Buy for 2-5+ years minimum.

## 3. DNS & Hosting Setup (Vercel)
1. Log into Vercel dashboard → your "spector" project.
2. Go to Domains → Add `spector.com` (or .app).
3. Follow the exact instructions Vercel gives:
   - Usually add a CNAME record (e.g., `cname.vercel-dns.com` or similar).
   - Or A/AAAA records for apex domain.
4. Wait for propagation (minutes to 48h). Vercel will issue SSL automatically (Let's Encrypt).
5. Set as Primary domain in Vercel.
6. (Optional) Set up redirect: old `spector-plum.vercel.app` → new domain (301) in Vercel or registrar.

## 4. Update All References in Code & Docs (Critical — Do Before or Immediately After DNS)
Search the entire repo for the old domain and update:

**Must update:**
- `public/index.html`: meta description, any links, title if needed.
- `public/app.html`: any references.
- `public/manifest.json`: `start_url` if absolute.
- `README.md`: all badges, links, "Try it instantly", Quick Start, etc.
- `TESTING.md`: all URLs and "Current Live Version".
- `PROJECT.md`: Live URL, deployment checks, contact links.
- Any other mentions (e.g., in tests, sw files if absolute).

**Example search:**
```bash
grep -r "spector-plum.vercel.app" . --include="*.md" --include="*.html" --include="*.json"
```

After updates:
- `git commit && git push`
- Trigger redeploy on Vercel (or it auto-deploys from main).

Also update:
- GitHub repo description, website URL in settings.
- Any external links (LinkedIn, personal site, future press).

## 5. Post-Migration
- Test thoroughly: landing, player launch, PWA install, offline (via sw-prime/verify).
- Update badges in README (change live link).
- Announce: Tweet / post the new domain + "now at spector.com".
- Consider:
  - Email: Forward `hello@spector.com` or set up Google Workspace / custom email.
  - Analytics: Add simple privacy-friendly tracking (Plausible, Fathom) if desired for funnel data.
  - Make GitHub repo public (if not already) for credibility.
  - Update TESTING.md with new domain for beta testers.
- Monitor: Vercel logs, uptime, any broken links.

## 6. "And Then What?" (Product Roadmap Tie-in)
Acquiring the domain is a strong signal of commitment. Immediate next:
- **Branding refresh**: Professional logo (beyond text "S"), favicon updates, perhaps custom illustrations (use the demo visuals we have as base).
- **Launch prep**: 
  - Public GitHub + CONTRIBUTING.
  - Beta landing page or waitlist form (simple Google Form or Typeform for now).
  - Real hardware testing campaign (recruit Ray-Ban Meta Display + other glasses owners via Reddit, X, creator communities).
- **Ecosystem play**:
  - Update copy to emphasize "works across Ray-Ban Meta Display, Gen 1/2, XREAL, Viture, and future glasses" + hardware button/gesture support.
  - Prepare SpectorCore porting guide for when app stores open.
- **Monetization / sustainability**: Free core PWA forever? Premium features (cloud sync, advanced analytics, plugin marketplace) behind paywall once accounts are added. Or "founding supporter" model.
- **Metrics & iteration**: Instrument basic events (sample used, Comfort tried, end screen reached, install clicked). Watch for drop-off at "first Comfort wow".
- **Meta angle (internal note)**: With a real domain and polished experience, SPECTOR becomes a credible "reference implementation" showing what a great rehearsal + HUD teleprompter layer looks like. Use it to inform whether Meta should:
  - Build equivalent (or better) native features into the Meta AI app / glasses OS.
  - Open more APIs sooner (button events, Neural Band, HUD text rendering) to enable great third-party experiences like this.
  - Feature or partner with high-quality apps.

## 7. Risks & Tips
- Domain squatting: Act fast if you decide.
- SEO: Old Vercel URLs will lose juice — set up proper redirects.
- Cost: Domain ~$10-100+/yr depending on .com premium; hosting on Vercel free tier is fine for PWA.
- Legal: The current "Spector™" claim in UI — ensure you own or have rights to the mark in your jurisdictions.

**Suggested immediate action if buying next week:**
1. Buy domain.
2. Add to Vercel + configure DNS.
3. Create a branch or PR with all URL updates + this DOMAIN.md.
4. Deploy to new domain + test end-to-end on real glasses.
5. Announce + start recruiting 10-20 beta testers specifically on Display hardware (ask about button usage, HUD readability, gesture ideas).

This turns the domain into a real brand asset and accelerates the "founding dev ready" positioning.

---

*Last updated with hardware controls & multi-brand clarifications (June 2026).*

Contact / questions: Update as needed.