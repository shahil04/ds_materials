# Python Learning Path

A free, self-paced Python tutorial built from this repository's course notes, Jupyter notebooks, exercises, and project resources. The homepage brings the material together in a guided path from the fundamentals to advanced topics and app frameworks.

## View the website

Run these commands from the repository root to preview the site locally:

```powershell
python scripts/build_catalog.py
python -m http.server 8000
```

Then open `http://localhost:8000`. Serving over HTTP is required for the browser to load the generated file catalog and course resources.

### Publish and keep the catalog up to date

1. In the GitHub repository, open **Settings → Pages** and set the source to **GitHub Actions**.
2. Push changes to the `main` branch.
3. The included workflow regenerates `catalog.json` from the repository files and deploys the static site.

After you add a file anywhere in the repository and push it to `main`, it appears in the catalog automatically. The catalog includes all non-hidden files; formats the browser cannot preview open as normal downloads. When testing locally, rerun `python scripts/build_catalog.py` after adding files. The website remains static; the Python script only builds its file index.

## Read files in the browser

Select a lesson or a file in **Browse course files in your browser** to open the reader. The reader supports:

- PDF files, using the browser's built-in PDF viewer
- DOCX files, converted to readable HTML in your browser
- Legacy DOC files, with instructions to convert them to DOCX before previewing
- PPTX presentations, displayed slide by slide in the browser
- Legacy PPT presentations, with instructions to convert them to PPTX before previewing
- Markdown files, rendered as readable pages
- Python files, displayed as source code
- Jupyter notebooks, displayed as Markdown, code cells, and saved text/image outputs
- HTML files, displayed in a sandboxed preview

DOCX preview uses the Mammoth.js browser library, loaded from jsDelivr when a Word document is opened. PPTX preview uses JSZip to read the presentation in the browser and display text and picture slides with previous/next controls. Complex PowerPoint features such as animations and some charts may not look exactly as they do in PowerPoint. These libraries are version-pinned and integrity-checked. The document is fetched from this site and processed locally in your browser; it is not uploaded to a converter service. An internet connection is needed to load the libraries. Legacy `.doc` and `.ppt` files use older binary formats and must first be converted to `.docx` or `.pptx` (for example, with Microsoft Office or LibreOffice).

Select **Learn** or **Start learning** to use the lesson-reader layout. It has a searchable, collapsible module sidebar and displays DOCX notes and notebooks in the lesson area.

The file catalog lists files from every repository folder in natural filename order, so `Module 2` appears before `Module 10`. Jupyter notebooks are rendered as notebook cells (Markdown, code, and saved outputs), not as raw JSON. Notebook code is never executed by the site. To run a notebook, download it and open it in Jupyter. GitHub Pages rebuilds the catalog on each deployment; for local use, run `python scripts/build_catalog.py` whenever files are added.

## Learning path

The homepage links to the course material in the `5.python basic to Advance/` folder and suggests this order:

1. Getting started and Python fundamentals
2. Operators, conditionals, and loops
3. Strings and collections
4. Functions, modules, and packages
5. File handling and exceptions
6. Object-oriented programming
7. Regular expressions, web scraping, and pickling
8. Databases, advanced Python, Streamlit, Flask, and FastAPI

Use the search box on the homepage to filter lessons by topic. The **Practice and project resources** section links to exercises, interview questions, project ideas, a cheat sheet, and additional class practice.

## Course materials

- `5.python basic to Advance/` — syllabus, lesson documents, notebooks, projects, and examples
- `class_practice/` — supplementary exercises, notebooks, and sample data
- `Extras/` — presentation slides, Python scripts, and a cheat sheet
- `doc/` — a reusable copy of the static website code and its setup guide

Notebook files (`.ipynb`) can be read in the site, or downloaded and opened in Jupyter Notebook, JupyterLab, or a compatible editor. DOCX lesson files can be read in the site; download them to edit in compatible office software.

## Contributing

Keep the site static with no server-side dependencies. Pin browser-only libraries to a specific version and use Subresource Integrity for CDN scripts. Repository files are discovered automatically; update the curated learning-path cards in `index.html` only when you want to add or revise those editorial links.
