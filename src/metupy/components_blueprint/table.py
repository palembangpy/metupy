class Table:
    def __init__(self, headers, rows):
        self.headers = headers
        self.rows = rows

    def __str__(self):
        th_html = "".join([f'<th style="padding: 0.75rem 1rem; text-align: left; border-bottom: 2px solid var(--border-color, #e5e7eb); font-weight: 600; color: var(--text-main);">{h}</th>' for h in self.headers])
        
        tr_html = ""
        for row in self.rows:
            td_html = "".join([f'<td style="padding: 0.75rem 1rem; border-bottom: 1px solid var(--border-color, #e5e7eb); color: var(--text-main);">{cell}</td>' for cell in row])
            tr_html += f'<tr>{td_html}</tr>\n'

        return f"""<div style="overflow-x: auto; margin: 1.5rem 0; border: 1px solid var(--border-color, #e5e7eb); border-radius: 8px;">
<table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
<thead style="background: var(--bg-secondary, rgba(0,0,0,0.02));">
<tr>{th_html}</tr>
</thead>
<tbody>
{tr_html}</tbody>
</table>
</div>"""
