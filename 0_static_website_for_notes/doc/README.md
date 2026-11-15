# Static Course Website Bundle

This folder contains a reusable copy of the static course website source:

- `index.html` — responsive course page, file search, and in-browser readers
- `learn.html` — searchable sidebar lesson reader for modules and notebooks
- `catalog.json` — generated file listing for this repository
- `scripts/build_catalog.py` — builds the file catalog from the parent repository
- `tests/test_build_catalog.py` — tests for natural sorting and catalog generation
- `deployment/pages.yml` — GitHub Pages workflow template
- `static_website_prompt.md` — reusable prompt for future course websites

The active site at the repository root remains unchanged. This copy is configured to read the course files from the parent repository.

## Preview this copy

Run these commands from the repository root:

```powershell
python doc/scripts/build_catalog.py
python -m http.server 8000
```

Open `http://localhost:8000/doc/`. The in-browser reader needs the site to be served over HTTP; opening the HTML with a `file://` URL may block catalog and course-file requests.

Run the focused tests from the `doc` folder:

```powershell
cd doc
python -m unittest discover -s tests -v
```

## Files and deployment

The catalog generator scans the parent repository recursively, omits hidden files and editor lock files, and sorts names naturally so Module 2 comes before Module 10. Rerun it after adding or removing files.

`deployment/pages.yml` is a template, not an active workflow at this nested path. To use the workflow for a separate course-site repository, copy it to `.github/workflows/pages.yml` at that repository's root and keep the catalog generator at `scripts/build_catalog.py`. GitHub Pages only discovers workflows in the repository-root `.github/workflows/` folder.

Notebook code is displayed but never executed. DOCX and PPTX previews are processed in the browser using version-pinned libraries loaded from CDNs; an internet connection is required. Legacy `.doc` and `.ppt` files must be converted to `.docx` and `.pptx`. PPTX slides are previews, so animations and complex formatting may differ from PowerPoint.

See [`static_website_prompt.md`](./static_website_prompt.md) for the reusable build prompt.
