import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, Mock
from catalog import Product, read_catalog, draft, clean_post, finish_post, STORE_FOOTER
from services import Facebook, generate_ai, checked
from media import card, slideshow


class Tests(unittest.TestCase):
    def test_store_template(self):
        product = Product('Camera IMOU S7XEP', '', '2 mắt camera\nĐàm thoại 2 chiều')
        text = draft(product, '')
        self.assertTrue(text.startswith('✨ CAMERA IMOU S7XEP\n✅ 2 mắt camera\n✅ Đàm thoại 2 chiều'))
        self.assertEqual(text.count(STORE_FOOTER), 1)
        self.assertIn('#camera', text.splitlines()[-1])
        self.assertNotIn('#MayTinh', text)
        self.assertNotIn('💰', text)
        ai = finish_post('🏡 CAMERA\n✅ 2 mắt\n#camera #imou', product)
        self.assertEqual(ai.count('#camera'), 1)
        self.assertEqual(ai.count(STORE_FOOTER), 1)
        self.assertEqual(finish_post(ai, product), ai)

    def test_remove_assistant_preamble_preserves_sales_copy(self):
        body = '✨ Laptop RAM 16GB\n\nNhắn tin Khánh Toàn Computer.\n#Laptop'
        intro = 'Tuyệt vời! Dưới đây là bài viết bán hàng Facebook cho Khánh Toàn Computer, tuân thủ chặt chẽ các yêu cầu bạn đưa ra:'
        self.assertEqual(clean_post(intro + '\n\n' + body), body)
        self.assertEqual(clean_post('Tuyệt vời!\n\nDưới đây là bài đăng:\n---\n' + body), body)
        self.assertEqual(clean_post('```text\n' + body + '\n```'), body)
        self.assertEqual(clean_post('Tuyệt vời cho công việc!\n' + body), 'Tuyệt vời cho công việc!\n' + body)
        self.assertEqual(clean_post(body), body)

    def test_optional_price(self):
        self.assertNotIn('giá', draft(Product('Laptop', '', 'RAM 16GB'), '').lower())
        self.assertIn('8.500.000 đ', draft(Product('Laptop', '8.500.000 đ'), ''))

    def test_text_only_has_no_media_or_facebook_calls(self):
        from main import App
        app = App()
        app.withdraw()
        try:
            app.vars['product_name'].set('Laptop thử nghiệm')
            app.description.insert('1.0', 'RAM 16GB')
            app.vars['images'].set('3')
            app.vars['videos'].set('1')
            app.ai_images.set(True)
            with tempfile.TemporaryDirectory() as folder, patch('main.Path.home', return_value=Path(folder)), \
                 patch('main.generate_ai') as ai, patch('main.card') as image, \
                 patch('main.slideshow') as video, patch('main.Facebook') as facebook:
                app.run_job = lambda label, work, done: done(work())
                app.generate_text_only()
                self.assertIn('LAPTOP THỬ NGHIỆM', app.post.get('1.0', 'end'))
                self.assertNotIn('giá', app.post.get('1.0', 'end').lower())
                self.assertTrue((app.output / 'bai_dang.txt').is_file())
                self.assertEqual(app.photos + app.videos, [])
                for service in (ai, image, video, facebook):
                    service.assert_not_called()
                app.post.delete('1.0', 'end')
                app.ai_text.set(True)
                app.vars['openai_key'].set('test-key')
                ai.return_value = 'Tuyệt vời! Dưới đây là bài viết bán hàng Facebook:\n\nBài viết thử bằng AI'
                app.generate_text_only()
                ai.assert_called_once()
                self.assertIn('Nếu giá trống', ai.call_args.args[3])
                self.assertEqual(ai.call_args.args[0], 'GPT / OpenAI')
                self.assertIn('Bài viết thử bằng AI', app.post.get('1.0', 'end'))
                self.assertNotIn('Dưới đây', app.post.get('1.0', 'end'))
                self.assertNotIn('Tuyệt vời', (app.output / 'bai_dang.txt').read_text(encoding='utf-8'))
                for service in (image, video, facebook):
                    service.assert_not_called()
        finally:
            app.destroy()

    def test_429_quota_rate_and_unknown_are_distinct(self):
        for code, expected in [('insufficient_quota', 'Billing'),
                               ('credit_balance_exhausted', 'Billing'),
                               ('project_spend_limit_exceeded', 'Billing'),
                               ('rate_limit_exceeded', 'tốc độ'),
                               ('unknown', 'chưa xác định')]:
            with self.subTest(code=code):
                response = Mock(ok=False, status_code=429)
                response.json.return_value = {'error': {'code': code, 'message': 'secret-key'}}
                with self.assertRaises(RuntimeError) as error:
                    checked(response, 'OpenAI')
                self.assertIn(expected, str(error.exception))
                self.assertNotIn('secret-key', str(error.exception))

    def test_image_failure_keeps_generated_text(self):
        from main import App
        app = App()
        app.withdraw()
        try:
            app.vars['product_name'].set('Laptop')
            app.vars['images'].set('1')
            app.ai_text.set(True)
            app.ai_images.set(True)
            app.vars['openai_key'].set('test-key')
            with tempfile.TemporaryDirectory() as folder, patch('main.Path.home', return_value=Path(folder)), \
                 patch('main.generate_ai', side_effect=['Bài đã tạo', RuntimeError('HTTP 429')]), \
                 patch('main.messagebox.showwarning') as warning:
                app.run_job = lambda label, work, done: done(work())
                app.generate()
                self.assertIn('Bài đã tạo', app.post.get('1.0', 'end'))
                self.assertIn('Bài đã tạo', (app.output / 'bai_dang.txt').read_text(encoding='utf-8'))
                self.assertEqual(app.photos, [])
                warning.assert_called_once()
        finally:
            app.destroy()

    def test_openai_text_ignores_reasoning_and_reads_message(self):
        response = Mock(ok=True)
        response.json.return_value = {'status': 'completed', 'output': [
            {'type': 'reasoning'}, {'type': 'message', 'content': [{'type': 'output_text', 'text': 'Bài tiếng Việt'}]}]}
        with patch('services.requests.post', return_value=response) as post:
            self.assertEqual(generate_ai('GPT / OpenAI', 'test-key', 'gpt-4.1-mini', 'Viết bài'), 'Bài tiếng Việt')
            self.assertEqual(post.call_args.args[0], 'https://api.openai.com/v1/responses')
            self.assertFalse(post.call_args.kwargs['json']['store'])

    def test_openai_image_and_gemini_routing(self):
        response = Mock(ok=True)
        response.json.return_value = {'data': [{'b64_json': 'aW1hZ2U='}]}
        with patch('services.requests.post', return_value=response) as post:
            self.assertEqual(generate_ai('GPT / OpenAI', 'test-key', 'gpt-image-1', 'Ảnh', True), b'image')
            self.assertTrue(post.call_args.args[0].endswith('/images/generations'))
            self.assertNotIn('response_format', post.call_args.kwargs['json'])
        with patch('services.gemini', return_value='Gemini') as gemini:
            self.assertEqual(generate_ai('Gemini', 'gem-key', 'gem-model', 'Bài'), 'Gemini')
            gemini.assert_called_once_with('gem-key', 'gem-model', 'Bài', False)

    def test_openai_incomplete_and_http_errors(self):
        response = Mock(ok=True)
        response.json.return_value = {'status': 'incomplete', 'output': []}
        with patch('services.requests.post', return_value=response):
            with self.assertRaises(RuntimeError):
                generate_ai('GPT / OpenAI', 'private-key', 'gpt-4.1-mini', 'Bài')
        response.ok = False
        response.status_code = 401
        with patch('services.requests.post', return_value=response):
            with self.assertRaises(RuntimeError) as error:
                generate_ai('GPT / OpenAI', 'private-key', 'gpt-4.1-mini', 'Bài')
            self.assertNotIn('private-key', str(error.exception))

    def test_provider_switch_preserves_separate_keys(self):
        from main import App
        app = App()
        app.withdraw()
        try:
            app.vars['openai_key'].set('openai-test')
            app.vars['key'].set('gemini-test')
            self.assertEqual(app.ai_entries['key'][1].get(), 'openai-test')
            app.vars['provider'].set('Gemini')
            self.assertEqual(app.ai_entries['key'][1].get(), 'gemini-test')
            app.vars['provider'].set('GPT / OpenAI')
            self.assertEqual(app.ai_entries['key'][1].get(), 'openai-test')
            self.assertEqual(app.ai_entries['text_model'][1].get(), 'gpt-5.6-terra')
            self.assertEqual(app.ai_entries['image_model'][1].get(), 'gpt-image-2.5-flare')
        finally:
            app.destroy()

    def test_csv_vietnamese_and_missing_price(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'gia.csv'
            path.write_text('Tên sản phẩm;Giá;Mô tả\nMáy tính;;RAM 16GB\n', encoding='utf-8-sig')
            product = read_catalog(path)[0]
            self.assertEqual(product.name, 'Máy tính')
            self.assertNotIn('báo giá', draft(product, ''))
            self.assertNotIn('bảo hành', draft(product, ''))

    def test_xlsx_title_row_and_numeric_price(self):
        from openpyxl import Workbook
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'gia.xlsx'
            book = Workbook()
            book.active.append(['BÁO GIÁ'])
            book.active.append(['Tên hàng', 'Đơn giá', 'Cấu hình'])
            book.active.append(['Laptop', 15000000, 'RAM 16GB'])
            book.save(path)
            self.assertEqual(read_catalog(path)[0].price, '15.000.000 đ')

    def test_wrong_page_never_publishes(self):
        client = Facebook('123', 'secret', 'v24.0')
        with patch.object(client, 'request', return_value={'id': '456'}) as request:
            with self.assertRaises(ValueError):
                client.publish('Nội dung')
            self.assertEqual(request.call_count, 1)
            self.assertEqual(request.call_args.args[0], 'GET')

    def test_photo_is_unpublished_before_feed(self):
        client = Facebook('123', 'secret', 'v24.0')
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'photo.png'
            path.write_bytes(b'image')
            with patch.object(client, 'request', side_effect=[{'id': '123'}, {'id': 'pic'}, {'id': 'post'}]) as request:
                self.assertEqual(client.publish('Bài', [str(path)]), 'post')
                self.assertEqual(request.call_args_list[1].kwargs['data']['published'], 'false')
                self.assertEqual(request.call_args_list[2].args[1], '123/feed')

    def test_media_real_encode(self):
        from PIL import Image
        import imageio.v2 as imageio
        with tempfile.TemporaryDirectory() as folder:
            photo = card(Product('Máy tính tiếng Việt', '12.000.000 đ', 'RAM 16GB'), '', Path(folder) / 'a.png')
            with Image.open(photo) as image:
                self.assertEqual(image.size, (1080, 1080))
            video = slideshow([photo], Path(folder) / 'v.mp4')
            reader = imageio.get_reader(video)
            try:
                self.assertEqual(reader.get_data(0).shape[:2], (720, 720))
                self.assertAlmostEqual(reader.get_meta_data()['duration'], 3, delta=0.1)
            finally:
                reader.close()


if __name__ == '__main__':
    unittest.main()
