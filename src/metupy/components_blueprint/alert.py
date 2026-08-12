import markdown


class Alert:

  def __init__(self, message, type="info", title=None):
    self.message = message
    self.type = type
    self.title = title

  def __str__(self):
    # Konfigurasi warna berdasarkan tipe
    themes = {
        "info": {
            "bg": "rgba(59, 130, 246, 0.1)",
            "border": "#3b82f6",
            "color": "#1d4ed8",
        },
        "success": {
            "bg": "rgba(34, 197, 94, 0.1)",
            "border": "#22c55e",
            "color": "#15803d",
        },
        "warning": {
            "bg": "rgba(245, 158, 11, 0.1)",
            "border": "#f59e0b",
            "color": "#b45309",
        },
        "danger": {
            "bg": "rgba(239, 68, 68, 0.1)",
            "border": "#ef4444",
            "color": "#b91c1c",
        },
    }
    theme = themes.get(self.type, themes["info"])

    # Icon SVG
    icons = {
        "info": (
            '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16"'
            ' x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01"'
            ' y2="8"></line>'
        ),
        "success": (
            '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline'
            ' points="22 4 12 14.01 9 11.01"></polyline>'
        ),
        "warning": (
            '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0'
            ' 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9"'
            ' x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01"'
            ' y2="17"></line>'
        ),
        "danger": (
            '<circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9"'
            ' x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line>'
        ),
    }

    title_html = (
        f'<div style="font-weight: 700; margin-bottom:'
        f' 0.25rem;">{self.title}</div>'
        if self.title
        else ""
    )

    # Convert Markdown inside message to HTML & remove wrapping <p> tag
    parsed_msg = markdown.markdown(self.message).strip()
    if parsed_msg.startswith("<p>") and parsed_msg.endswith("</p>"):
      parsed_msg = parsed_msg[3:-4]

    return f"""<div style="background: {theme['bg']}; border-left: 4px solid {theme['border']}; border-radius: 6px; padding: 1rem 1.25rem; margin-bottom: 1.5rem; display: flex; gap: 1rem; align-items: flex-start;">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{theme['border']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0; margin-top: 2px;">{icons[self.type]}</svg>
<div style="color: var(--text-main); font-size: 0.95rem;">
{title_html}
<div style="opacity: 0.9;">{parsed_msg}</div>
</div>
</div>"""
