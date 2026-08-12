<p align="center">
  <img src="https://raw.githubusercontent.com/palembangpy/metupy/main/src/metupy/assets/metupy.png" alt="Metupy Logo" width="180">
</p>

<p align="center">
  <a href="https://pypi.org/project/metupy"><img src="https://img.shields.io/pypi/v/metupy?color=blue&style=for-the-badge" alt="PyPI Version"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"></a>
  <a href="https://github.com"><img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License"></a>
  <a href="https://github.com"><img src="https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge&logo=github-actions" alt="Build Status"></a>
</p>

<h1 align="center">Metupy Framework</h1>

<p align="center">
  A lightweight, modern Python documentation framework & Static Site Generator (SSG) powered by PalembangPy Community.
</p>

---

## ✨ Features

* **⚡ Fast & Lightweight:** Built on top of Flask and Alpine.js with minimal setup.
* **🛠️ CLI-Driven Workflow:** Commands for project initialization, page generation, theme management, and building.
* **🏗️ Static Site Generator (SSG):** Export documentation to ready-to-deploy static HTML and Markdown files (dist/).
* **🔍 Built-in Search:** Instantly search through your documentation out-of-the-box.
* **🌙 Dark Mode:** Native light and dark theme switching.
* **📱 Responsive Layout:** 3-column layout with sidebar navigation and Table of Contents (ToC).
* **📦 Dynamic Component System:** Pre-built UI components like Buttons, Modals, Tabs, Badges, Kbd, and Icon.
* **🎨 Theme Engine:** Support for custom themes and direct theme installation from GitHub repositories.

---

## 📦 Installation

Install Metupy using uv or pip:

```text
# Using uv (Recommended)
uv add metupy

# Using pip
pip install metupy
```

---

## 🚀 Quick Start

1. Initialize a new Metupy project:

```console
metupy init my_docs
cd my_docs
```

2. Start the local development server:

`metupy dev`

Open your browser at http://localhost:5000.

3. Build static site for production:

`metupy build`

Your HTML documentation and Markdown files will be generated inside the dist/ folder.

---

## 💻 Creating Pages

Pages are created inside the pages/ directory using Python and the Page class:
```python
# pages/index.py
from metupy.page import Page
from components import Button, Icon

page = Page(title="Home")

# 1. Page Content
page.title("Welcome to Metupy")
page.text("Lightweight Python-based framework for documentation.")

# 2. Interactive Components
btn_start = Button(text="Get Started", icon="fa-solid fa-rocket", href="#quickstart")

# 3. HTML Layout
page.raw(f"""
<div style="text-align: center; margin-top: 2rem;">
    {btn_start}
</div>
""")
```
---

## 🛠️ CLI Commands

| Command | Description |
|---|---|
| metupy init <project_name> | Initialize a new Metupy project boilerplate |
| metupy dev [--port 5000] | Run development server with local live-reload |
| metupy build | Export project into static HTML & Markdown (dist/) |
| metupy add <component_name> | Add blueprint UI component to local ./components/ |
| metupy make:page <path> | Create a new page file in ./pages/ |
| metupy make:pagegroup <paths> | Create multiple pages or folders at once |
| metupy make:theme <theme_name> | Scaffold a new custom theme in ./templates/ |
| metupy install:theme <user/repo> | Download and install theme from GitHub repository |

---

## 📂 Project Structure

```text
my_docs/
├── pyproject.toml      # Framework & theme configuration
├── assets/             # Static files (images, logo, etc.)
├── components/         # Local UI components & dynamic component loader
│   └── __init__.py
├── pages/              # Documentation site pages
│   └── index.py
└── dist/               # Generated build output (after metupy build)
    ├── sites/          # Compiled HTML documentation
    └── contents/       # Raw Markdown files
```
---

## 📄 License

This project is licensed under the MIT License.
