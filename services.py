"""API có timeout; không ghi khóa API/token vào đĩa hoặc thông báo lỗi."""
import base64
import json
import re
import mimetypes
from urllib.parse import quote
from pathlib import Path
import requests


def checked(response, label):
    if not response.ok:
        if label == 'OpenAI':
            try:
                payload = response.json()
            except ValueError:
                payload = {}
            error = payload.get('error', {}) if isinstance(payload, dict) else {}
            error = error if isinstance(error, dict) else {}
            # Only expose recognized codes; server messages can contain request data.
            codes = {str(error.get('code', '')), str(error.get('type', ''))}
            quota_codes = {'insufficient_quota', 'billing_hard_limit_reached',
                           'billing_not_active', 'usage_limit_reached',
                           'organization_usage_limit_exceeded', 'billing_limit_user_error',
                           'credit_balance_exhausted', 'organization_spend_limit_exceeded',
                           'project_spend_limit_exceeded', 'credits_exhausted', 'spend_limit_exceeded'}
            if codes & quota_codes:
                code = sorted(codes & quota_codes)[0]
                raise RuntimeError(f'OpenAI: HTTP {response.status_code} ({code}).\n'
                                   'Hạn mức/số dư API không đủ hoặc thanh toán chưa hoạt động. '
                                   'Kiểm tra Billing và Limits của đúng project/organization tại platform.openai.com. '
                                   'Đổi quyền API key hoặc bấm tạo lại không khắc phục được lỗi hạn mức.')
            if response.status_code == 429:
                if codes & {'rate_limit_exceeded', 'rate_limit_error', 'slow_down'}:
                    raise RuntimeError('OpenAI: HTTP 429 (rate_limit_exceeded).\n'
                                       'Đã vượt tốc độ yêu cầu/token cho phép. Đợi một lúc rồi thử lại với 1 ảnh; '
                                       'kiểm tra Limits của model. Ứng dụng không tự gửi lại yêu cầu tính phí.')
                raise RuntimeError('OpenAI: HTTP 429, chưa xác định được loại giới hạn.\n'
                                   'Kiểm tra Billing, số dư và Limits của project. Có thể hết hạn mức hoặc gửi quá nhanh. '
                                   'Chưa có bằng chứng đây là lỗi quyền API key.')
            if response.status_code in (401, 403):
                raise RuntimeError(f'OpenAI: HTTP {response.status_code}.\n'
                                   'Kiểm tra API key còn hiệu lực, quyền gọi Responses/tạo ảnh và quyền truy cập model của project.')
        raise RuntimeError(f'{label}: HTTP {response.status_code}. Kiểm tra khóa/token, quyền truy cập, model và hạn mức dịch vụ.')
    try:
        return response.json()
    except ValueError:
        raise RuntimeError(f'{label}: phản hồi không phải JSON.') from None


def gemini(key, model, prompt, images=False):
    if not key.strip() or not re.fullmatch(r'[A-Za-z0-9._-]+', model):
        raise ValueError('Nhập API key Gemini và tên model hợp lệ trong Cài đặt.')
    body = {'contents': [{'parts': [{'text': prompt}]}]}
    if images:
        body['generationConfig'] = {'responseModalities': ['TEXT', 'IMAGE']}
    try:
        response = requests.post(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent',
                                 headers={'x-goog-api-key': key}, json=body, timeout=(15, 180))
    except requests.RequestException:
        raise RuntimeError('Không kết nối được Gemini. Kiểm tra Internet và thử lại.') from None
    data = checked(response, 'Gemini')
    parts = data.get('candidates', [{}])[0].get('content', {}).get('parts', [])
    if images:
        for part in parts:
            inline = part.get('inlineData', {})
            if inline.get('mimeType', '').startswith('image/'):
                return base64.b64decode(inline['data'])
        raise RuntimeError('Model chưa trả về ảnh. Kiểm tra model có hỗ trợ tạo ảnh hoặc đổi mô tả.')
    result = '\n'.join(part.get('text', '') for part in parts).strip()
    if not result:
        raise RuntimeError('AI chưa trả về nội dung. Hãy đổi mô tả hoặc model.')
    return result


def openai_generate(key, model, prompt, images=False):
    if not key.strip() or not re.fullmatch(r'[A-Za-z0-9._:-]+', model):
        raise ValueError('Nhập OpenAI API key và tên model hợp lệ trong tab Kết nối.')
    endpoint = 'images/generations' if images else 'responses'
    body = ({'model': model, 'prompt': prompt, 'n': 1, 'size': '1024x1024'} if images
            else {'model': model, 'input': prompt, 'store': False})
    try:
        response = requests.post(f'https://api.openai.com/v1/{endpoint}',
                                 headers={'Authorization': 'Bearer ' + key.strip()},
                                 json=body, timeout=(15, 300))
    except requests.RequestException:
        raise RuntimeError('Không kết nối được OpenAI. Kiểm tra Internet; yêu cầu có thể đã được tính phí, hãy kiểm tra trước khi thử lại.') from None
    data = checked(response, 'OpenAI')
    if images:
        items = data.get('data') or []
        encoded = items[0].get('b64_json') if items else None
        if not encoded:
            raise RuntimeError('OpenAI chưa trả về ảnh. Hãy chọn model GPT Image được tài khoản cấp quyền.')
        try:
            return base64.b64decode(encoded, validate=True)
        except (ValueError, TypeError):
            raise RuntimeError('OpenAI trả về dữ liệu ảnh không hợp lệ.') from None
    if data.get('status') != 'completed':
        raise RuntimeError('OpenAI chưa hoàn thành nội dung. Hãy kiểm tra model hoặc đổi yêu cầu.')
    result = '\n'.join(part.get('text', '')
                       for item in data.get('output', []) if item.get('type') == 'message'
                       for part in item.get('content', []) if part.get('type') == 'output_text').strip()
    if not result:
        raise RuntimeError('OpenAI chưa trả về nội dung hoặc đã từ chối yêu cầu. Hãy đổi mô tả.')
    return result


def generate_ai(provider, key, model, prompt, images=False):
    if provider == 'GPT / OpenAI':
        return openai_generate(key, model, prompt, images)
    if provider == 'Gemini':
        return gemini(key, model, prompt, images)
    raise ValueError('Hãy chọn GPT / OpenAI hoặc Gemini.')


def facebook_error(response, data, stage, token):
    """Preserve diagnostic fields, never include the request token or headers."""
    error = data.get('error', {}) if isinstance(data, dict) else {}
    error = error if isinstance(error, dict) else {}
    code = str(error.get('code', ''))
    subcode = str(error.get('error_subcode', ''))
    code = code if code.isdigit() else '?'
    subcode = subcode if subcode.isdigit() else '?'
    def clean(value):
        text = str(value or '')
        for secret in (token, quote(token, safe='')):
            if secret:
                text = text.replace(secret, '[đã ẩn token]')
        text = re.sub(r'(?i)(access_token[\s\"\x27:=]+)[^\s&\"\x27,}]+', r'\1[đã ẩn]', text)
        text = re.sub(r'(?i)Bearer\s+[^\s\"\x27,}]+', 'Bearer [đã ẩn]', text)
        return text[:800]
    if code == '190':
        advice = 'Kiểm tra token còn hiệu lực; nếu hết hạn hoặc bị thu hồi, lấy lại Page Access Token của đúng trang.'
    elif code == '10' or (code.isdigit() and 200 <= int(code) <= 299):
        advice = 'Kiểm tra quyền pages_manage_posts/pages_read_engagement, quyền tạo nội dung trên trang và vai trò trong ứng dụng Meta.'
    elif code in ('100', '803'):
        advice = 'Kiểm tra chi tiết Meta bên dưới: có thể là tham số/file không hợp lệ, ID không đúng hoặc tài khoản không được truy cập đối tượng.'
    else:
        advice = 'Đối chiếu chi tiết Meta bên dưới để xác định nguyên nhân; chỉ mã HTTP chưa đủ kết luận.'
    details = clean(error.get('message')) or 'Meta không trả thông báo lỗi có thể đọc được.'
    trace = clean(error.get('fbtrace_id'))
    return RuntimeError(f'Facebook: HTTP {response.status_code}\nBước: {stage}\n'
                        f'Mã lỗi: {code} • Mã phụ: {subcode}\n\n{details}\n\n{advice}'
                        + (f'\nMã tra cứu Meta: {trace}' if trace else '')
                        + ('\nKiểm tra fanpage trước khi thử đăng lại để tránh trùng bài.' if stage != 'Kiểm tra token và fanpage' else ''))


class Facebook:
    def __init__(self, page_id, token, version):
        if not page_id.isdigit() or not token.strip() or not re.fullmatch(r'v\d+\.\d+', version):
            raise ValueError('Cần Page ID dạng số, Page Access Token và phiên bản Graph API (ví dụ v24.0).')
        self.page_id = page_id
        self.base = f'https://graph.facebook.com/{version}'
        self.headers = {'Authorization': 'Bearer ' + token.strip()}

    def request(self, method, path, **kwargs):
        stage = {'me': 'Kiểm tra token và fanpage', 'photos': 'Tải ảnh chưa xuất bản',
                 'videos': 'Đăng video', 'feed': 'Xuất bản bài viết'}.get(path.split('/')[-1], 'Gọi Facebook API')
        try:
            response = requests.request(method, f'{self.base}/{path}', headers=self.headers,
                                        timeout=(15, 240), **kwargs)
        except requests.RequestException:
            raise RuntimeError('Mất kết nối Facebook. Kiểm tra fanpage trước khi thử lại để tránh đăng trùng.') from None
        try:
            data = response.json()
        except ValueError:
            data = {}
            if response.ok:
                raise RuntimeError(f'Facebook: HTTP {response.status_code}. Bước: {stage}. Phản hồi không phải JSON.') from None
        if not response.ok or (isinstance(data, dict) and 'error' in data):
            token = self.headers['Authorization'].removeprefix('Bearer ')
            raise facebook_error(response, data, stage, token)
        if not isinstance(data, dict):
            raise RuntimeError(f'Facebook: phản hồi không hợp lệ. Bước: {stage}.')
        return data

    def verify(self):
        data = self.request('GET', 'me', params={'fields': 'id,name,link'})
        if str(data.get('id')) != self.page_id:
            raise ValueError('Token không thuộc Page ID đã nhập. Hãy dùng Page Access Token đúng fanpage.')
        return data

    def publish(self, text, photos=(), video=None):
        if video and photos:
            raise ValueError('Chưa hỗ trợ trộn ảnh và video trong cùng một bài qua API của ứng dụng.')
        for path in list(photos) + ([video] if video else []):
            if not Path(path).is_file():
                raise ValueError(f'Không tìm thấy file: {Path(path).name}')
        self.verify()
        if video:
            with open(video, 'rb') as handle:
                result = self.request('POST', f'{self.page_id}/videos', data={'description': text},
                                      files={'source': (Path(video).name, handle, 'video/mp4')})
        else:
            attached = []
            for photo in photos:
                with open(photo, 'rb') as handle:
                    uploaded = self.request('POST', f'{self.page_id}/photos', data={'published': 'false'},
                                            files={'source': (Path(photo).name, handle, mimetypes.guess_type(photo)[0] or 'image/png')})
                attached.append({'media_fbid': uploaded['id']})
            body = {'message': text}
            if attached:
                body['attached_media'] = json.dumps(attached)
            result = self.request('POST', f'{self.page_id}/feed', data=body)
        if not result.get('id'):
            raise RuntimeError('Facebook chưa trả về mã bài đăng. Kiểm tra fanpage trước khi thử lại.')
        return str(result['id'])
