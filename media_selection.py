"""Thứ tự media và lựa chọn đăng, độc lập với giao diện/API."""
from dataclasses import dataclass
from pathlib import Path

PHOTO_TYPES = {'.png', '.jpg', '.jpeg', '.webp'}


@dataclass
class MediaItem:
    path: str
    kind: str
    selected: bool = True


class MediaSelection:
    def __init__(self):
        self.items = []

    def add(self, paths):
        additions = []
        known = {str(Path(item.path).resolve()).casefold() for item in self.items}
        for raw in paths:
            path = Path(raw).resolve()
            if path.suffix.lower() not in PHOTO_TYPES | {'.mp4'}:
                raise ValueError(f'Chỉ hỗ trợ ảnh PNG/JPG/WEBP và video MP4: {path.name}')
            if not path.is_file():
                raise ValueError(f'Không tìm thấy file: {path.name}')
            if str(path).casefold() not in known:
                additions.append(MediaItem(str(path), 'video' if path.suffix.lower() == '.mp4' else 'photo'))
                known.add(str(path).casefold())
        self.items.extend(additions)

    def move(self, source, target):
        if 0 <= source < len(self.items) and 0 <= target < len(self.items):
            self.items.insert(target, self.items.pop(source))

    def chosen(self):
        return [MediaItem(item.path, item.kind, True) for item in self.items if item.selected]


def facebook_media_plan(items):
    """Fail before any upload; never silently discard mixed media."""
    for item in items:
        if not Path(item.path).is_file():
            raise ValueError(f'File đã bị xóa hoặc di chuyển: {Path(item.path).name}')
        if item.kind not in ('photo', 'video'):
            raise ValueError('Loại media chưa được hỗ trợ.')
    photos = [item.path for item in items if item.kind == 'photo']
    videos = [item.path for item in items if item.kind == 'video']
    if videos and (photos or len(videos) > 1):
        raise ValueError('Bản tích hợp API hiện tại hỗ trợ một nhóm ảnh hoặc một video cho mỗi bài. '
                         'Danh sách đang chọn có nhiều video hoặc trộn ảnh và video. '
                         'Hãy bỏ tích các mục không dùng, hoặc xuất danh sách theo thứ tự để đăng thủ công. '
                         'Chưa có file nào được tải lên; ứng dụng không tự tách thành nhiều bài.')
    return photos, videos[0] if videos else None
