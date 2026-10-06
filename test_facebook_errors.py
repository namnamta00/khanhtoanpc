import unittest
from unittest.mock import Mock, patch
from services import Facebook


class FacebookErrorTests(unittest.TestCase):
    def test_400_reports_stage_code_and_redacts_token(self):
        response = Mock(ok=False, status_code=400)
        response.json.return_value = {'error': {'code': 190, 'error_subcode': 463,
            'message': 'Expired token private-secret access_token=another-secret', 'fbtrace_id': 'trace123'}}
        with patch('services.requests.request', return_value=response) as request:
            with self.assertRaises(RuntimeError) as caught:
                Facebook('123', 'private-secret', 'v24.0').verify()
            text = str(caught.exception)
            self.assertIn('190', text)
            self.assertIn('463', text)
            self.assertIn('Kiểm tra token', text)
            self.assertIn('trace123', text)
            self.assertNotIn('private-secret', text)
            self.assertNotIn('another-secret', text)
            request.assert_called_once()

    def test_permission_error_even_with_http_200(self):
        response = Mock(ok=True, status_code=200)
        response.json.return_value = {'error': {'code': 200, 'message': 'Permissions error'}}
        with patch('services.requests.request', return_value=response):
            with self.assertRaises(RuntimeError) as caught:
                Facebook('123', 'test', 'v24.0').request('POST', '123/feed', data={'message': 'x'})
            self.assertIn('Xuất bản bài viết', str(caught.exception))
            self.assertIn('pages_manage_posts', str(caught.exception))

    def test_non_json_400_is_reported_without_body(self):
        response = Mock(ok=False, status_code=400)
        response.json.side_effect = ValueError()
        with patch('services.requests.request', return_value=response):
            with self.assertRaises(RuntimeError) as caught:
                Facebook('123', 'test', 'v24.0').request('POST', '123/videos')
            self.assertIn('Đăng video', str(caught.exception))
            self.assertIn('Mã lỗi: ?', str(caught.exception))

    def test_success_unchanged(self):
        response = Mock(ok=True, status_code=200)
        response.json.return_value = {'id': '123', 'name': 'Trang thử'}
        with patch('services.requests.request', return_value=response):
            self.assertEqual(Facebook('123', 'test', 'v24.0').verify()['id'], '123')


if __name__ == '__main__':
    unittest.main()
