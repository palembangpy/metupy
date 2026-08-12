class Badge:
    def __init__(self, text, type="primary", rounded=False):
        self.text = text
        self.type = type
        self.rounded = rounded

    def __str__(self):
        colors = {
            "primary": {"bg": "var(--accent)", "text": "#ffffff"},
            "secondary": {"bg": "var(--bg-surface)", "text": "var(--text-main)", "border": "var(--border-color)"},
            "danger": {"bg": "#ef4444", "text": "#ffffff"},
            "success": {"bg": "#22c55e", "text": "#ffffff"}
        }
        theme = colors.get(self.type, colors["primary"])
        border = f"1px solid {theme.get('border', theme['bg'])}"
        radius = "9999px" if self.rounded else "4px"
        
        return f'<span style="background: {theme["bg"]}; color: {theme["text"]}; border: {border}; padding: 0.15rem 0.5rem; font-size: 0.75rem; font-weight: 600; border-radius: {radius}; display: inline-flex; align-items: center; justify-content: center; vertical-align: middle;">{self.text}</span>'
