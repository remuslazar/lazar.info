# lazar.info

Source of https://lazar.info, served by GitHub Pages.

- `index.html`, `404.html`: the site, plain static HTML.
- `.github/workflows/pages.yml`: deploys on push and every 6 hours.
  Each run writes `posts.json` from the Medium feed (`scripts/fetch_posts.py`),
  which `index.html` renders.
- `.well-known/appspecific/com.tesla.3p.public-key.pem`: public key for the
  Tesla Fleet API (Home Assistant). Tesla's developer app and Home Assistant
  depend on this exact URL. Do not move or rename it.
