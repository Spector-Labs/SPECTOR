#!/bin/bash
#
# SPECTOR Domain Migration Helper
# Run this when you have acquired the new domain (e.g. spector.com or spector.app)
#
# Usage:
#   ./scripts/migrate-domain.sh spector.com
#   or
#   NEW_DOMAIN=spector.app ./scripts/migrate-domain.sh
#
# What it does:
# - Replaces all occurrences of the old temporary Vercel URL with the new domain.
# - Updates badges, links, docs, examples, and verification references.
# - Leaves a note for manual steps (Vercel custom domain, DNS, redirects, re-deploy).
#
# IMPORTANT:
# - Run from the repo root.
# - Review the diff before committing.
# - After running, update Vercel project to add the custom domain and set up DNS records.
# - Set up a 301 redirect from old domain → new domain (can be done in Vercel).
# - Re-deploy and test thoroughly (PWA install, offline, player launch, ?test, glasses web app flow).
# - Update external references (GitHub repo settings, any socials, etc.).
#
# Recommended new domain: spector.com (premium) or spector.app (tech feel).
# Buy both if possible for protection.

set -e

OLD_DOMAIN="spector-plum.vercel.app"
NEW_DOMAIN="${1:-${NEW_DOMAIN:-spector.com}}"

if [[ "$NEW_DOMAIN" == "$OLD_DOMAIN" ]]; then
  echo "Error: NEW_DOMAIN cannot be the same as OLD_DOMAIN"
  exit 1
fi

echo "Migrating from $OLD_DOMAIN → $NEW_DOMAIN ..."

# Files that commonly contain the old URL (docs + code)
FILES=(
  "README.md"
  "TESTING.md"
  "PROJECT.md"
  "DOMAIN.md"
  # Add more if needed (e.g. any other .md, .html, .json)
)

for file in "${FILES[@]}"; do
  if [[ -f "$file" ]]; then
    echo "Processing $file..."
    # Use portable sed (works on macOS + Linux)
    sed -i.bak "s|${OLD_DOMAIN}|${NEW_DOMAIN}|g" "$file"
    rm -f "${file}.bak"
  else
    echo "Warning: $file not found, skipping."
  fi
done

echo ""
echo "Replacements done for $OLD_DOMAIN → $NEW_DOMAIN in the listed files."
echo ""
echo "NEXT MANUAL STEPS (do these after running the script):"
echo "1. git diff   # review all changes"
echo "2. Update your Vercel project:"
echo "   - Add custom domain $NEW_DOMAIN (and www if desired)"
echo "   - Follow Vercel's DNS instructions (usually CNAME to cname.vercel-dns.com)"
echo "   - Wait for SSL/propagation"
echo "   - Set $NEW_DOMAIN as the primary domain"
echo "3. (Recommended) Configure redirect: old domain → new domain (301)"
echo "   - Can be done via Vercel 'Redirects' or registrar"
echo "4. git add -A && git commit -m 'chore: migrate from spector-plum.vercel.app to $NEW_DOMAIN'"
echo "5. git push"
echo "6. Trigger re-deploy on Vercel (or let GitHub integration do it)"
echo "7. Full smoke test:"
echo "   - Landing page loads cleanly"
echo "   - Samples + demo video work"
echo "   - Launch player, Comfort mode, hardware note visible"
echo "   - PWA install prompt"
echo "   - Offline (sw-prime.html / verify-sw.html)"
echo "   - app.html?test passes"
echo "   - TESTING.md examples updated"
echo "8. Update any external links (GitHub repo 'Website' field, social profiles, etc.)"
echo "9. Update 'spector.com coming soon' notes to remove or change to 'Now at spector.com'"
echo ""
echo "After this, the product will feel much more 'real' and ready for beta outreach on real hardware."
echo ""
echo "See DOMAIN.md for the full acquisition + post-purchase playbook (including beta program and hardware testing focus on the button/gestures)."