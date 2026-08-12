# File: ./components/hero.py

class Hero:
    """Komponen UI Hero Modern ala Shadcn."""
    
    def __init__(self, badge: str, title: str, highlight: str, desc: str):
        self.badge = badge
        self.title = title
        self.highlight = highlight
        self.desc = desc

    def __str__(self):
        return f"""
<div class="hero" style="text-align: center; padding: 4rem 1rem;">
    <div class="hero-badge" style="display: inline-block; padding: 6px 12px; background: rgba(59, 130, 246, 0.15); color: #3b82f6; border-radius: 20px; font-size: 0.85rem; font-weight: 600; margin-bottom: 1.5rem; border: 1px solid rgba(59, 130, 246, 0.3);">
        ✨ {self.badge}
    </div>
    <h1 class="hero-title" style="font-size: 3.5rem; font-weight: 800; line-height: 1.1; margin-bottom: 1.5rem; letter-spacing: -0.04em; margin-top: 0;">
        <span style="background: linear-gradient(135deg, #fff, #a1a1aa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{self.title}</span> <br>
        <span style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{self.highlight}</span>
    </h1>
    <p class="hero-desc" style="font-size: 1.2rem; color: #a1a1aa; max-width: 600px; margin: 0 auto 2.5rem; line-height: 1.6;">
        {self.desc}
    </p>
</div>
"""
