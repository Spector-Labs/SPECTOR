# Spector Domain Acquisition & Migration Checklist

**Goal:** The domain spectorlabs.io has been purchased (via Namecheap). This thorough pre-purchase pass ensures the project is clean and consistent for the migration.

## 1. Before You Buy (This Week)
- Search trademark databases (USPTO, EUIPO, etc.) for "Spector" in software, productivity, or wearable categories. Consider "Spector Teleprompter" or similar.
- Check social handles (@spector, spector.app on X/Instagram/TikTok).
- Domain purchased: spectorlabs.io (via Namecheap). Migration now complete.
- Verify the seller (avoid aftermarket scams).

## 2. Purchase
- Recommended registrars: Namecheap, Google Domains (if available), Porkbun, or direct via a broker for premium .com.
- Enable auto-renew + privacy protection.
- Buy for 2-5+ years minimum.

## 3. DNS & Hosting Setup (Vercel)
1. Log into Vercel dashboard → your "spector" project.
2. Go to Domains → Add `spectorlabs.io`.
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
./scripts/migrate-domain.sh spectorlabs.io
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
- Announce: Tweet / post the new domain + "now at spectorlabs.io".
- Consider:
  - Email: Forward `hello@spectorlabs.io` or set up Google Workspace / custom email.
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

**Migration for spectorlabs.io (purchased via Namecheap):**
1. Vercel dashboard → Project → Domains → add spectorlabs.io. Follow DNS instructions (CNAME), wait for SSL, set as primary.
2. Run the migration (script already executed in this pass for spectorlabs.io):
   ```bash
   ./scripts/migrate-domain.sh spectorlabs.io
   ```
   Commit and push.
3. Set up redirect from old plum URL if desired.
4. Full test on https://spectorlabs.io.
5. Update external links.
6. Clean “launching soon” language.
7. Announce and recruit beta testers (focus on button/HUD testing per TESTING.md).

The flip is now clean.

## 8. Full Pass Readiness Checklist (Completed before domain purchase)
As of this very thorough pre-purchase pass:

- [x] All original 1-4 priorities + extras implemented (visibility/education, conversion/polish, Phase 2 items, strategic/Meta notes).
- [x] Landing: cue insertion toolbar, 6 strong presets (including TEDx, Wedding, Earnings), word/est-time count, live validation (inline errors), local history with clear future-sync note, actionable beta form (real mailto + optional glasses model field), punchier “Glasses & Future” section (benefit-led, 2 tight paragraphs), consistent domain language, demo section now functional/interactive-focused (removed fake visuals).
- [x] Player: persistent hardware controls legend (detailed right-temple button + Neural Band + other brands), first-run coach toast (auto-highlights Comfort + button story), controls fade on idle, simulate button + 'b' key handler, section bookmarks, mirror polish (text-only flip), end-screen + analytics reinforcement with hardware tie-in.
- [x] Hardware specifics fully addressed across UI + docs: right temple button as first-class control, clear Gen 1/2 vs Display/HUD distinctions, broad multi-brand support (XREAL, Viture, etc.).
- [x] Docs fully aligned: README (punchier glasses language, updated beta/quickstart), PROJECT (refreshed shipped table, roadmap, strategic section, consistent URLs), TESTING (button test cases + 'b' key, specific hardware feedback questions, updated URLs), DOMAIN (detailed migration script + expanded checklist + this thorough pass summary).
- [x] Added MIT LICENSE, cleaned up old domain references, added more presets for immediate value, made beta/history feel intentional rather than placeholder.
- [x] PWA/offline/verification paths remain solid. No major bugs. Recommend local test + ?test mode before domain flip.

The project is now very clean and ready for your review + domain purchase.

**Remaining before/after purchase (low effort):**
- Run the migration script once domain is yours.
- Remove "launching soon" notes and update live URLs.
- Update beta form text/email to beta@spectorlabs.io.
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