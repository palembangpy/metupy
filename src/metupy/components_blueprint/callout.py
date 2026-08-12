class Callout:
    def __init__(self, message, title=None, type="info"):
        self.message = message
        self.title = title
        self.type = type

    def __str__(self):
        themes = {
            "info": {"border": "#3b82f6", "bg": "rgba(59, 130, 246, 0.08)", "title": "#1d4ed8"},
            "tip": {"border": "#10b981", "bg": "rgba(16, 185, 129, 0.08)", "title": "#047857"},
            "warning": {"border": "#f59e0b", "bg": "rgba(245, 158, 11, 0.08)", "title": "#b45309"},
            "danger": {"border": "#ef4444", "bg": "rgba(239, 68, 68, 0.08)", "title": "#b91c1c"}
        }
        theme = themes.get(self.type, themes["info"])
        title_html = f'<strong style="display: block; color: {theme["title"]}; margin-bottom: 0.25rem;">{self.title}</strong>' if self.title else ''

        return f"""<div style="background: {theme['bg']}; border-left: 4px solid {theme['border']}; border-radius: 0 8px 8px 0; padding: 1rem 1.25rem; margin: 1.25rem 0;">
{title_html}
<div style="color: var(--text-main); font-size: 0.95rem; line-height: 1.6;">{self.message}</div>
</div>"""
