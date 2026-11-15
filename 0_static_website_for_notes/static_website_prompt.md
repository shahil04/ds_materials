# Reusable Prompt: Turn a Course Repository into a Static Learning Website

Copy this prompt into a coding assistant when you want to build a static course website from the files in a repository. Replace the bracketed details if needed; otherwise, inspect the repository and make sensible choices.

---

## Prompt

Act as a senior frontend engineer. Inspect this repository and turn its existing course materials into a polished, responsive, accessible static learning website.

### Goals

1. Create a clear course homepage at the repository root (`index.html`) that introduces the course, guides learners through the content, and makes the existing learning resources easy to find.
2. Build a file catalog from the repository itself. Do not maintain a second, manually written list of files in the HTML.
3. Show course files in natural filename order within their folders. Numeric portions must sort as numbers, so `Module 2` comes before `Module 10`. Keep filenames intact and label each item with its file type.
4. Let learners search the catalog and open files in an in-page reader whenever the format can be safely previewed.
5. Keep the site static: no application server, database, account system, build framework, or package installation should be required to view the deployed site.

### Before making changes

- Inspect the repository structure, existing homepage/readme, file types, deployment configuration, and current working-tree changes.
- Reuse existing conventions and preserve unrelated user changes.
- Identify which formats are actually present. Do not invent file links or claim a format is supported without implementing and testing it.

### Homepage and catalog

- Create or update a responsive, accessible root `index.html` that clearly presents the course and its learning path.
- Include the major lesson modules and practice/project resources. Curated course cards are fine, but the file catalog itself must be generated from repository contents.
- Generate a catalog manifest (for example, `catalog.json`) using a small standard-library script (for example, `scripts/build_catalog.py`).
- Scan files recursively and include newly added files automatically after catalog generation/deployment. Ignore hidden files, editor lock files (such as `~$...`), generated site output, dependency directories, caches, and the generated catalog itself. Do not expose secrets, `.env` files, or other hidden configuration.
- Include the relative path, filename, parent folder, and extension in each catalog entry.
- Sort folder/file names naturally and case-insensitively so module numbers are in numeric sequence. Preserve Unicode filenames and URLs correctly.
- Group entries by folder, display the extension/type badge, and provide a working search box.
- Do not expose hidden files or accidentally list generated catalog output recursively.

### In-browser file reading

Implement and test appropriate previews for the formats present in this repository. For example:

- **Jupyter notebooks (`.ipynb`):** render notebook-like Markdown cells, code cells, and saved text/image outputs. Never execute notebook code in a static site.
- **Markdown (`.md`, `.markdown`):** render readable headings, paragraphs, lists, links, and fenced code safely.
- **Python (`.py`) and text/code files:** display escaped source text in a readable code block; never execute it.
- **PDF (`.pdf`):** use the browser’s built-in PDF viewer.
- **HTML (`.html`, `.htm`):** use a sandboxed preview. Do not allow untrusted page scripts to run in the main site origin.
- **Word (`.docx`):** if using a browser library, pin its version, use Subresource Integrity for CDN scripts, document the network requirement, and sanitize/allowlist converted markup. Process the document in the visitor’s browser; do not upload private course material to a third-party conversion service.
- **Legacy Word (`.doc`) and PowerPoint (`.ppt`):** explain that these binary formats should be converted to `.docx` or `.pptx` before previewing. Keep the original available as a download.
- **PowerPoint (`.pptx`):** provide slide-by-slide preview with previous/next controls where feasible. Clearly explain that complex formatting, animations, or some chart types may differ from Microsoft PowerPoint. Pin and integrity-check any browser libraries.
- For unsupported formats, keep a working link to the original file/download and show a clear type label instead of a broken preview.

Use safe DOM APIs (`textContent`, element creation, allowlists, and protocol checks); do not insert untrusted file contents directly as arbitrary HTML. Reader errors should be visible and explain likely causes such as a missing file, offline CDN, or opening the site with `file://` rather than HTTP.

### Deployment and automatic updates

- Add or update a GitHub Actions Pages workflow that runs when files are pushed to the primary branch and supports manual dispatch.
- The workflow must install no application dependencies; use an available Python runtime to run the catalog generator, then publish the static repository output using the supported Pages artifact/deploy actions.
- Document the one-time GitHub setting required to use **Settings → Pages → GitHub Actions**.
- Make it clear that a pushed file appears after deployment. For local testing, document the exact command to regenerate the catalog and start a basic HTTP server.
- Do not imply that a static site can inspect the repository directory at visitor runtime. The catalog must be generated before deployment; GitHub Pages then serves the generated manifest.

### Documentation

Create or update `README.md` with:

- How to run the catalog generator and preview locally over HTTP.
- How automatic deployment works and the one-time Pages setting.
- Supported browser previews, limitations, network requirements, and how to download/run notebooks.
- How to add new materials and what to do for formats requiring conversion.
- Where course content lives, based on the actual repository.

### Validation and completion

- Add focused tests for catalog generation, natural numeric sorting, nested paths, ignored files, and supported/unsupported extensions.
- Run those tests and regenerate the catalog.
- Confirm every catalog path exists and module files are in natural order.
- Validate the HTML/JavaScript as available and check all generated links.
- Use a browser or equivalent functional test to exercise catalog search, at least one notebook preview, and each implemented document/slide viewer that can be tested locally.
- Run `git diff --check` and report validation results and any format limitations.
- Avoid unrelated refactors, do not commit changes unless explicitly requested, and finish with a concise summary of changed files and the local run instructions.

### Repository-specific preferences (optional)

- Course title: [COURSE TITLE]
- Primary course-material folder(s): [FOLDERS, OR “DETECT AUTOMATICALLY”]
- Preferred visual style: [STYLE, OR “CHOOSE A CLEAN, READABLE DESIGN”]
- Primary deployment branch: [BRANCH, USUALLY `main`]

---
