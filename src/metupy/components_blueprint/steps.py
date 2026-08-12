class Steps:
    def __init__(self, steps_data):
        # steps_data = [{"title": "Step 1", "desc": "Penjelasan"}, ...]
        self.steps_data = steps_data

    def __str__(self):
        items_html = ""
        total = len(self.steps_data)
        for idx, step in enumerate(self.steps_data):
            num = idx + 1
            title = step.get("title", "")
            desc = step.get("desc", "")
            is_last = idx == total - 1
            line_html = '' if is_last else '<div style="position: absolute; top: 32px; left: 15px; bottom: -12px; width: 2px; background: var(--border-color, #e5e7eb);"></div>'

            items_html += f"""<div style="position: relative; display: flex; gap: 1rem; margin-bottom: 1.25rem;">
{line_html}
<div style="width: 32px; height: 32px; border-radius: 50%; background: var(--primary-color, #3b82f6); color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; flex-shrink: 0; z-index: 1;">{num}</div>
<div style="padding-top: 2px;">
<div style="font-weight: 600; color: var(--text-main); font-size: 1rem; margin-bottom: 0.25rem;">{title}</div>
<div style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.5;">{desc}</div>
</div>
</div>"""

        return f"""<div style="margin: 1.5rem 0;">
{items_html}
</div>"""
