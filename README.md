# GeoXVIEW

**Geospatially eXplicit Vertically Integrated Exposure Workflow**

A scale-adaptive environmental exposure modeling framework validated across 1,400 seasonally stratified field sites in Texas (2023–2026), showing how administrative scale alters environmental exposure estimates and how to address this.

**Author:** Abdulla Al Kafy — PhD Student, Digital Landscapes Laboratory, Department of Geography & the Environment, The University of Texas at Austin · abdullaalkafy@utexas.edu

**PhD Supervisor:** Kelley A. Crews

**Live site (after deployment):** `https://YOUR-USERNAME.github.io/geoxview/`

---

## Repository contents

| File | Description |
|------|-------------|
| `index.html` | Landing page — two cards linking to the Story and the Dashboard. |
| `GeoXVIEW_StoryMap.html` | Long-form scrollytelling page: Problem, Methods, Explore (embedded dashboard), Spotlights. |
| `GeoXVIEW_Dashboard.html` | Live interactive map. Five boundary scales; every Texas polygon rendered (measured or stratum-matched spatial proxy). Client-side search bar for city / county / ZIP / site name. |
| `README.md` | This file. |
| `LICENSE` | MIT License. |
| `CITATION.cff` | Academic citation metadata. |
| `.gitignore` | Excludes build artifacts and local data. |

All three HTML files are self-contained — GeoJSON data, images, and CSS are embedded inline. No server, database, or build step required.

---

## Deploy to GitHub Pages — step-by-step

This takes about 5 minutes from a new repository to a live public URL.

### Option 1 — Deploy as a project site (recommended)

The site will live at `https://YOUR-USERNAME.github.io/geoxview/`. Your main GitHub profile page (if you have one) remains untouched.

#### 1. Create a new public repository

1. Sign in to GitHub and go to https://github.com/new
2. **Repository name:** `geoxview` (or any name you prefer — the name becomes the URL path)
3. **Description:** `GeoXVIEW — Scale-adaptive environmental exposure modeling for Texas`
4. **Public** (required for free GitHub Pages)
5. Check **Add a README file** (you'll replace it in the next step)
6. Click **Create repository**

#### 2. Upload the four files from this folder

On the new repo's main page:

1. Click **Add file → Upload files** (top right of the file list)
2. Drag and drop, from this folder on your computer:
   - `index.html`
   - `GeoXVIEW_StoryMap.html`
   - `GeoXVIEW_Dashboard.html`
   - `README.md` *(this one replaces the auto-generated README)*
   - `LICENSE`
   - `CITATION.cff`
   - `.gitignore`
3. Scroll down, add a commit message (e.g., `Initial GeoXVIEW release`)
4. Click **Commit changes**

> **Note on file size.** `GeoXVIEW_Dashboard.html` is ~40 MB, well under GitHub's 100 MB per-file cap. GitHub's web-upload interface handles it without issue. First-visit load on the deployed site takes 5–10 seconds while the browser parses the embedded GeoJSON; subsequent interactions are instant.

#### 3. Enable GitHub Pages

1. In the repo, click **Settings** (top menu)
2. In the left sidebar, click **Pages**
3. Under **Build and deployment → Source**, select **Deploy from a branch**
4. Under **Branch**, choose `main` and folder `/ (root)`
5. Click **Save**

Wait 30–60 seconds. A green banner appears at the top of the Pages settings screen:

> **Your site is live at https://YOUR-USERNAME.github.io/geoxview/**

Open that URL. You should see the landing page with two cards.

---

### Option 2 — Deploy as your personal profile site

If you want GeoXVIEW to be your **main GitHub profile page** (i.e., hosted at `https://YOUR-USERNAME.github.io/`), name the repository `YOUR-USERNAME.github.io` instead of `geoxview`. Everything else in the steps above is identical.

> ⚠️ Use this only if you're fine with GeoXVIEW being the default landing for your whole GitHub profile. Most people prefer Option 1 (project site) so the main profile URL stays free for a general personal page.

---

### Option 3 — Custom domain (optional)

If you own a domain (e.g., `geoxview.abdullaalkafy.com`):

1. In the repo, go to **Settings → Pages → Custom domain**
2. Enter your domain and click **Save**
3. GitHub will prompt you to add DNS records at your domain registrar:
   - For an apex domain (`example.com`): four A records pointing to GitHub's IPs (shown in the Pages settings)
   - For a subdomain (`geoxview.example.com`): a CNAME record pointing to `YOUR-USERNAME.github.io`
4. After DNS propagates (up to 24 hours), check **Enforce HTTPS** in the Pages settings

---

## Updating the site

When you regenerate the HTMLs (new field data, revised narrative, additional photos):

1. Go to the repo's main page
2. Click the file you want to replace → click the pencil icon (edit) → **Replace file** (or drag a new file into **Add file → Upload files**)
3. Commit the change
4. Wait ~60 seconds; GitHub Pages rebuilds automatically

No command-line git required.

---

## Using git from the command line (optional, for frequent updates)

If you prefer the terminal:

```bash
# One-time clone
git clone https://github.com/YOUR-USERNAME/geoxview.git
cd geoxview

# After editing files locally
git add .
git commit -m "Update dashboard data"
git push
```

Pages rebuilds within a minute of each push.

---

## How the code is structured

All three HTML files are **static pages** — pure HTML + embedded CSS + embedded JavaScript.

- **Dashboard.** Built with [Leaflet 1.9.4](https://leafletjs.com/) for interactive mapping, Esri World Imagery / CartoDB for basemaps, and embedded GeoJSON for all five polygon scales. No external API calls at runtime except tile fetches. The client-side search bar indexes site names, counties, ZIP codes, and subdivisions for instant lookup.
- **StoryMap.** Single-column scrollytelling page. Pure HTML/CSS, no framework. Images are embedded as base64 data URIs so the file is portable.
- **Landing page.** Minimal HTML with two cards linking to the Story and the Dashboard.

There is no build step. To regenerate from source data, the Python scripts under `scripts/` (not included in this public repo — maintained separately) perform the pipeline: reprojection → spatial-join → stratum-matched IDW → GeoJSON export → HTML template substitution.

---

## Data sources

- **Boundary polygons:** U.S. Census Bureau TIGER/Line 2020 (counties, county subdivisions, ZCTAs, tracts, block groups)
- **Ecoregions:** U.S. EPA Level-III Ecoregions
- **Köppen zones:** Beck et al., 2018
- **Satellite products:** Landsat 8/9, Sentinel-2, MODIS
- **Field data:** 22,400 records collected 2023–2026 across 1,400 stratified sites in 254 Texas counties; 121 unique environmental strata (NLCD × Ecoregion × Köppen)

## Data and code release

- **Dataset:** Texas Data Repository + Zenodo (pending)
- **Source code:** GitHub (this repository is the public front-end; analysis scripts pending)

## Citation

If you use this framework, dataset, or visualization, please cite:

> Al Kafy, A. (2026). *GeoXVIEW — Geospatially eXplicit Vertically Integrated Exposure Workflow.* The University of Texas at Austin. https://YOUR-USERNAME.github.io/geoxview/

(See `CITATION.cff` for a machine-readable version.)

## Acknowledgments

- **Scholars Lab Fellowship** — UT Libraries
- **Robert E. Veselka Memorial Fellowship**
- Kelley A. Crews (PhD Supervisor)
- Alex Marden (GIS & Geospatial Data Coordinator, UT Libraries)

## License

MIT. See `LICENSE`.

## Contact

**Abdulla Al Kafy** · abdullaalkafy@utexas.edu
