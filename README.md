# Scottsdale Martial Arts Center — website

A static, framework-free site for SMAC. No build step is required to host
it — every `.html` file at the repo root and under `programs/` is ready to
deploy as-is (GitHub Pages, Netlify, S3, etc.).

## Structure

- `index.html`, `about.html`, `schedule.html`, `events.html`, `blog.html`,
  `client-info-media.html`, `privacy.html`, `terms.html` — top-level pages.
- `programs/` — one page per program (preschool through weapons), plus a
  `programs/index.html` overview.
- `assets/css/styles.css` — the whole design system (colors, type, layout).
- `assets/js/main.js` — mobile nav toggle and the trial-request form.
- `build/build.py` — the generator. All page copy lives here as plain
  Python data (`PROGRAMS`, `INSTRUCTORS`, `FAQS`, `WEEKLY_SCHEDULE`, etc.),
  rendered through small template functions into the `.html` files above.

## Editing content

Don't hand-edit the generated `.html` files — edit `build/build.py`
(or `assets/css/styles.css` / `assets/js/main.js`) and regenerate:

```
python3 build/build.py
```

That rewrites every page from the shared header/nav/footer + the content
tables at the top of the script, so a nav or footer change only needs to
happen once.

## Notes for the site owner

- **Lead form**: the "Request more information" form on the homepage is
  marked up to work automatically the moment this site is hosted on
  Netlify (`data-netlify="true"` + a hidden `form-name` field — Netlify
  Forms needs nothing else, and submissions land in your Netlify
  dashboard and can be emailed to you). On any other host, or until then,
  it falls back to opening the visitor's email client with the details
  pre-filled, so a submission is never silently lost. See
  `assets/js/main.js` (`initLeadForm`). To use a different backend
  (Formspree, a CRM endpoint, etc.), change the form's `action` in
  `build/build.py` — the fetch-then-fallback logic works unchanged.
- **Privacy Policy / Terms of Service**: `privacy.html` and `terms.html`
  are placeholders, not real legal text — replace them with your actual
  policies before launch.
- **FAQ answers**: two FAQ answers on the homepage ("Will my child become
  a bully?" and "How do I claim your limited time offer?") are copied
  verbatim from the previous site. The other five are newly written in
  the same voice and should be reviewed for accuracy.
- **Blog**: `blog.html` plus six posts under `blog/` are new, original
  content written for this site (not migrated from anywhere) — factual
  claims lean on the real bios/schedule already in `build/build.py`, but
  it's still worth a read-through before publishing.
- **Images — action needed**: this build references six placeholder
  images that still need to be added to `assets/img/`:
  `hero-kick.png`, `facility-floor.png`, `belt-knot.png`,
  `kids-silhouette.png`, `weapons-rack.png`, `jujutsu-grapple.png`.
  These are generic, non-identifying AI-generated mood shots (no real
  people, no real signage) generated for this build — this environment's
  network policy blocked downloading them into the repo automatically,
  so grab them from the chat where they were shown and drop them in with
  those exact filenames, or swap in your own real photography using the
  same filenames. Everything (program pages, About, Schedule, the blog)
  is already wired to display them at those paths — no code changes
  needed once the files exist. Cards/banners fall back to a plain
  parchment-colored box if an image is missing, so nothing breaks in the
  meantime.
