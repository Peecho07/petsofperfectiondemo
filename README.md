# Pet Perfection Site

Demo redesign of petsofperfection.com (Pets of Perfection, Boynton Beach, FL), built by tsKaizen.
Plain HTML, CSS and JS. No frameworks, no build step needed to host.

## Pages
Home · Services · Cats · About · Gallery · Reviews · FAQ · Privacy & SMS Policy · Book · 404

## Deploy on GitHub Pages
1. Create a repo named `pet-perfection-site` under Peecho07.
2. Upload everything in this folder to the repo root (index.html must be at the root).
3. Settings > Pages > Deploy from branch > `main` / `(root)`.
4. Live at `https://peecho07.github.io/pet-perfection-site/`.

Netlify works too: drag the folder in, publish directory = root.

## Editing
- **Prices, services, copy, reviews, contact info:** edit the top of `tools/build.py`, then run `python3 tools/build.py`. It rewrites every page.
- **Booking form email + hours logic:** `js/config.js`. Paste a Formspree endpoint into `FORM_ENDPOINT`. Left empty, the form runs in demo mode (validates and shows the success screen but sends nothing).
- **Styles:** `css/style.css`. Colors are tokens at the top.

## Notes
- All prices are SAMPLES for the demo. See AUDIT.md for the full pre-launch checklist.
- Respects reduced-motion settings, keyboard navigation and screen readers.
