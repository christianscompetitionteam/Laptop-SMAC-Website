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

- **Lead form**: the "Request more information" form on the homepage has
  no backend yet. It currently opens the visitor's email client with the
  details pre-filled (see `assets/js/main.js`). Wire it to your CRM
  (e.g. SparkMembership) or an email service when ready.
- **Privacy Policy / Terms of Service**: `privacy.html` and `terms.html`
  are placeholders, not real legal text — replace them with your actual
  policies before launch.
- **FAQ answers**: two FAQ answers on the homepage ("Will my child become
  a bully?" and "How do I claim your limited time offer?") are copied
  verbatim from the previous site. The other five are newly written in
  the same voice and should be reviewed for accuracy.
- **Images**: this build ships without photography (none was available
  while building). The design currently relies on typography, color, and
  layout rather than photos — drop real photos of the facility, classes,
  and instructors into `assets/img/` and reference them in `build/build.py`
  whenever you're ready.
- **Blog**: no blog content was migrated. `blog.html` is a holding page
  that points to Facebook/Instagram in the meantime.
