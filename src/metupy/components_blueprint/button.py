class Button:
    def __init__(self, text, width="auto", height="40px", icon=None, icon_size="md", icon_position="left", href=None, on_click=None):
        self.text = text
        self.width = width
        self.height = height
        self.icon = icon  
        self.icon_size = icon_size
        self.icon_position = icon_position
        self.href = href
        self.on_click = on_click

    def __str__(self):
        sizes = {"sm": "0.8rem", "md": "1rem", "lg": "1.3rem", "xl": "1.6rem"}
        size_px = sizes.get(self.icon_size, "1rem")
        
        icon_html = ""
        if self.icon:
            # Mengatur jarak margin berdasarkan posisi icon terhadap teks
            margin_side = "right" if self.icon_position == "left" else ("left" if self.icon_position == "right" else "bottom")
            icon_html = f'<i class="{self.icon}" style="font-size: {size_px}; margin-{margin_side}: 8px;"></i>'
        
        # Mengatur arah flexbox tombol berdasarkan posisi icon
        if self.icon_position == "top":
            flex_dir = "column"
        elif self.icon_position == "down":
            flex_dir = "column-reverse"
        elif self.icon_position == "right":
            flex_dir = "row-reverse"
        else:
            flex_dir = "row"

        # Menentukan tag HTML yang digunakan (<a> jika ada href, <button> jika on_click/tanpa aksi)
        tag = "a" if self.href else "button"
        
        # Injeksi aksi (href untuk pindah halaman, onclick untuk aksi JS)
        action_attr = f'href="{self.href}"' if self.href else (f'onclick="{self.on_click}"' if self.on_click else "")

        # Tambahkan styling CSS bawaan ala Metupy
        base_style = f"width: {self.width}; height: {self.height}; padding: 0.75rem; display: inline-flex; align-items: center; justify-content: center; cursor: pointer; flex-direction: {flex_dir}; background: var(--accent); color: #ffffff; border: none; border-radius: 6px; text-decoration: none; font-weight: 500; font-size: 0.95rem; font-family: inherit; transition: opacity 0.2s ease, transform 0.1s ease; box-sizing: border-box;"

        # FIX: String HTML rapat tanpa spasi di awal (Zero Indentation) agar tidak disangka code block oleh Markdown
        return f'<{tag} {action_attr} style="{base_style}" onmouseover="this.style.opacity=\'0.85\'" onmouseout="this.style.opacity=\'1\'" onmousedown="this.style.transform=\'scale(0.97)\'" onmouseup="this.style.transform=\'scale(1)\'">{icon_html}<span>{self.text}</span></{tag}>'
