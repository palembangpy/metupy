class Modal:
    def __init__(self, id_name, title, content, trigger_text="Buka Modal"):
        self.id_name = id_name
        self.title = title
        self.content = content
        self.trigger_text = trigger_text

    def __str__(self):
        return f'''<div x-data="{{ {self.id_name}: false }}" style="display: inline-block;">
<button class="tab-btn active" @click="{self.id_name} = true">{self.trigger_text}</button>
<template x-teleport="body">
<div class="modal-wrapper" x-show="{self.id_name}" x-cloak>
<div class="modal-backdrop-bg" @click="{self.id_name} = false" x-transition.opacity></div>
<div class="modal-card" x-transition>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.75rem;">
<h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: var(--text-main);">{self.title}</h3>
<button @click="{self.id_name} = false" style="background: none; border: none; font-size: 1.5rem; color: var(--text-muted); cursor: pointer;">&times;</button>
</div>
<div style="color: var(--text-main); font-size: 0.95rem; margin-bottom: 1.5rem; line-height: 1.6;">{self.content}</div>
<div style="display: flex; justify-content: flex-end;">
<button class="tab-btn" style="background: var(--bg-base); border: 1px solid var(--border-color);" @click="{self.id_name} = false">Tutup</button>
</div>
</div>
</div>
</template>
</div>'''
