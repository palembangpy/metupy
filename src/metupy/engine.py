import importlib.util
import json
import os
import re
import sys
import time

from flask import Flask, abort, jsonify, render_template_string, send_from_directory
import markdown

if sys.version_info >= (3, 11):
    import tomllib as toml
else:
    import toml


class MetupyServer:
    def __init__(self, project_dir="."):
        self.project_dir = os.path.abspath(project_dir)
        self.pages_dir = os.path.join(self.project_dir, "pages")
        self.assets_dir = os.path.join(self.project_dir, "assets")
        
        self.server_start_time = str(time.time())
        self.is_dev = False
        
        self.config = {
            "name": "Metupy",
            "theme": "default",
            "use_search": True,
            "use_darkmode": True,
            "icon_cdn": "",
            "logo": "",
            "favicon": ""
        }
        self._load_config()
        
        self.app = Flask(__name__)
            
        self._routes = {} 
        self._tree = {}
        
        if self.project_dir not in sys.path:
            sys.path.insert(0, self.project_dir)
            
        self._scan_pages()
        self._setup_routes()

    def _load_config(self):
        toml_path = os.path.join(self.project_dir, "pyproject.toml")
        if os.path.exists(toml_path):
            mode = "rb" if sys.version_info >= (3, 11) else "r"
            with open(toml_path, mode) as f:
                data = toml.load(f)
                
                self.config["name"] = data.get("project", {}).get("name", "Metupy")
                
                meta = data.get("tool", {}).get("metupy", {})
                self.config.update({k: v for k, v in meta.items() if k != 'icons'})
                self.config["theme"] = meta.get("theme", "default")
                self.config["icon_cdn"] = meta.get("icons", {}).get("cdn_url", "")

    def _scan_pages(self):
        if not os.path.exists(self.pages_dir):
            return
        
        for root, dirs, files in os.walk(self.pages_dir):
            for file in files:
                if file.endswith('.py') and file != 'metupy.py':
                    rel_dir = os.path.relpath(root, self.pages_dir).replace('\\', '/')
                    if rel_dir == ".":
                        rel_dir = "root"
                    
                    if rel_dir not in self._tree:
                        self._tree[rel_dir] = []
                        
                    file_path = os.path.join(root, file)
                    spec = importlib.util.spec_from_file_location("mod", file_path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)

                    if hasattr(mod, 'page'):
                        route = "/" + os.path.relpath(file_path, self.pages_dir).replace("\\", "/").replace(".py", "")
                        if route.endswith("/index"):
                            route = route[:-6]
                        if route == "":
                            route = "/"
                        
                        self._routes[route] = mod.page
                        self._tree[rel_dir].append({
                            "route": route, 
                            "title": getattr(mod.page, 'page_title', 'Untitled')
                        })

    def _setup_routes(self):
        theme_name = self.config.get("theme", "default")
        
        user_theme_dir = os.path.join(self.project_dir, "templates", theme_name)
        lib_theme_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", theme_name)
        
        if os.path.exists(user_theme_dir):
            active_theme_dir = user_theme_dir
        elif os.path.exists(lib_theme_dir):
            active_theme_dir = lib_theme_dir
        else:
            fallback_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "default")
            active_theme_dir = fallback_dir

        layout_path = os.path.join(active_theme_dir, "layout.html")
        css_path = os.path.join(active_theme_dir, "style.css")
        js_path = os.path.join(active_theme_dir, "script.js")

        if not os.path.exists(layout_path):
            raise FileNotFoundError(f"Layout file 'layout.html' not found in theme '{theme_name}'")

        with open(layout_path, "r", encoding="utf-8") as f:
            HTML_TEMPLATE = f.read()

        default_css = ""
        if os.path.exists(css_path):
            with open(css_path, "r", encoding="utf-8") as f:
                default_css = f.read()

        default_js = ""
        if os.path.exists(js_path):
            with open(js_path, "r", encoding="utf-8") as f:
                default_js = f.read()

        @self.app.route('/__metupy_livereload')
        def livereload():
            return jsonify({"version": self.server_start_time})
            
        @self.app.route('/assets/<path:filename>')
        def serve_user_assets(filename):
            return send_from_directory(self.assets_dir, filename)

        @self.app.route('/', defaults={'path': ''})
        @self.app.route('/<path:path>')
        def render_page(path):
            route_path = f"/{path}" if path else "/"
            if route_path != "/" and route_path.endswith("/"):
                route_path = route_path[:-1]
            if route_path not in self._routes:
                abort(404)

            page_obj = self._routes[route_path]
            
            # Navigation links
            sidebar_html = ""
            for folder, pages in self._tree.items():
                if folder == "root":
                    for p in pages:
                        active_class = 'active' if route_path == p["route"] else ""
                        sidebar_html += f'<a class="menu-link {active_class}" href="{p["route"]}" @click="sidebarOpen = false">{p["title"]}</a>\n'
                else:
                    is_active_group = any(route_path == p["route"] for p in pages)
                    open_state = 'true' if is_active_group else 'false'
                    folder_title = folder.replace('-', ' ').replace('_', ' ').title()
                    
                    sidebar_html += f'''
                    <div x-data="{{ open: {open_state} }}" style="margin-bottom: 4px;">
                        <button @click="open = !open" class="menu-link dropdown-btn" :class="{{ 'active': open }}">
                            <span style="font-weight: 600;">{folder_title}</span>
                            <svg class="chevron" :class="{{ 'rotate': open }}" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
                        </button>
                        <div x-show="open" x-collapse class="dropdown-menu">
                    '''
                    for p in pages:
                        active_class = 'active' if route_path == p["route"] else ""
                        sidebar_html += f'<a class="menu-link {active_class}" href="{p["route"]}" @click="sidebarOpen = false">{p["title"]}</a>\n'
                    sidebar_html += '</div></div>\n'

            # Search index
            search_data = []
            for r, p_obj in self._routes.items():
                raw_md = p_obj.render()
                clean_text = re.sub(r'<[^>]+>', '', raw_md)
                clean_text = re.sub(r'#+\s', '', clean_text)
                clean_text = re.sub(r'[\*\_\`\>\[\]\(\)]', '', clean_text)
                clean_text = " ".join(clean_text.split())
                search_data.append({
                    "url": r,
                    "title": getattr(p_obj, 'page_title', 'Untitled'),
                    "content": clean_text
                })

            md_content = page_obj.render()
            
            # Markdown processing
            html_content = markdown.markdown(
                md_content, 
                extensions=['fenced_code', 'tables', 'toc', 'attr_list']
            )

            return render_template_string(
                HTML_TEMPLATE,
                title=getattr(page_obj, 'page_title', 'Untitled'),
                sidebar_links=sidebar_html,
                content=html_content,
                is_dev=self.is_dev,
                server_start_time=self.server_start_time,
                config=self.config,
                search_index_json=json.dumps(search_data),
                default_css=default_css,
                default_js=default_js
            )

    def run(self, port=5000):
        self.is_dev = True
        watch_files = [os.path.join(self.project_dir, 'pyproject.toml')]
        if os.path.exists(self.pages_dir):
            for root, _, files in os.walk(self.pages_dir):
                for f in files:
                    if f.endswith('.py'):
                        watch_files.append(os.path.join(root, f))
                        
        self.app.run(port=port, debug=True, extra_files=watch_files)
