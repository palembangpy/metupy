import html


class Page:

    def __init__(self, title="Untitled"):
        self.page_title = title
        self._content = []

    def __iadd__(self, component):
        self._content.append(f"{str(component)}\n\n")
        return self

    def title(self, text: str):
        self._content.append(f"# {text}\n\n")

    def subtitle(self, text: str):
        self._content.append(f"### {text}\n\n")

    def text(self, content: str):
        self._content.append(f"{content}\n\n")

    def info(self, content: str):
        self._content.append(f"> **💡 Info:** {content}\n\n")

    def raw(self, content: str):
        """Menambahkan HTML/Markdown mentah langsung ke dalam halaman."""
        self._content.append(f"{content}\n\n")

    def code(self, code: str, lang: str = "text", filename: str = ""):
        safe_code = html.escape(code.strip())
        display_title = filename if filename else lang.lower()

        terminal_html = f"""
<div class="metupy-terminal">
    <div class="terminal-header">
        <div class="terminal-dots">
            <span class="dot close"></span>
            <span class="dot minimize"></span>
            <span class="dot expand"></span>
        </div>
        <div class="terminal-title">{display_title}</div>
        <button class="terminal-copy" onclick="copyMetupyCode(this)">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            <span>Copy</span>
        </button>
    </div>
    <div class="terminal-body">
        <pre><code class="language-{lang}">{safe_code}</code></pre>
    </div>
</div>
"""
        self._content.append(f"{terminal_html}\n\n")

    def render(self) -> str:
        return "".join(self._content)
