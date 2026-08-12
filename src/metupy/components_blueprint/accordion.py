class Accordion:
    def __init__(self, items):
        """
        items: List of dictionaries dengan format [{'title': 'Judul', 'content': 'Isi'}]
        """
        self.items = items

    def __str__(self):
        html = '<div style="border: 1px solid var(--border-color); border-radius: 8px; overflow: hidden; margin-bottom: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.02); max-width: 100%; box-sizing: border-box;">\n'
        
        for idx, item in enumerate(self.items):
            border_bottom = 'border-bottom: 1px solid var(--border-color);' if idx < len(self.items) - 1 else ''
            title = item.get('title', 'Untitled')
            content = item.get('content', '')
            
            # FIX: Rapat kiri
            html += f"""<div x-data="{{ open: false }}" style="{border_bottom}">
<button @click="open = !open" style="width: 100%; box-sizing: border-box; padding: 1rem 1.25rem; text-align: left; background: var(--bg-surface); border: none; color: var(--text-main); font-weight: 600; font-size: 1rem; display: flex; justify-content: space-between; align-items: center; cursor: pointer; transition: background 0.2s;" onmouseover="this.style.background='var(--bg-base)'" onmouseout="this.style.background='var(--bg-surface)'">
<span>{title}</span>
<svg :style="open ? 'transform: rotate(180deg); transition: transform 0.3s;' : 'transition: transform 0.3s;'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--text-muted); flex-shrink: 0; margin-left: 10px;"><polyline points="6 9 12 15 18 9"></polyline></svg>
</button>
<div x-show="open" x-collapse>
<div style="padding: 1.25rem; background: var(--bg-base); color: var(--text-main); font-size: 0.95rem; border-top: 1px dashed var(--border-color); line-height: 1.6; box-sizing: border-box;">
{content}
</div>
</div>
</div>\n"""
        html += '</div>'
        return html
