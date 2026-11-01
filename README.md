<!-- ============ custom hero ============ -->
<img src="assets/header.svg" width="100%" alt="Kenzy Zero: big data and location intelligence, and the open-source tools to work with it" />

<!-- ============ quick links ============ -->
<p align="center">
  <a href="https://pypi.org/project/kenze/"><img src="https://img.shields.io/badge/kenze-live%20on%20PyPI-f0b429?style=flat-square&logo=pypi&logoColor=0d1117&labelColor=161b22" alt="kenze on PyPI" /></a>
  <a href="https://github.com/Kenzy-Zero?tab=repositories"><img src="https://img.shields.io/badge/repositories-8b949e?style=flat-square&logo=github&logoColor=white&labelColor=161b22" alt="repositories" /></a>
  <a href="mailto:kenzy.zero.k0@gmail.com"><img src="https://img.shields.io/badge/email-8b949e?style=flat-square&logo=gmail&logoColor=white&labelColor=161b22" alt="email" /></a>
  <img src="https://komarev.com/ghpvc/?username=Kenzy-Zero&label=views&color=f0b429&style=flat-square&labelColor=161b22" alt="profile views" />
</p>

<br/>

<!-- ============ 01 whoami ============ -->
<img src="assets/whoami.svg" width="100%" alt="whoami: big data and location intelligence, creator of kenze" />

<br/><br/>

<!-- ============ 02 what I do ============ -->
<img src="assets/div-work.svg" width="100%" alt="what I do" />

> I work with **large-scale location and movement data**: billions of raw device pings, cleaned and turned
> into footfall, catchments, home and work areas, audiences and maps that real decisions get made on.
> Years of building the whole path end to end, from the raw files to the shipped product.

- Building a **location-intelligence platform**: turning *where people go* into planning and insight
- Pipelines at two scales: **DuckDB on a laptop, PySpark on a cluster**, the same cleaning rules on both sides
- Maps people can use: indoor store polygons, drive-time areas, story maps, dashboards that filter the map
- The unglamorous part done properly: de-duplication, sink detection, time zones, determinism, run logs
- Drawn to problems where **data meets the real world**

<br/>

<!-- ============ 03 what I'm building ============ -->
<img src="assets/div-building.svg" width="100%" alt="what I'm building" />

#### kenze &nbsp;·&nbsp; <sub>shipped and live on PyPI</sub>

> **Big-file data prep that never runs out of memory.** An interactive shell *and* a one-line CLI for
> CSV / Parquet / JSON / Excel files that are too big for pandas. DuckDB does the heavy lifting; kenze
> auto-sizes memory so the job never crashes, and there is no SQL to learn and no lock-in.
>
> 40 commands for the everyday work. Autocomplete that knows the **real values in your file**, with
> exact row counts. Live previews on every step. Model-ready in one step (`scale`, `bin`, `encode`,
> `traintest`). Client-ready PDF / HTML reports. Excel and GeoJSON in and out. Reads `s3://` directly.
> Every recipe ejects to plain DuckDB SQL or Python.

```bash
pip install kenze          # then just run:  kenze
```

<a href="https://github.com/Kenzy-Zero/kenze"><img src="https://raw.githubusercontent.com/Kenzy-Zero/kenze/main/demo.gif" width="100%" alt="kenze in action: load, filter, plot and run a 60M-row file without ever running out of memory" /></a>

<p>
  <a href="https://github.com/Kenzy-Zero/kenze"><img src="https://img.shields.io/badge/repo-kenze-f0b429?style=flat&logo=github&logoColor=101010" alt="repo" /></a>
  <a href="https://pypi.org/project/kenze/"><img src="https://img.shields.io/pypi/v/kenze?color=f0b429&label=PyPI&logo=pypi&logoColor=white" alt="PyPI" /></a>
  <a href="https://pepy.tech/project/kenze"><img src="https://static.pepy.tech/badge/kenze" alt="downloads" /></a>
  <a href="https://github.com/Kenzy-Zero/kenze/actions"><img src="https://img.shields.io/github/actions/workflow/status/Kenzy-Zero/kenze/ci.yml?color=f0b429&label=CI&logo=githubactions&logoColor=white" alt="CI" /></a>
  <a href="https://github.com/Kenzy-Zero/kenze/stargazers"><img src="https://img.shields.io/github/stars/Kenzy-Zero/kenze?color=f0b429&logo=github" alt="stars" /></a>
  <a href="https://github.com/Kenzy-Zero/kenze/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/kenze?color=f0b429" alt="license" /></a>
</p>

#### Kenzehub &nbsp;·&nbsp; <sub>in development, private until it is polished</sub>

> **Big messy files in, a client-ready document out.** A local-first desktop app (Tauri + DuckDB) that
> opens files far bigger than Excel can, lets you shape and check them in a grid, and writes a finished
> PDF / Word / HTML report. Nothing leaves the machine: no account, no upload, no server. The export is
> fully offline too, with zero scripts and zero external references. Thousands of tests and counting.

<p>
  <img src="https://img.shields.io/badge/status-in%20development-f0b429?style=flat" alt="status" />
  <img src="https://img.shields.io/badge/local--first-·-101010?style=flat&logo=tauri&logoColor=f0b429" alt="local-first" />
  <img src="https://img.shields.io/badge/engine-DuckDB-101010?style=flat&logo=duckdb&logoColor=f0b429" alt="DuckDB engine" />
</p>

#### kenzeplan &nbsp;·&nbsp; <sub>early build</sub>

> **A vector PDF floor plan in, IMDF and GeoJSON out, fully offline.** Reads the shapes and the unit
> labels from the plan, joins them to a tenant list, georeferences the floor and writes the OGC IMDF
> standard, validated locally against the spec. On known ground truth it recovers 9 units in 10, with
> 99.7% of them attached to the right shape. Written clean-room from scratch.

<p>
  <img src="https://img.shields.io/badge/status-early%20build-f0b429?style=flat" alt="status" />
  <img src="https://img.shields.io/badge/indoor%20mapping-IMDF-101010?style=flat" alt="IMDF" />
</p>

#### On the bench

| Project | What it is | Where it stands |
|---|---|---|
| **K-Series** | The mobility data layer: a GeoParquet profile plus the movement verbs (cleaning, home, work, dwell, trips, catchments), built on kenze's engine. | groundwork, starts after Kenzehub |
| **Z-Series** | `.z1`, an open documentation standard for the AI era: machine-first project docs at around 10x fewer tokens than a README. Working CLI. | paused |
| **A toy-city open world** | A real city rebuilt in the browser as a walkable, drivable toy city, from open map data only. Codename for now. | playable, friends beta next |

<br/>

<!-- ============ 04 stack ============ -->
<img src="assets/div-stack.svg" width="100%" alt="stack" />

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black" alt="DuckDB" />
  <img src="https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white" alt="PySpark" />
  <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="pandas" />
  <img src="https://img.shields.io/badge/GeoPandas-139C5A?style=for-the-badge&logo=python&logoColor=white" alt="GeoPandas" />
  <img src="https://img.shields.io/badge/PostgreSQL%20%2B%20PostGIS-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL + PostGIS" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
  <img src="https://img.shields.io/badge/Tauri-24C8D8?style=for-the-badge&logo=tauri&logoColor=white" alt="Tauri" />
  <img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white" alt="Node.js" />
  <img src="https://img.shields.io/badge/MapLibre%20%2B%20Kepler.gl-396CB2?style=for-the-badge&logo=maplibre&logoColor=white" alt="MapLibre + Kepler.gl" />
  <img src="https://img.shields.io/badge/AWS%20S3-232F3E?style=for-the-badge" alt="AWS S3" />
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git" />
  <img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="GitHub Actions" />
</p>

<br/>

<!-- ============ 05 signals ============ -->
<img src="assets/div-signals.svg" width="100%" alt="signals" />

<p align="center">
  <a href="https://github.com/Kenzy-Zero"><img src="https://img.shields.io/badge/contributions%20in%202026-2%2C600%2B-f0b429?style=flat-square&logo=github&logoColor=0d1117&labelColor=161b22" alt="2,600+ contributions in 2026" /></a>
  <a href="https://github.com/Kenzy-Zero/kenze/commits/main"><img src="https://img.shields.io/github/last-commit/Kenzy-Zero/kenze?style=flat-square&color=f0b429&logo=git&logoColor=white&labelColor=161b22&label=kenze%20last%20commit" alt="kenze last commit" /></a>
  <a href="https://github.com/Kenzy-Zero/kenze/releases"><img src="https://img.shields.io/github/v/release/Kenzy-Zero/kenze?style=flat-square&color=f0b429&logo=github&logoColor=white&labelColor=161b22&label=kenze%20release" alt="kenze latest release" /></a>
  <img src="https://img.shields.io/badge/building%20since-May%202026-f0b429?style=flat-square&logo=rocket&logoColor=0d1117&labelColor=161b22" alt="building since May 2026" />
</p>

<p align="center"><sub>Most of the work lives in private repos until it is polished enough to show. The public ones are the finished goods.</sub></p>

<br/>

<!-- ============ 06 connect ============ -->
<img src="assets/div-connect.svg" width="100%" alt="connect" />

<p>
  <a href="https://github.com/Kenzy-Zero"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /></a>
  <a href="https://www.linkedin.com/in/kenzy-zero/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="https://x.com/kenzy_zero"><img src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white" alt="X" /></a>
  <a href="https://www.reddit.com/user/kenzy_zero/"><img src="https://img.shields.io/badge/Reddit-FF4500?style=for-the-badge&logo=reddit&logoColor=white" alt="Reddit" /></a>
  <a href="mailto:kenzy.zero.k0@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
  <a href="https://pypi.org/project/kenze/"><img src="https://img.shields.io/badge/PyPI-3775A9?style=for-the-badge&logo=pypi&logoColor=white" alt="PyPI" /></a>
</p>

<br/><br/>

<img src="assets/footer.svg" width="100%" alt="still shipping" />
