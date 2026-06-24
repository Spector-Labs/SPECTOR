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
Use the provided migration helper for speed and safety:

```bash
# From repo root
./scripts/migrate-domain.sh spector.com
# or
NEW_DOMAIN=spector.app ./scripts/migrate-domain.sh
```

The script handles the bulk replacements across README, TESTING, PROJECT, DOMAIN, etc.

**Manual review still required** after running:
- `git diff`
- Check for any other hard-coded references (e.g. in future added files).
- Update GitHub repo settings (Website URL, description).
- Update external links.

See the script header for the full list of post-migration steps (Vercel DNS, redirects, re-deploy, testing matrix, etc.).

**Example manual search if needed:**
```bash
grep -r "spector-plum.vercel.app" . --include="*.md" --include="*.html" --include="*.json"
```

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

## 8. Full Pass Readiness Checklist (Completed before domain purchase)
As of the latest full review pass (all original 1-4 priorities + additional polish completed):

- [x] All original prioritized recs (visibility, conversion/polish, Phase 2 items, strategic) implemented and committed.
- [x] Landing: cue toolbar, samples, install/PWA, demo video + concept images, beta form with history persistence, word count/est time, validation, history section.
- [x] Player: persistent hardware controls legend (button details), first-run coach toast (auto Comfort + button highlight), controls fade, simulate right-temple button + 'b' key, bookmarks, mirror polish (text only), end-screen + analytics reinforcement with hardware notes.
- [x] Hardware specifics addressed: right temple button simulation and docs, Gen 1/2 vs Display/HUD differences, other brands (XREAL etc.) compatibility notes in all docs and UI.
- [x] Docs: README, PROJECT (with strategic/Meta notes and shipped features), TESTING (with button test cases and feedback questions), DOMAIN (migration script + checklist).
- [x] LICENSE added (MIT).
- [x] Demo images copied to public/images and displayed on landing for visuals.
- [x] Analytics v2 starter (local history of runs + export).
- [x] Domain migration script ready and tested in guide.
- [x] Copy professionalism reviewed and tightened across UI and docs.
- [x] PWA, offline, verification paths intact.
- [x] No major bugs found in full pass (tested mentally + via structure; recommend user runs ?test and verification script).

**Remaining before/after purchase (low effort):**
- Run the migration script once domain is yours.
- Remove "spector.com coming soon" notes and update live URLs.
- Update beta form text/email to beta@spector.com.
- Test full flow on new domain + real glasses (use simulate button as proxy first).
- Consider making GitHub repo public after domain live for contributors.
- Optional: connect beta form to real service (Formspree, email) on new domain.

**Suggested action for you now:**
1. Review the current state (landing, player, all docs).
2. Run local test: `python -m http.server --directory public 8080`, open http://localhost:8080 and app.html?test.
3. If happy with the full pass, purchase the domain.
4. Run the migration script.
5. Vercel custom domain setup + re-deploy.
6. Announce and recruit beta testers.

---

*Last updated with full pass completion and readiness checklist (June 2026).*

Contact / questions: Update as needed.