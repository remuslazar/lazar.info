# lazar.info

Source of https://lazar.info, served by GitHub Pages.

- `index.html`, `404.html`: the site, plain static HTML.
- `.github/workflows/pages.yml`: deploys on push and every 6 hours.
  Each run writes `posts.json` from the Medium feed (`scripts/fetch_posts.py`),
  which `index.html` renders.
  GitHub disables the 6-hourly schedule of a public repository after 60
  days without activity; re-enable it under *Actions* or push a commit.
- `.well-known/appspecific/com.tesla.3p.public-key.pem`: public key for the
  Tesla Fleet API (Home Assistant). Tesla's developer app and Home Assistant
  depend on this exact URL. Do not move or rename it.

The code is MIT licensed (`LICENSE`). The texts on the page are
© Remus Lazar and not covered by that license.
