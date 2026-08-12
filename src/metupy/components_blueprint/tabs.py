class Tabs:
    def __init__(self, items):
        self.items = items

    def __str__(self):
        buttons_html = ""
        panels_html = ""

        for idx, item in enumerate(self.items):
            title = item[0] if isinstance(item, (tuple, list)) else item.get("title", f"Tab {idx+1}")
            content = item[1] if isinstance(item, (tuple, list)) else item.get("content", "")
            
            escaped_content = content.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$').replace('"', '&quot;')

            buttons_html += f'<button class="tab-btn" :class="{{ \'active\': active === {idx} }}" @click="active = {idx}">{title}</button>'
            
            panels_html += f'''<div class="tab-panel" x-show="active === {idx}" x-cloak>
<button class="tab-copy-btn" @click="navigator.clipboard.writeText(`{escaped_content}`); copied = {idx}; setTimeout(() => copied = null, 2000)">
<span x-text="copied === {idx} ? '✓ Copied' : 'Copy'">Copy</span>
</button>
<pre><code>{content}</code></pre>
</div>'''

        return f'''<div class="metupy-tabs" x-data="{{ active: 0, copied: null }}">
<div class="tabs-header">{buttons_html}</div>
{panels_html}
</div>'''
