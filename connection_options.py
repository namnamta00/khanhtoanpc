"""Các lựa chọn trong tab Kết nối. Sửa file này rồi mở lại ứng dụng.

FACEBOOK_PAGES: mỗi tên page là duy nhất, gồm page_id và token tương ứng.
Có thể điền Page ID trực tiếp; token có thể lấy từ biến môi trường riêng.
AI_MODELS: thêm/bớt tên model trong từng danh sách; mục đầu là mặc định.
Chỉ thêm model mà tài khoản API của bạn có quyền sử dụng.
"""
import os


FACEBOOK_PAGES = {
    'Khánh Toàn Computer': {
        'page_id': os.getenv('FACEBOOK_PAGE_ID', ''),
        'token': os.getenv('FACEBOOK_PAGE_TOKEN', ''),
    },
    # 'Fanpage thứ hai': {
    #     'page_id': 'DIEN_PAGE_ID_TAI_DAY',
    #     'token': os.getenv('FACEBOOK_PAGE_TOKEN_2', ''),
    # },
}

AI_MODELS = {
    'GPT / OpenAI': {
        # Điền API key giữa hai dấu nháy rỗng bên dưới để tự điền khi chọn GPT.
        # Nếu có biến môi trường OPENAI_API_KEY thì ưu tiên dùng giá trị đó.
        'api_key': os.getenv('OPENAI_API_KEY', ''),
        'text_model': ['gpt-5.6-terra', 'gpt-4.1-mini'],
        'image_model': ['gpt-image-2.5-flare', 'gpt-image-1']
    },
    'Gemini': {
        'text_model': ['gemini-2.5-flash'],
        'image_model': ['gemini-2.5-flash-image']
    }
}

PROVIDER_PREFIXES = {'GPT / OpenAI': 'openai_', 'Gemini': ''}

GRAPH_API_VERSIONS = ['v26.0']
