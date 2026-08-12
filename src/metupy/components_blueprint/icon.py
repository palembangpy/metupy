class Icon:
    def __init__(self, name, size="md", color="inherit", position="left"):
        self.name = name
        self.size = size
        self.color = color
        self.position = position
        
        # Mapping size
        self.sizes = {"sm": "0.8rem", "md": "1.2rem", "lg": "1.8rem", "xl": "2.5rem"}

    def __str__(self):
        size_px = self.sizes.get(self.size, "1.2rem")
        return f'<i class="metupy-icon {self.name}" style="font-size: {size_px}; color: {self.color}; display: inline-block; vertical-align: middle; margin-{self.position}: 8px; margin-right: 8px;"></i>'
