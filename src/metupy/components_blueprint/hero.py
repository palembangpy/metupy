class Hero:
    def __init__(self, title="", highlight="", desc="", logo=None, actions=None, model=1):
        self.title = title
        self.highlight = highlight
        self.desc = desc
        self.logo = logo
        self.actions = actions
        self.model = model

    def __str__(self):
        logo_html = ""
        if self.logo:
            logo_html = f'''
        <div style="position: relative; z-index: 1; margin-bottom: 2rem; display: inline-block;">
            <div style="position: absolute; inset: -6px; background: linear-gradient(135deg, #3b82f6, #6366f1); filter: blur(16px); opacity: 0.2; border-radius: 20px;"></div>
            <img src="{self.logo}" alt="Hero Logo" style="position: relative; max-width: 170px; height: auto; filter: drop-shadow(0 12px 24px rgba(0, 0, 0, 0.15)); transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.04)'" onmouseout="this.style.transform='scale(1)'">
        </div>
            '''

        actions_alignment = 'center' if self.model in [3, 5] else 'center'
        actions_html = ""
        if self.actions:
            actions_html = f'''
        <div style="display: flex; gap: 1rem; justify-content: {actions_alignment}; align-items: center; flex-wrap: wrap; margin-top: 2rem;">
            {self.actions}
        </div>
            '''

        # Model 1: Centered with Radial Glow (Classic Default)
        if self.model == 1:
            return f'''<div class="hero-wrapper" style="position: relative; text-align: center; padding: 4rem 1rem 3rem 1rem; overflow: hidden;">
    <div style="position: absolute; top: 35%; left: 50%; transform: translate(-50%, -50%); width: 260px; height: 260px; background: radial-gradient(circle, rgba(55, 118, 171, 0.22) 0%, rgba(255, 212, 59, 0.12) 55%, transparent 75%); filter: blur(35px); pointer-events: none; z-index: 0;"></div>
    
    <div style="position: relative; z-index: 1;">
        {logo_html}
        <h1 style="font-size: clamp(2.5rem, 6vw, 3.8rem); font-weight: 800; line-height: 1.15; letter-spacing: -0.03em; margin: 0 0 1.25rem 0;">
            <span style="color: var(--text-main, #ffffff);">{self.title}</span><br>
            <span style="background: linear-gradient(135deg, #4B8BBE 0%, #3776AB 40%, #FFD43B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{self.highlight}</span>
        </h1>
        <p style="font-size: clamp(1.05rem, 2.5vw, 1.25rem); color: var(--text-muted, #9ca3af); max-width: 650px; margin: 0 auto; line-height: 1.6; font-weight: 400;">
            {self.desc}
        </p>
        {actions_html}
    </div>
</div>'''

        # Model 2: Vercel Style (Grid background texture with announcement pill badge)
        elif self.model == 2:
            return f'''<div class="hero-wrapper" style="position: relative; text-align: center; padding: 5rem 1rem 4rem 1rem; background-image: radial-gradient(var(--border-color, #27272a) 1px, transparent 1px); background-size: 32px 32px; overflow: hidden;">
    <div style="position: absolute; top: 0; left: 0; right: 0; height: 100%; background: radial-gradient(circle at 50% 20%, rgba(55, 118, 171, 0.15) 0%, transparent 60%); pointer-events: none;"></div>
    
    <div style="position: relative; z-index: 1; max-width: 800px; margin: 0 auto;">
        <div style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.35rem 0.9rem; background: rgba(255,255,255,0.03); border: 1px solid var(--border-color, #27272a); border-radius: 9999px; font-size: 0.85rem; color: var(--text-muted); margin-bottom: 2rem; backdrop-filter: blur(8px);">
            <span style="background: linear-gradient(135deg, #3776AB, #FFD43B); color: #000; font-weight: 700; font-size: 0.7rem; padding: 0.1rem 0.5rem; border-radius: 9999px;">NEW</span>
            <span>Explore the latest release features</span>
        </div>
        {logo_html}
        <h1 style="font-size: clamp(2.6rem, 6.5vw, 4.2rem); font-weight: 800; line-height: 1.1; letter-spacing: -0.04em; margin: 0 0 1.25rem 0;">
            <span style="color: var(--text-main, #ffffff);">{self.title}</span><br>
            <span style="background: linear-gradient(135deg, #4B8BBE 0%, #3776AB 40%, #FFD43B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{self.highlight}</span>
        </h1>
        <p style="font-size: clamp(1.1rem, 2.3vw, 1.25rem); color: var(--text-muted, #9ca3af); max-width: 650px; margin: 0 auto; line-height: 1.6; font-weight: 400;">
            {self.desc}
        </p>
        {actions_html}
    </div>
</div>'''

        # Model 3: Laravel-Inspired Minimalist Clean Centered Style
        elif self.model == 3:
            return f'''<div class="hero-wrapper" style="position: relative; text-align: center; padding: 5rem 1rem 4rem 1rem; max-width: 850px; margin: 0 auto; overflow: hidden;">
    <div style="position: relative; z-index: 1;">
        {logo_html}
        <h1 style="font-size: clamp(2.7rem, 6.5vw, 4.2rem); font-weight: 800; line-height: 1.12; letter-spacing: -0.035em; margin: 0 auto 1.5rem auto;">
            <span style="color: var(--text-main, #ffffff);">{self.title}</span><br>
            <span style="color: var(--text-main, #ffffff);">{self.highlight}</span>
        </h1>
        <p style="font-size: clamp(1.1rem, 2.4vw, 1.25rem); color: var(--text-muted, #9ca3af); max-width: 600px; margin: 0 auto; line-height: 1.65; font-weight: 400;">
            {self.desc}
        </p>
        <div style="display: flex; gap: 1rem; justify-content: center; align-items: center; flex-wrap: wrap; margin-top: 2.5rem;">
            {self.actions if self.actions else ''}
        </div>
    </div>
</div>'''

        # Model 4: Split Grid with Visual Component Card (Text left, Graphic card right)
        elif self.model == 4:
            right_side = f'''<div style="flex: 1; display: flex; justify-content: center; align-items: center; min-width: 260px;">
        <div style="width: 100%; max-width: 340px; padding: 2rem; background: var(--bg-base, #0d0d12); border: 1px solid var(--border-color, #2a2a3c); border-radius: 16px; box-shadow: 0 16px 32px rgba(0,0,0,0.3); text-align: center;">
            <img src="{self.logo}" alt="Hero Logo" style="max-width: 120px; height: auto; filter: drop-shadow(0 8px 16px rgba(0,0,0,0.4)); margin-bottom: 1rem;">
            <div style="font-size: 0.9rem; color: var(--text-muted); font-weight: 500;">Powering Modern Systems</div>
        </div>
    </div>''' if self.logo else '<div style="flex: 1;"></div>'

            return f'''<div class="hero-wrapper" style="position: relative; padding: 4rem 1rem; max-width: 1100px; margin: 0 auto;">
    <div style="display: flex; gap: 3rem; align-items: center; flex-wrap: wrap;">
        <div style="flex: 1.2; min-width: 280px; text-align: left;">
            <h1 style="font-size: clamp(2.3rem, 5vw, 3.5rem); font-weight: 800; line-height: 1.15; letter-spacing: -0.03em; margin: 0 0 1.25rem 0;">
                <span style="color: var(--text-main, #ffffff);">{self.title}</span><br>
                <span style="background: linear-gradient(135deg, #4B8BBE 0%, #3776AB 40%, #FFD43B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{self.highlight}</span>
            </h1>
            <p style="font-size: clamp(1rem, 2vw, 1.15rem); color: var(--text-muted, #9ca3af); line-height: 1.6; font-weight: 400; margin: 0 0 1.5rem 0;">
                {self.desc}
            </p>
            {actions_html}
        </div>
        {right_side}
    </div>
</div>'''

        # Model 5: Clean, Simple, Modern & Adaptive (Adapts seamlessly to light/dark mode via CSS variables)
        elif self.model == 5:
            return f'''<div class="hero-wrapper" style="position: relative; text-align: center; padding: 5rem 1.5rem 4rem 1.5rem; background: var(--bg-base, #ffffff); color: var(--text-main, #111827); overflow: hidden; transition: background 0.3s ease, color 0.3s ease;">
    <div style="position: absolute; top: 0; left: 50%; transform: translateX(-50%); width: 100%; max-width: 900px; height: 100%; background: radial-gradient(circle at 50% 20%, rgba(59, 130, 246, 0.05) 0%, transparent 60%); pointer-events: none;"></div>
    
    <div style="position: relative; z-index: 1; max-width: 800px; margin: 0 auto;">
        {logo_html}
        <h1 style="font-size: clamp(2.6rem, 6.5vw, 4.2rem); font-weight: 800; line-height: 1.12; letter-spacing: -0.035em; margin: 0 0 1.25rem 0;">
            <span style="color: var(--text-main, #111827);">{self.title}</span><br>
            <span style="background: linear-gradient(135deg, #2563eb 0%, #3b82f6 50%, #6366f1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{self.highlight}</span>
        </h1>
        <p style="font-size: clamp(1.05rem, 2.3vw, 1.2rem); color: var(--text-muted, #4b5563); max-width: 650px; margin: 0 auto 2.2rem auto; line-height: 1.6; font-weight: 400;">
            {self.desc}
        </p>
        <div style="display: flex; gap: 1rem; justify-content: center; align-items: center; flex-wrap: wrap;">
            {self.actions if self.actions else ''}
        </div>
    </div>
</div>'''

        # Fallback to Model 1
        return self.__str__()
