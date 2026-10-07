"""Giao diện nhập sản phẩm trực tiếp, các khối bo góc và vùng cuộn."""
import tkinter as tk
import customtkinter as ctk
from media_list import MediaList
from connection_options import AI_MODELS, FACEBOOK_PAGES, GRAPH_API_VERSIONS

ctk.set_appearance_mode('light')
ctk.set_default_color_theme('green')

INK = '#182E2A'
MUTED = '#6A7B77'
ACCENT = '#147D64'


class StudioUI:
    def label(self, parent, text, size=14, bold=False, **kwargs):
        return ctk.CTkLabel(parent, text=text, text_color=INK,
                            font=ctk.CTkFont(family='Segoe UI', size=size, weight='bold' if bold else 'normal'), **kwargs)

    def button(self, parent, text, command, secondary=False):
        return ctk.CTkButton(parent, text=text, command=command, height=42, corner_radius=12,
                            font=('Segoe UI', 13, 'bold'), fg_color='#E7F1EC' if secondary else ACCENT,
                            text_color=INK if secondary else 'white', hover_color='#CFDFD5' if secondary else '#0C6650')

    def section(self, parent, title, subtitle=None):
        panel = ctk.CTkFrame(parent, fg_color='white', corner_radius=20)
        panel.pack(fill='x', pady=(0, 14))
        self.label(panel, title, 18, True).pack(anchor='w', padx=20, pady=(18, 4))
        if subtitle:
            self.label(panel, subtitle, 12, wraplength=370, justify='left').pack(anchor='w', padx=20, pady=(0, 10))
        return panel

    def build_interface(self):
        self.configure(fg_color='#F2F5F1')
        header = ctk.CTkFrame(self, fg_color='#183D32', corner_radius=22, height=100)
        header.pack(fill='x', padx=22, pady=(20, 10))
        ctk.CTkLabel(header, text='KHÁNH TOÀN  /  CONTENT STUDIO', text_color='#C6F1B3',
                     font=('Segoe UI', 13, 'bold')).pack(anchor='w', padx=24, pady=(18, 0))
        ctk.CTkLabel(header, text='Biến thông tin sản phẩm thành bài viết.', text_color='white',
                     font=('Segoe UI', 25, 'bold')).pack(anchor='w', padx=24, pady=(3, 18))
        self.tabs = ctk.CTkTabview(self, fg_color='#F2F5F1', corner_radius=18,
                                    segmented_button_selected_color=ACCENT,
                                    segmented_button_selected_hover_color='#0C6650')
        self.tabs.pack(fill='both', expand=True, padx=16)
        for tab in ['Soạn nội dung', 'Ảnh & video', 'Kết nối']:
            self.tabs.add(tab)
        self.build_compose(self.tabs.tab('Soạn nội dung'))
        self.build_media(self.tabs.tab('Ảnh & video'))
        self.build_settings(self.tabs.tab('Kết nối'))
        ctk.CTkLabel(self, textvariable=self.vars['status'], text_color=MUTED, anchor='w',
                     font=('Segoe UI', 12), wraplength=1100).pack(fill='x', padx=30, pady=(8, 14))

    def build_compose(self, parent):
        parent.grid_columnconfigure(0, weight=4, uniform='columns')
        parent.grid_columnconfigure(1, weight=5, uniform='columns')
        parent.grid_rowconfigure(0, weight=1)
        left = ctk.CTkScrollableFrame(parent, fg_color='transparent', corner_radius=0)
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 14))
        form = self.section(left, '01   Thông tin sản phẩm', 'Nhập trực tiếp, không cần file Excel hoặc CSV.')
        self.label(form, 'Tên sản phẩm *', bold=True).pack(anchor='w', padx=20, pady=(4, 6))
        self.name_entry = ctk.CTkEntry(form, textvariable=self.vars['product_name'], height=44, corner_radius=12)
        self.name_entry.pack(fill='x', padx=20)
        self.label(form, 'Ví dụ: Laptop Dell Latitude 5420', 12).pack(anchor='w', padx=20, pady=(3, 12))
        self.label(form, 'Mô tả ban đầu', bold=True).pack(anchor='w', padx=20, pady=(0, 6))
        self.description = ctk.CTkTextbox(form, height=120, corner_radius=12, fg_color='#F3F6F3', font=('Segoe UI', 14), wrap='word')
        self.description.pack(fill='x', padx=20)
        self.label(form, 'Cấu hình, đặc điểm, tình trạng hoặc điểm nổi bật.', 12).pack(anchor='w', padx=20, pady=(4, 12))
        self.label(form, 'Giá bán  ·  không bắt buộc', bold=True).pack(anchor='w', padx=20, pady=(0, 6))
        ctk.CTkEntry(form, textvariable=self.vars['product_price'], height=44, corner_radius=12).pack(fill='x', padx=20)
        self.label(form, 'Ví dụ: 8.500.000 đ. Để trống để bỏ phần giá.', 12).pack(anchor='w', padx=20, pady=(4, 18))
        options = self.section(left, '02   Cách viết bài')
        self.label(options, 'Yêu cầu thêm (tùy chọn)', bold=True).pack(anchor='w', padx=20, pady=(4, 6))
        self.extra = ctk.CTkTextbox(options, height=75, corner_radius=12, fg_color='#F3F6F3', font=('Segoe UI', 14), wrap='word')
        self.extra.pack(fill='x', padx=20, pady=(0, 12))
        ctk.CTkOptionMenu(options, variable=self.vars['provider'], values=list(AI_MODELS),
                          height=38, corner_radius=10, fg_color=ACCENT).pack(fill='x', padx=20, pady=(0, 12))
        ctk.CTkSwitch(options, text='Dùng AI viết bài', variable=self.ai_text, progress_color=ACCENT).pack(anchor='w', padx=20)
        self.label(options, 'Tắt: bài mẫu miễn phí. Bật: cần API key có hạn mức.', 12, wraplength=370, justify='left').pack(anchor='w', padx=20, pady=(6, 12))
        self.button(options, 'Tạo văn bản  →', self.generate_text_only).pack(fill='x', padx=20, pady=(0, 8))
        self.label(options, 'Chỉ tạo bản nháp • Không tự đăng Facebook', 12).pack(padx=20, pady=(0, 18))
        right = ctk.CTkFrame(parent, fg_color='white', corner_radius=20)
        right.grid(row=0, column=1, sticky='nsew')
        self.label(right, '03   Nội dung của bạn', 20, True).pack(anchor='w', padx=24, pady=(24, 4))
        self.label(right, 'Xem trước, chỉnh sửa và sao chép bài viết tại đây.', 13).pack(anchor='w', padx=24, pady=(0, 14))
        self.post = ctk.CTkTextbox(right, corner_radius=14, fg_color='#F7F9F6', font=('Segoe UI', 15), wrap='word', undo=True)
        self.post.pack(fill='both', expand=True, padx=22, pady=(0, 16))
        actions = ctk.CTkFrame(right, fg_color='transparent')
        actions.pack(fill='x', padx=22, pady=(0, 12))
        self.button(actions, 'Sao chép', self.copy_post).pack(side='left', expand=True, fill='x', padx=(0, 8))
        self.button(actions, 'Lưu bài đã sửa', self.save_post, True).pack(side='left', expand=True, fill='x')
        self.button(right, 'Mở thư mục kết quả', self.open_output, True).pack(fill='x', padx=22, pady=(0, 22))

    def build_media(self, parent):
        panel = ctk.CTkScrollableFrame(parent, fg_color='white', corner_radius=20)
        panel.pack(fill='both', expand=True)
        self.label(panel, 'Ảnh & video tùy chọn', 22, True).pack(anchor='w', padx=20, pady=18)
        self.label(panel, 'Dùng thông tin đã nhập ở tab Soạn nội dung.', 14).pack(anchor='w', padx=20)
        for title, key, maximum in [('Số ảnh', 'images', 10), ('Số video', 'videos', 5)]:
            row = ctk.CTkFrame(panel, fg_color='transparent')
            row.pack(fill='x', padx=20, pady=8)
            self.label(row, title).pack(side='left', padx=(0, 16))
            ctk.CTkOptionMenu(row, variable=self.vars[key], values=[str(i) for i in range(maximum+1)]).pack(side='left')
        self.ai_images_switch = ctk.CTkSwitch(panel, text='Dùng AI tạo ảnh minh họa', variable=self.ai_images)
        self.ai_images_switch.pack(anchor='w', padx=20, pady=10)
        self.photo_label = self.label(panel, 'Chưa chọn ảnh gốc')
        self.photo_label.pack(anchor='w', padx=20)
        self.button(panel, 'Chọn ảnh gốc', self.pick_photos, True).pack(anchor='w', padx=20, pady=8)
        self.button(panel, 'Tạo bài + media', self.generate).pack(fill='x', padx=20, pady=8)
        self.label(panel, 'Danh sách đăng bài', 20, True).pack(anchor='w', padx=20, pady=(18, 4))
        self.label(panel, 'Tích mục muốn đăng. Giữ biểu tượng ☰ rồi kéo đến vị trí mới, hoặc bấm ↑ ↓.', 13).pack(anchor='w', padx=20)
        toolbar = ctk.CTkFrame(panel, fg_color='transparent')
        toolbar.pack(fill='x', padx=20, pady=10)
        self.button(toolbar, 'Thêm ảnh / video từ máy', self.import_media, True).pack(side='left', padx=(0, 8))
        self.button(toolbar, 'Chọn tất cả', lambda: self.media_list.choose_all(True), True).pack(side='left', padx=(0, 8))
        self.button(toolbar, 'Bỏ chọn tất cả', lambda: self.media_list.choose_all(False), True).pack(side='left')
        self.media_summary = self.label(panel, '', 13)
        self.media_summary.pack(anchor='w', padx=20)
        self.media_list = MediaList(panel, self.media_selection, self.update_media_summary, self.open_media)
        self.media_list.pack(fill='x', padx=20, pady=10)
        self.label(panel, 'Đăng trực tiếp: nhóm ảnh hoặc một video. Chưa hỗ trợ bài trộn ảnh + video.\n'
                   'Xuất danh sách để giữ thứ tự file khi đăng thủ công. Facebook có thể tự bố trí ảnh khác phần xem trước.',
                   13, justify='left', wraplength=850).pack(anchor='w', padx=20, pady=8)
        self.button(panel, 'Xuất các mục đã chọn theo thứ tự', self.export_selected_media, True).pack(fill='x', padx=20, pady=8)
        self.button(panel, 'Kiểm tra & đăng các mục đã chọn…', self.publish).pack(fill='x', padx=20, pady=(8, 20))

    def build_settings(self, parent):
        panel = ctk.CTkScrollableFrame(parent, fg_color='white', corner_radius=20)
        panel.pack(fill='both', expand=True)
        panel.grid_columnconfigure(1, weight=1)
        self.label(panel, 'Kết nối dịch vụ', 22, True).grid(row=0, column=0, columnspan=2, sticky='w', padx=24, pady=20)
        self.label(panel, 'Dịch vụ AI').grid(row=1, column=0, padx=24, sticky='w')
        ctk.CTkOptionMenu(panel, variable=self.vars['provider'], values=list(AI_MODELS)).grid(row=1, column=1, sticky='ew', padx=24, pady=8)
        fields = [('API key', 'key'), ('Model viết bài', 'text_model'), ('Model tạo ảnh', 'image_model'),
                  ('Fanpage', 'page_choice'), ('Facebook Page ID', 'page'),
                  ('Page Access Token', 'token'), ('Phiên bản Graph API', 'version')]
        self.ai_entries = {}
        for index, (title, key) in enumerate(fields, 2):
            label = self.label(panel, title)
            label.grid(row=index, column=0, sticky='w', padx=24, pady=10)
            if key in ('text_model', 'image_model', 'page_choice', 'version'):
                values = (list(FACEBOOK_PAGES) if key == 'page_choice' else
                          GRAPH_API_VERSIONS if key == 'version' else
                          AI_MODELS[self.vars['provider'].get()][key])
                entry = ctk.CTkOptionMenu(panel, variable=self.vars[key], values=values or [''],
                                          state='normal' if values else 'disabled',
                                          corner_radius=12, height=42, dynamic_resizing=False)
            else:
                entry = ctk.CTkEntry(panel, textvariable=self.vars[key], show='•' if key in ('key', 'token') else '',
                                    state='readonly' if key == 'page' else 'normal', corner_radius=12, height=42)
            entry.grid(row=index, column=1, sticky='ew', padx=24, pady=10)
            if key in ('key', 'text_model', 'image_model'):
                self.ai_entries[key] = (label, entry)
        self.vars['provider'].trace_add('write', self.provider_changed)
        self.provider_changed()
        self.vars['page_choice'].trace_add('write', self.page_changed)
        self.page_changed()
        self.button(panel, 'Kiểm tra fanpage', self.check_page, True).grid(row=9, column=1, sticky='ew', padx=24, pady=10)
        self.label(panel, 'Chỉ tạo văn bản không cần kết nối Facebook.\n'
                   'Danh sách page, model và phiên bản API: sửa connection_options.py rồi mở lại ứng dụng.\n'
                   'API key nhập trực tiếp chỉ giữ trong phiên chạy. GPT qua API cần số dư riêng với ChatGPT Plus.\n'
                   'Kết quả lưu trong Documents/KhanhToanStudio. Ảnh AI cần kiểm tra trước khi sử dụng.',
                   14, justify='left', wraplength=800).grid(row=10, column=0, columnspan=2, sticky='w', padx=24, pady=20)

    def copy_post(self):
        content = self.post.get('1.0', 'end').strip()
        if content:
            self.clipboard_clear()
            self.clipboard_append(content)
            self.vars['status'].set('Đã sao chép bài viết.')
