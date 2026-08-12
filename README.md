# 🚀 Metupy

A lightweight, modern Python documentation framework powered by Flask, Alpine.js, and Markdown.

---

## ✨ Features

* **⚡ Fast & Lightweight:** Built on top of Flask and Alpine.js with minimal setup.
* **🔍 Built-in Search:** Instantly search through your documentation with zero extra configuration.
* **🌙 Dark Mode:** Native light and dark theme switching out-of-the-box.
* **📱 Responsive Layout:** 3-column layout with sidebar navigation and Table of Contents (ToC).
* **🔄 Live Reload:** Automatically refreshes the browser during development.
* **📦 Component Blueprints:** Pre-built UI components like Badges, Cards, Modals, Tabs, and Buttons.

---

## 📦 Installation

Install Metupy using `uv` or `pip`:

```bash
# Using uv (Recommended)
uv add metupy

# Using pip
pip install metupy
```

### 🚀 Quick Start

1. Initialize your pages directory and create an `index.py`:

```python
# pages/index.py
from metupy import page

@page(title="Welcome to Metupy")
def index():
    return """
    # Hello Metupy!
    Welcome to your new documentation site.
    """
```

2. Run the development server:

```python
from metupy.engine import MetupyServer

if __name__ == "__main__":
    server = MetupyServer()
    server.run(port=5000)
```

## 📂 Project Structure

```text
metupy/
├── pyproject.toml
├── uv.lock
├── pages/
│   └── index.py
└── src/
    └── metupy/
        ├── assets/
        ├── components_blueprint/
        ├── templates/
        ├── cli.py
        ├── engine.py
        └── page.py
```

## 📄 License

This project is licensed under the MIT License.