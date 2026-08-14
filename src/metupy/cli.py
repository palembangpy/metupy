import io
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
import zipfile
import click
import jinja2
import markdown

from metupy.engine import MetupyServer

PACKAGE_NAME = "metupy"


def check_and_auto_update():
    try:
        from importlib.metadata import PackageNotFoundError, version
        current_version = version(PACKAGE_NAME)
    except Exception:
        return

    try:
        url = f"https://pypi.org/pypi/{PACKAGE_NAME}/json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Metupy-CLI'})

        with urllib.request.urlopen(req, timeout=1.5) as response:
            data = json.loads(response.read().decode())
            latest_version = data["info"]["version"]

        def parse_ver(v):
            return tuple(map(int, (v.split("."))))

        if parse_ver(latest_version) > parse_ver(current_version):
            click.secho(
                f"\n🚀 [Metupy] New version found! (v{current_version} ->"
                f" v{latest_version})",
                fg='cyan',
            )
            click.secho("🔄 Starting auto-update process...", fg='yellow')

            cmd = [sys.executable, "-m", "pip", "install", "--upgrade", PACKAGE_NAME]
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            if result.returncode == 0:
                click.secho(
                    f"✨ [Metupy] Successfully updated to v{latest_version}!",
                    fg='green',
                    bold=True,
                )
                click.secho("💡 Please re-run your command.\n", fg='yellow')
                sys.exit(0)
            else:
                click.secho(
                    "⚠️ Auto-update failed, continuing with current version...\n",
                    fg='yellow',
                )
    except Exception:
        pass


COMPONENTS_INIT_TEMPLATE = '''import os
import sys
import re
import importlib.util

_cache = {}

def _get_active_theme() -> str:
    toml_path = os.path.join(os.getcwd(), "pyproject.toml")
    if os.path.exists(toml_path):
        try:
            try:
                import tomllib
            except ImportError:
                import tomllib as tomllib
            with open(toml_path, "rb") as f:
                data = tomllib.load(f)
                return data.get("tool", {}).get("metupy", {}).get("theme", "default")
        except Exception:
            pass
    return "default"

def __getattr__(name: str):
    if name in _cache:
        return _cache[name]
        
    file_name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    cwd = os.getcwd()
    active_theme = _get_active_theme()
    
    import metupy
    lib_dir = os.path.dirname(os.path.abspath(metupy.__file__))

    # Workspace prioritas untuk tema luar (./theme/) dan tema default (templates/)
    possible_paths = [
        os.path.join(cwd, 'components', f"{file_name}.py"),
        os.path.join(cwd, 'theme', active_theme, 'components', f"{file_name}.py"),
        os.path.join(cwd, 'templates', active_theme, 'components', f"{file_name}.py"),
        os.path.join(lib_dir, 'templates', active_theme, 'components', f"{file_name}.py"),
        os.path.join(lib_dir, 'components_blueprint', f"{file_name}.py"),
    ]

    target_path = None
    for path in possible_paths:
        if os.path.exists(path):
            target_path = path
            break

    if not target_path:
        raise AttributeError(f"Component '{name}' (file: {file_name}.py) not found.")

    module_name = f"components._dynamic_{file_name}"
    spec = importlib.util.spec_from_file_location(module_name, target_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Failed to load module for component '{name}'")

    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)

    component_cls = getattr(mod, name, None)
    if not component_cls:
        for attr in dir(mod):
            if not attr.startswith('_') and isinstance(getattr(mod, attr), type):
                component_cls = getattr(mod, attr)
                break

    if not component_cls:
        raise AttributeError(f"Class '{name}' not found in {target_path}")

    _cache[name] = component_cls
    return component_cls
'''


@click.group()
def cli():
    """Metupy CLI - Modern Python SSG Framework."""
    check_and_auto_update()


@cli.command()
@click.argument('project_name')
def init(project_name):
    """Initialize a new Metupy project including GitHub Actions workflow."""
    if project_name == ".":
        base_dir = os.getcwd()
        actual_project_name = os.path.basename(base_dir)
    else:
        base_dir = os.path.join(os.getcwd(), project_name)
        actual_project_name = project_name
        if os.path.exists(base_dir):
            click.secho(f"Folder '{project_name}' already exists!", fg='red')
            return

    toml_path = os.path.join(base_dir, 'pyproject.toml')
    if os.path.exists(toml_path):
        click.secho("Metupy project is already initialized in this directory!", fg='red')
        return

    pages_dir = os.path.join(base_dir, 'pages')
    assets_dir = os.path.join(base_dir, 'assets')
    components_dir = os.path.join(base_dir, 'components')
    workflows_dir = os.path.join(base_dir, '.github', 'workflows')

    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)
    os.makedirs(components_dir, exist_ok=True)
    os.makedirs(workflows_dir, exist_ok=True)

    library_dir = os.path.dirname(os.path.abspath(__file__))

    lib_logo_path = os.path.join(library_dir, "assets", "metupy.png")
    if os.path.exists(lib_logo_path):
        shutil.copy(lib_logo_path, os.path.join(assets_dir, "metupy.png"))

    with open(
        os.path.join(components_dir, "__init__.py"), "w", encoding="utf-8"
    ) as f:
        f.write(COMPONENTS_INIT_TEMPLATE)

    workflow_path = os.path.join(workflows_dir, 'deploy.yml')
    workflow_content = """name: Deploy Metupy SSG

on:
  push:
    branches:
      - main

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
          cache: 'pip'

      - name: Install Metupy
        run: |
          python -m pip install --upgrade pip
          pip install metupy

      - name: Build Static Site
        run: |
          metupy build

      - name: Upload Artifact (/dist)
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""
    with open(workflow_path, 'w', encoding='utf-8') as f:
        f.write(workflow_content)

    index_path = os.path.join(pages_dir, 'index.py')
    index_content = '''# Generated by Metupy CLI
from metupy.page import Page
from components import Button, Tabs, Kbd, Modal, Icon

page = Page(title="Home")

icon_badge = Icon("fa-solid fa-rocket", size="sm")
icon_bolt_title = Icon("fa-solid fa-bolt", size="md")
icon_fast = Icon("fa-solid fa-bolt-lightning", size="xl", color="var(--accent)")
icon_palette = Icon("fa-solid fa-palette", size="xl", color="var(--accent)")
icon_responsive = Icon("fa-solid fa-mobile-screen-button", size="xl", color="var(--accent)")

btn_primary = Button(
    text="Get Started", 
    icon="fa-solid fa-rocket", 
    href="#quickstart", 
    height="44px"
)
btn_github = Button(
    text="GitHub Repo", 
    icon="fa-brands fa-github", 
    href="https://github.com", 
    height="44px"
)

code_python = """from metupy.page import Page

page = Page(title="Home")
page.title("Hello World!")"""

code_terminal = "pip install metupy\\nmetupy dev"

tabs_demo = Tabs([
    ("Python", code_python),
    ("Terminal", code_terminal)
])

kbd_shortcut = Kbd(["Ctrl", "K"])

modal_demo = Modal(
    id_name="welcome_modal",
    title="Welcome to Metupy!",
    content="The boilerplate home page is successfully loaded! Components like Modal, Tabs, Button, Kbd, and Icon are now cleanly initialized.",
    trigger_text="Open Interactive Modal"
)

page.raw(f"""
<div style="text-align: center; padding: 2.5rem 1rem 1.5rem 1rem; max-width: 800px; margin: 0 auto;">
    <span style="display: inline-flex; align-items: center; padding: 4px 14px; background: var(--accent-glow); color: var(--accent); border-radius: 20px; font-size: 0.85rem; font-weight: 600; margin-bottom: 1.25rem;">
        {icon_badge} Metupy Framework v1.0
    </span>
    <h1 style="font-size: 2.5rem; font-weight: 800; line-height: 1.25; margin-bottom: 1rem; letter-spacing: -0.02em;">
        Build Modern & Fast Python Documentation
    </h1>
    <p style="font-size: 1.1rem; color: var(--text-muted); max-width: 620px; margin: 0 auto 2rem auto; line-height: 1.6;">
        Lightweight Python-based framework for creating interactive, precise, and responsive documentation websites instantly.
    </p>
    <div style="display: flex; gap: 0.85rem; justify-content: center; align-items: center; flex-wrap: wrap;">
        {btn_primary}
        {btn_github}
    </div>
</div>

<div id="quickstart" style="max-width: 800px; margin: 2.5rem auto 1rem auto;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 8px;">
        <h2 style="border: none; margin: 0; font-size: 1.3rem; font-weight: 700; display: flex; align-items: center;">
            {icon_bolt_title} Quick Start
        </h2>
        <span style="font-size: 0.85rem; color: var(--text-muted);">
            Press {kbd_shortcut} to search
        </span>
    </div>
    {tabs_demo}
</div>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 1.25rem; max-width: 800px; margin: 2.5rem auto;">
    <div style="padding: 1.25rem; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 12px;">
        <div style="margin-bottom: 0.5rem;">{icon_fast}</div>
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.05rem; font-weight: 600;">Blazing Fast</h3>
        <p style="margin: 0; font-size: 0.875rem; color: var(--text-muted); line-height: 1.5;">High performance with zero heavy dependencies, ready directly from Python.</p>
    </div>
    <div style="padding: 1.25rem; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 12px;">
        <div style="margin-bottom: 0.5rem;">{icon_palette}</div>
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.05rem; font-weight: 600;">Modern Components</h3>
        <p style="margin: 0; font-size: 0.875rem; color: var(--text-muted); line-height: 1.5;">Button, Modal, Tabs, Kbd, and Icon components pre-styled for elegance.</p>
    </div>
    <div style="padding: 1.25rem; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 12px;">
        <div style="margin-bottom: 0.5rem;">{icon_responsive}</div>
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.05rem; font-weight: 600;">100% Responsive</h3>
        <p style="margin: 0; font-size: 0.875rem; color: var(--text-muted); line-height: 1.5;">Fully optimized UI layout for desktop and mobile displays.</p>
    </div>
</div>

<div style="text-align: center; max-width: 800px; margin: 2.5rem auto 1rem auto; padding: 2rem 1.5rem; background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 14px;">
    <h3 style="margin-top: 0; margin-bottom: 0.5rem; font-size: 1.2rem;">Interactive Feature Demo</h3>
    <p style="color: var(--text-muted); font-size: 0.925rem; margin-bottom: 1.25rem;">Click the button below to trigger an interactive dialog modal.</p>
    {modal_demo}
</div>
""")
'''
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)

    toml_content = f"""# Generated by Metupy CLI
[project]
name = "{actual_project_name}"
version = "0.1.0"
description = "Documentation created with Metupy"
requires-python = ">=3.10"
dependencies = ["metupy"]

[tool.metupy]
theme = "default"
category = "docs"
author = "Nama Kreator <email@domain.com>"
organization = "Company / Organization"
theme_status = "available"
theme_repo_url = "https://github.com/username/repo"
theme_registry_date = "2026-08-13|11:51:27"
use_darkmode = true
use_search = true
logo = "/assets/metupy.png"

[tool.metupy.icons]
cdn_url = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css"
"""
    with open(toml_path, 'w', encoding='utf-8') as f:
        f.write(toml_content)

    if project_name == ".":
        click.secho(
            "Project successfully initialized in the current directory! Run 'metupy dev'",
            fg='green',
        )
    else:
        click.secho(
            f"Project '{project_name}' successfully created with GitHub Actions workflow! Run 'cd {project_name}'"
            " then 'metupy dev'",
            fg='green',
        )


@cli.command()
@click.argument('component_names', nargs=-1, required=True)
def add(component_names):
    """Add component from blueprint to local ./components/ directory."""
    library_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(os.getcwd(), 'components')

    os.makedirs(target_dir, exist_ok=True)

    for component_name in component_names:
        file_name = component_name.lower()
        target_path = os.path.join(target_dir, f"{file_name}.py")

        if os.path.exists(target_path):
            click.secho(
                f"Component '{component_name}' already exists in"
                f" ./components/{file_name}.py!",
                fg='yellow',
            )
            continue

        blueprint_path = os.path.join(
            library_dir, 'components_blueprint', f"{file_name}.py"
        )

        if not os.path.exists(blueprint_path):
            click.secho(
                f"Component '{component_name}' not found in default blueprints.",
                fg='red',
            )
            continue

        shutil.copy(blueprint_path, target_path)

        click.secho(
            f"Component '{component_name}' successfully added to"
            f" ./components/{file_name}.py!",
            fg='green',
        )


@cli.command(name="make:page")
@click.argument('path')
def make_page(path):
    """Create a single new page compatible with any active theme."""
    path = path.replace('.py', '')
    target_dir = os.path.join(os.getcwd(), 'pages')
    os.makedirs(target_dir, exist_ok=True)

    file_path = os.path.join(target_dir, f"{path}.py")
    if os.path.exists(file_path):
        click.secho("Page already exists!", fg='red')
        return

    page_name = os.path.basename(path).replace('_', ' ').capitalize()
    template = (
        f'# Generated by Metupy CLI\nfrom metupy.page import Page\n\npage ='
        f' Page(title="{page_name}")\npage.title("{page_name}'
        f' Page")\npage.text("Welcome to {page_name} page")\n'
    )
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(template)

    click.secho(f"Page created: ./pages/{path}.py", fg='green')


@cli.command(name="make:pagegroup")
@click.argument('args', nargs=-1)
def make_pagegroup(args):
    """Create a group of pages compatible with any active theme."""
    for arg in args:
        parts = arg.split('/')
        folder = os.path.join(os.getcwd(), 'pages', parts[0])
        os.makedirs(folder, exist_ok=True)

        file_name = f"{parts[1]}.py" if len(parts) > 1 else "index.py"
        file_path = os.path.join(folder, file_name)

        if not os.path.exists(file_path):
            page_name = (
                parts[1].capitalize()
                if len(parts) > 1
                else parts[0].capitalize()
            )
            template = (
                '# Generated by Metupy CLI\nfrom metupy.page import Page\n\npage ='
                f' Page(title="{page_name}")\npage.title("{page_name}'
                ' Page")\n'
            )
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(template)
            click.secho(f"Page created: ./pages/{arg}.py", fg='green')


@cli.command(name="make:theme")
@click.argument('theme_name')
def make_theme(theme_name):
    """Create a new custom theme directory in ./theme/<theme_name>/ with its own config file."""
    target_dir = os.path.join(os.getcwd(), 'theme', theme_name)

    if os.path.exists(target_dir):
        click.secho(
            f"Theme '{theme_name}' already exists in ./theme/!", fg='red'
        )
        return

    library_dir = os.path.dirname(os.path.abspath(__file__))
    default_theme_dir = os.path.join(library_dir, "templates", "default")

    if not os.path.exists(default_theme_dir):
        click.secho("Default Metupy theme directory not found!", fg='red')
        return

    click.secho(f"\nConfiguring metadata for theme: '{theme_name}'", fg='cyan', bold=True)
    version = click.prompt("Enter theme version", type=str, default="1.0.0").strip()
    category = click.prompt("Enter theme category (e.g., docs, landing, blog)", type=str, default="docs").strip()
    author = click.prompt("Enter author name", type=str, default="johndoe").strip()
    organization = click.prompt("Enter organization / company name", type=str, default="PalembangPy Community").strip()
    theme_repo_url = click.prompt("Enter theme repository URL", type=str, default=f"https://github.com/{author}/{theme_name}").strip()
    
    import datetime
    theme_registry_date = datetime.datetime.now().strftime("%Y-%m-%d|%H:%M:%S")

    os.makedirs(target_dir, exist_ok=True)
    boilerplate_files = ["layout.html", "style.css", "script.js"]
    for file_name in boilerplate_files:
        src_file = os.path.join(default_theme_dir, file_name)
        if os.path.exists(src_file):
            shutil.copy(src_file, os.path.join(target_dir, file_name))

    default_components_dir = os.path.join(default_theme_dir, "components")
    if os.path.exists(default_components_dir):
        shutil.copytree(default_components_dir, os.path.join(target_dir, "components"), dirs_exist_ok=True)

    theme_toml_content = f"""[tool.metupy.theme]
name = "{theme_name}"
version = "{version}"
category = "{category}"
author = "{author}"
organization = "{organization}"
theme_status = "not-available"
theme_repo_url = "{theme_repo_url}"
theme_registry_date = "{theme_registry_date}"
"""
    theme_toml_path = os.path.join(target_dir, "pyproject.toml")
    with open(theme_toml_path, 'w', encoding='utf-8') as f:
        f.write(theme_toml_content)

    click.secho(
        f"\nTheme '{theme_name}' successfully created at ./theme/{theme_name}/ with its own configuration!",
        fg='green',
    )


@cli.command(name="install:theme")
@click.argument('repo_path')
def install_theme(repo_path):
    """Download and install a theme from GitHub into ./theme/."""
    repo_clean = repo_path.replace("https://github.com/", "").strip("/")
    parts = repo_clean.split("/")

    if len(parts) < 2:
        click.secho(
            "Invalid repository format! Use 'username/repo-name'", fg='red'
        )
        return

    user, repo = parts[0], parts[1]
    theme_name = repo.replace("metupy-theme-", "").replace("metupy-", "")
    target_dir = os.path.join(os.getcwd(), 'theme', theme_name)

    click.secho(
        f"Downloading theme '{theme_name}' from GitHub ({user}/{repo})...",
        fg='cyan',
    )

    urls_to_try = [
        f"https://github.com/{user}/{repo}/archive/refs/heads/main.zip",
        f"https://github.com/{user}/{repo}/archive/refs/heads/master.zip",
    ]

    zip_bytes = None
    for url in urls_to_try:
        try:
            req = urllib.request.Request(
                url, headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    zip_bytes = response.read()
                    break
        except Exception:
            continue

    if not zip_bytes:
        click.secho(
            "Failed to download theme repository. Check the GitHub repository"
            " name and branch (main/master).",
            fg='red',
        )
        return

    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
            root_folder = z.namelist()[0].split('/')[0]

            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            os.makedirs(target_dir, exist_ok=True)

            for member in z.infolist():
                if member.filename.startswith(root_folder + "/"):
                    rel_path = member.filename[len(root_folder) + 1 :]
                    if not rel_path:
                        continue

                    dest_path = os.path.join(target_dir, rel_path)
                    if member.is_dir():
                        os.makedirs(dest_path, exist_ok=True)
                    else:
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        with (
                            z.open(member) as source,
                            open(dest_path, "wb") as target,
                        ):
                            shutil.copyfileobj(source, target)

        toml_path = os.path.join(os.getcwd(), 'pyproject.toml')
        if os.path.exists(toml_path):
            with open(toml_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            updated_content = re.sub(
                r'theme\s*=\s*"[^"]*"', 
                f'theme = "{theme_name}"', 
                content
            )
            
            with open(toml_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

        click.secho(
            f"Theme '{theme_name}' successfully installed to ./theme/{theme_name}/",
            fg='green',
        )
        click.secho(
            f"Automatically updated pyproject.toml -> theme = \"{theme_name}\"",
            fg='cyan',
        )

    except Exception as e:
        click.secho(f"An error occurred while extracting theme: {e}", fg='red')


@cli.command()
@click.option('--port', default=5000)
def dev(port):
    """Run local development server."""
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())

    app = MetupyServer(os.getcwd())
    click.secho(f"Server running at http://localhost:{port}", fg='green')
    app.run(port=port)


@cli.command()
@click.option('--domain', default="", help="Custom domain or subdomain for deployment.")
@click.option('--pwa/--no-pwa', default=False, help="Enable or disable PWA support.")
def build(domain, pwa):
    """Build static site documentation into pure HTML pages using active theme workspace."""
    custom_domain_value = domain
    enable_pwa = pwa

    if not domain and sys.stdin and sys.stdin.isatty():
        custom_domain_choice = click.prompt("Do you want to customize the domain? (yes/no)", type=str, default="no").strip().lower()
        if custom_domain_choice == "yes":
            custom_domain_value = click.prompt("Enter domain or subdomain (without http/https)", type=str).strip()

    if not pwa and sys.stdin and sys.stdin.isatty():
        pwa_choice = click.prompt("Do you want to enable PWA (Progressive Web App) support? (yes/no)", type=str, default="no").strip().lower()
        enable_pwa = (pwa_choice == "yes")

    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())

    app = MetupyServer(os.getcwd())
    dist_dir = 'dist'
    dist_assets = os.path.join(dist_dir, 'assets')

    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir, exist_ok=True)

    user_assets = os.path.join(os.getcwd(), 'assets')
    if os.path.exists(user_assets):
        shutil.copytree(user_assets, dist_assets)

    theme_name = app.config.get("theme", "default")
    
    user_theme_dir = os.path.join(os.getcwd(), "theme", theme_name)
    legacy_user_theme_dir = os.path.join(os.getcwd(), "templates", theme_name)
    lib_theme_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "templates", theme_name
    )
    fallback_lib_default = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "templates", "default"
    )

    if os.path.exists(user_theme_dir):
        active_theme_dir = user_theme_dir
    elif os.path.exists(legacy_user_theme_dir):
        active_theme_dir = legacy_user_theme_dir
    elif os.path.exists(lib_theme_dir):
        active_theme_dir = lib_theme_dir
    else:
        active_theme_dir = fallback_lib_default

    layout_path = os.path.join(active_theme_dir, "layout.html")
    css_path = os.path.join(active_theme_dir, "style.css")
    js_path = os.path.join(active_theme_dir, "script.js")

    if not os.path.exists(layout_path):
        click.secho(f"Error: Template layout.html not found in active workspace '{active_theme_dir}'", fg='red')
        return

    with open(layout_path, 'r', encoding='utf-8') as f:
        layout_src = f.read()

    default_css = ""
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            default_css = f.read()

    default_js = ""
    if os.path.exists(js_path):
        with open(js_path, "r", encoding="utf-8") as f:
            default_js = f.read()

    env = jinja2.Environment()
    template = env.from_string(layout_src)

    search_index = []
    for route, page_obj in app._routes.items():
        clean_r = route.strip('/')
        url_file = f"/{clean_r}" if clean_r else "/"
        title = getattr(page_obj, 'page_title', clean_r.replace('_', ' ').replace('-', ' ').title() or 'Home')

        raw_content = page_obj.render() if hasattr(page_obj, 'render') else str(page_obj)
        
        clean_text = re.sub(r'```.*?```', ' ', raw_content, flags=re.DOTALL)
        clean_text = re.sub(r'`[^`]+`', ' ', clean_text)
        clean_text = re.sub(r'<[^>]+>', ' ', clean_text)
        clean_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_text)
        clean_text = re.sub(r'[#\*\_\>\|\-\=\[\]\(\)]', ' ', clean_text)
        clean_text = " ".join(clean_text.split())

        search_index.append({
            'title': title,
            'url': url_file,
            'content': clean_text
        })

    search_index_json = json.dumps(search_index)

    def generate_ssg_sidebar(current_route):
        active_folder_init = "null"
        for folder, pages in app._tree.items():
            if folder != "root" and any(current_route == p["route"] for p in pages):
                active_folder_init = f"'{folder.replace(chr(39), chr(92)+chr(39))}'"
                break

        sidebar_html = f'<div x-data="{{ activeGroup: {active_folder_init} }}">\n'
        
        for folder, pages in app._tree.items():
            if folder == "root":
                for p in pages:
                    clean_r = p["route"].strip('/')
                    href = f"/{clean_r}" if clean_r else "/"
                    active_class = 'active' if current_route == p["route"] else ""
                    sidebar_html += f'<a class="menu-link {active_class}" href="{href}" @click="sidebarOpen = false">{p["title"]}</a>\n'
            else:
                folder_id = folder.replace("'", "\\'")
                folder_title = folder.replace('-', ' ').replace('_', ' ').title()

                sidebar_html += f'''
                <div style="margin-bottom: 4px;">
                    <button @click="activeGroup = (activeGroup === '{folder_id}' ? null : '{folder_id}')" 
                            class="menu-link dropdown-btn" 
                            :class="{{ 'active': activeGroup === '{folder_id}' }}">
                        <span style="font-weight: 600;">{folder_title}</span>
                        <svg class="chevron" :class="{{ 'rotate': activeGroup === '{folder_id}' }}" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
                    </button>
                    <div x-show="activeGroup === '{folder_id}'" x-collapse class="dropdown-menu">
                '''
                for p in pages:
                    clean_r = p["route"].strip('/')
                    href = f"/{clean_r}" if clean_r else "/"
                    active_class = 'active' if current_route == p["route"] else ""
                    sidebar_html += f'<a class="menu-link {active_class}" href="{href}" @click="sidebarOpen = false">{p["title"]}</a>\n'
                sidebar_html += '</div></div>\n'
        
        sidebar_html += '</div>'
        return sidebar_html

    # ==== PWA Configuration & Injection ====
    pwa_head_tags = ""
    pwa_body_tags = ""
    
    if enable_pwa:
        user_logo = app.config.get("logo", "/assets/metupy.png")
        app_name = app.config.get("name", "Metupy Documentation")

        pwa_head_tags = f"""
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#ffffff">
    <link rel="apple-touch-icon" href="{user_logo}">
"""
        pwa_body_tags = """
    <script>
      if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
          navigator.serviceWorker.register('/sw.js')
            .then(reg => console.log('Metupy Service Worker registered!'))
            .catch(err => console.log('Service Worker registration failed: ', err));
        });
      }

      let deferredPrompt;
      window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        
        let installBtn = document.getElementById('pwa-install-btn');
        if (!installBtn) {
          installBtn = document.createElement('button');
          installBtn.id = 'pwa-install-btn';
          installBtn.innerHTML = '<i class="fa-solid fa-download"></i> Install';
          installBtn.style.cssText = 'position: fixed; bottom: 20px; right: 20px; z-index: 9999; background: var(--accent, #3b82f6); color: white; border: none; padding: 10px 18px; border-radius: 30px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.15); display: flex; align-items: center; gap: 8px; font-size: 0.9rem; transition: transform 0.2s;';
          
          installBtn.onmouseover = () => installBtn.style.transform = 'scale(1.05)';
          installBtn.onmouseout = () => installBtn.style.transform = 'scale(1)';
          
          installBtn.addEventListener('click', async () => {
            if (deferredPrompt) {
              deferredPrompt.prompt();
              const {{ outcome }} = await deferredPrompt.userChoice;
              if (outcome === 'accepted') {
                console.log('User accepted the install prompt');
              }
              deferredPrompt = null;
              installBtn.remove();
            }
          });
          document.body.appendChild(installBtn);
        }
      });
    </script>
"""
        manifest_data = {
            "name": app_name,
            "short_name": app_name,
            "start_url": "/",
            "display": "standalone",
            "background_color": "#f1f2f3",
            "theme_color": "#f1f2f3",
            "icons": [
                {
                    "src": user_logo,
                    "sizes": "192x192",
                    "type": "image/png"
                },
                {
                    "src": user_logo,
                    "sizes": "512x512",
                    "type": "image/png"
                }
            ]
        }
        with open(os.path.join(dist_dir, 'manifest.json'), 'w', encoding='utf-8') as f:
            json.dump(manifest_data, f, indent=4)
        
        sw_content = f"""
const CACHE_NAME = 'metupy-pwa-cache-v1';
const urlsToCache = ['/', '/index.html', '/manifest.json', '{user_logo}'];

self.addEventListener('install', event => {{
    event.waitUntil(
        caches.open(CACHE_NAME).then(async cache => {{
            for (const url of urlsToCache) {{
                try {{
                    await cache.add(url);
                }} catch (err) {{
                    console.warn('Failed to cache:', url, err);
                }}
            }}
        }})
    );
}});

self.addEventListener('fetch', event => {{
    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request))
    );
}});
"""
        with open(os.path.join(dist_dir, 'sw.js'), 'w', encoding='utf-8') as f:
            f.write(sw_content.strip())
        
        click.secho("PWA successfully configured with user config logo & custom install banner!", fg='cyan')

    for route, page_obj in app._routes.items():
        rel_path = route.strip('/')
        
        if not rel_path or rel_path == 'index':
            out_file = os.path.join(dist_dir, 'index.html')
        else:
            out_file = os.path.join(dist_dir, rel_path, 'index.html')

        os.makedirs(os.path.dirname(out_file), exist_ok=True)

        raw_content = page_obj.render() if hasattr(page_obj, 'render') else str(page_obj)

        if markdown:
            rendered_content = markdown.markdown(
                raw_content, 
                extensions=['fenced_code', 'tables', 'toc', 'attr_list']
            )
        else:
            rendered_content = raw_content

        title = getattr(page_obj, 'page_title', rel_path.replace('_', ' ').replace('-', ' ').title() or 'Home')
        sidebar_html = generate_ssg_sidebar(route)

        html_output = template.render(
            title=title,
            config=app.config,
            default_css=default_css,
            default_js=default_js,
            sidebar_links=sidebar_html,
            content=rendered_content,
            search_index_json=search_index_json,
            is_dev=False,
            server_start_time=""
        )

        if enable_pwa:
            html_output = html_output.replace('</head>', f"{pwa_head_tags}\n</head>")
            html_output = html_output.replace('</body>', f"{pwa_body_tags}\n</body>")

        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(html_output)

    error_404_content = """
    <div style="text-align: center; padding: 10vh 1rem;">
        <h1 style="font-size: 5rem; margin-bottom: 0.5rem; color: var(--text-main);">404</h1>
        <h2 style="font-size: 1.5rem; font-weight: 500; margin-bottom: 2rem;">Page Not Found</h2>
        <p style="margin-bottom: 2rem; color: var(--text-muted);">Halaman yang kamu tuju tidak ditemukan atau URL-nya salah.</p>
        <a href="/" style="padding: 0.75rem 1.5rem; background: var(--accent); color: white; text-decoration: none; border-radius: 6px; font-weight: 600;">Kembali ke Beranda</a>
    </div>
    """
    
    html_404_output = template.render(
        title="404 Not Found",
        config=app.config,
        default_css=default_css,
        default_js=default_js,
        sidebar_links=generate_ssg_sidebar("/404"),
        content=error_404_content,
        search_index_json=search_index_json,
        is_dev=False,
        server_start_time=""
    )
    
    if enable_pwa:
        html_404_output = html_404_output.replace('</head>', f"{pwa_head_tags}\n</head>")
        html_404_output = html_404_output.replace('</body>', f"{pwa_body_tags}\n</body>")
    
    with open(os.path.join(dist_dir, '404.html'), 'w', encoding='utf-8') as f:
        f.write(html_404_output)

    if custom_domain_value:
        cname_path = os.path.join(dist_dir, 'CNAME')
        with open(cname_path, 'w', encoding='utf-8') as f:
            f.write(custom_domain_value)
        click.secho(f"Custom domain CNAME file created: {custom_domain_value}", fg='cyan')

    click.secho("Static HTML build successful! Output saved in ./dist/", fg='green', bold=True)

if __name__ == "__main__":
    cli()
