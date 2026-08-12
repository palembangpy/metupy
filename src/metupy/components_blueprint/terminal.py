class Terminal:
    def __init__(self, code, title="Terminal", lang="bash"):
        self.code = code
        self.title = title
        self.lang = lang

    def __str__(self):
        return f"""<div class="metupy-terminal" style="background: #1e1e2e; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; margin: 1.25rem 0; overflow: hidden; font-family: monospace;">
<div style="background: rgba(0, 0, 0, 0.25); padding: 0.5rem 1rem; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
<div style="display: flex; align-items: center; gap: 6px;">
<span style="width: 10px; height: 10px; border-radius: 50%; background: #ff5f56; display: inline-block;"></span>
<span style="width: 10px; height: 10px; border-radius: 50%; background: #ffbd2e; display: inline-block;"></span>
<span style="width: 10px; height: 10px; border-radius: 50%; background: #27c93f; display: inline-block;"></span>
<span style="color: #a6adc8; font-size: 0.8rem; margin-left: 8px;">{self.title}</span>
</div>
<button onclick="copyMetupyCode(this)" style="background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.15); color: #cdd6f4; border-radius: 4px; padding: 3px 8px; font-size: 0.75rem; cursor: pointer; display: flex; align-items: center; gap: 4px;">
<span>Copy</span>
</button>
</div>
<pre style="margin: 0; padding: 1rem; overflow-x: auto;"><code class="language-{self.lang}" style="color: #cdd6f4; font-size: 0.9rem;">{self.code}</code></pre>
</div>"""
