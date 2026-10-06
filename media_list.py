from pathlib import Path
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageOps


class MediaList(ctk.CTkFrame):
    def __init__(self, parent, selection, changed, opened):
        super().__init__(parent, fg_color='#F3F6F3', corner_radius=16)
        self.selection = selection
        self.changed = changed
        self.opened = opened
        self.drag_path = None
        self.target = None
        self.rows = []
        self.thumbnails = []
        self.body = ctk.CTkScrollableFrame(self, fg_color='transparent', height=310)
        self.body.pack(fill='both', expand=True, padx=4, pady=4)
        self.refresh()

    def refresh(self):
        for child in self.body.winfo_children():
            child.destroy()
        self.rows = []
        self.thumbnails = []
        if not self.selection.items:
            ctk.CTkLabel(self.body, text='Chưa có media. Tạo ảnh/video hoặc thêm file từ máy.',
                         text_color='#6A7B77', height=80).pack(fill='x', padx=10)
        for index, item in enumerate(self.selection.items):
            row = ctk.CTkFrame(self.body, fg_color='white', corner_radius=12, border_width=2, border_color='white')
            row.pack(fill='x', padx=3, pady=4)
            self.rows.append(row)
            grip = ctk.CTkLabel(row, text='☰', width=34, cursor='hand2', font=('Segoe UI', 22), text_color='#6A7B77')
            grip.pack(side='left', padx=(6, 0), pady=10)
            grip.bind('<ButtonPress-1>', lambda event, path=item.path: self.start_drag(path))
            grip.bind('<B1-Motion>', self.drag)
            grip.bind('<ButtonRelease-1>', self.drop)
            chosen = tk.BooleanVar(value=item.selected)
            ctk.CTkCheckBox(row, text='', width=24, variable=chosen,
                            command=lambda entry=item, var=chosen: self.toggle(entry, var.get())).pack(side='left', padx=8)
            photo = None
            if item.kind == 'photo':
                try:
                    with Image.open(item.path) as source:
                        thumb = ImageOps.fit(ImageOps.exif_transpose(source).convert('RGB'), (64, 52))
                    photo = ctk.CTkImage(light_image=thumb, dark_image=thumb, size=(64, 52))
                    self.thumbnails.append(photo)
                except (OSError, ValueError):
                    pass
            ctk.CTkLabel(row, image=photo, text='' if photo else '▶ MP4' if item.kind == 'video' else 'Ảnh', width=68).pack(side='left', padx=6)
            label = ctk.CTkLabel(row, text=f'{index + 1:02d}   {Path(item.path).name}', anchor='w',
                                 font=('Segoe UI', 13), wraplength=430, justify='left')
            label.pack(side='left', fill='x', expand=True, padx=8)
            label.bind('<Double-1>', lambda event, path=item.path: self.opened(path))
            for title, delta in [('↑', -1), ('↓', 1)]:
                ctk.CTkButton(row, text=title, width=30, height=30, fg_color='#E7F1EC', text_color='#183D32',
                               hover_color='#CFDFD5', command=lambda i=index, d=delta: self.move(i, i+d)).pack(side='left', padx=2)
            ctk.CTkButton(row, text='Mở', width=48, height=30, command=lambda path=item.path: self.opened(path)).pack(side='left', padx=(6, 10))
        self.changed()

    def toggle(self, item, value):
        item.selected = bool(value)
        self.changed()

    def move(self, source, target):
        self.selection.move(source, target)
        self.refresh()

    def start_drag(self, path):
        self.drag_path = path
        self.target = None

    def drag(self, event):
        if self.drag_path is None or not self.rows:
            return
        # Scroll the list near its top/bottom while dragging a long collection.
        canvas = self.body._parent_canvas
        top, height = canvas.winfo_rooty(), canvas.winfo_height()
        if event.y_root < top + 22:
            canvas.yview_scroll(-1, 'units')
        elif event.y_root > top + height - 22:
            canvas.yview_scroll(1, 'units')
        self.target = min(range(len(self.rows)), key=lambda i: abs(event.y_root - (self.rows[i].winfo_rooty() + self.rows[i].winfo_height()/2)))
        for i, row in enumerate(self.rows):
            row.configure(border_color='#147D64' if i == self.target else 'white')

    def drop(self, event):
        if self.drag_path is not None and self.target is not None:
            source = next((i for i, item in enumerate(self.selection.items) if item.path == self.drag_path), None)
            if source is not None:
                self.selection.move(source, self.target)
        self.drag_path = None
        self.target = None
        self.refresh()

    def choose_all(self, value):
        for item in self.selection.items:
            item.selected = value
        self.refresh()
