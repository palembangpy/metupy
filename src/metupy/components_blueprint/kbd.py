class Kbd:
    def __init__(self, keys):
        self.keys = keys if isinstance(keys, list) else [keys]

    def __str__(self):
        keys_html = [f'<kbd>{k}</kbd>' for k in self.keys]
        return f'<span style="display: inline-flex; gap: 4px; align-items: center; margin: 0 2px;">{" + ".join(keys_html)}</span>'
