class Card:
    def __init__(self, content, title=None, subtitle=None, footer=None, image_top=None, image_bottom=None, width="100%"):
        self.title = title
        self.subtitle = subtitle
        self.content = content
        self.footer = footer
        self.image_top = image_top
        self.image_bottom = image_bottom
        self.width = width

    def __str__(self):
        title_html = f'<h3 style="margin-top: 0; margin-bottom: 0.25rem; color: var(--text-main); font-size: 1.25rem;">{self.title}</h3>' if self.title else ''
        subtitle_html = f'<div style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1rem;">{self.subtitle}</div>' if self.subtitle else ''
        img_top_html = f'<img src="{self.image_top}" style="width: 100%; height: auto; object-fit: cover; border-bottom: 1px solid var(--border-color);">' if self.image_top else ''
        img_bot_html = f'<img src="{self.image_bottom}" style="width: 100%; height: auto; object-fit: cover; border-top: 1px solid var(--border-color);">' if self.image_bottom else ''
        footer_html = f'<div style="padding: 1rem 1.5rem; border-top: 1px solid var(--border-color); background: var(--bg-base); font-size: 0.85rem; color: var(--text-muted);">{self.footer}</div>' if self.footer else ''
        
        # FIX: Tambahkan max-width: 100% dan box-sizing: border-box, serta rapat kiri untuk Markdown
        return f"""<div style="border: 1px solid var(--border-color); border-radius: 12px; background: var(--bg-surface); overflow: hidden; width: {self.width}; max-width: 100%; box-sizing: border-box; box-shadow: 0 4px 12px rgba(0,0,0,0.03); margin-bottom: 1.5rem; display: flex; flex-direction: column;">
{img_top_html}
<div style="padding: 1.5rem; flex: 1; box-sizing: border-box;">
{title_html}
{subtitle_html}
<div style="color: var(--text-main); font-size: 0.95rem; line-height: 1.6;">{self.content}</div>
</div>
{img_bot_html}
{footer_html}
</div>"""
