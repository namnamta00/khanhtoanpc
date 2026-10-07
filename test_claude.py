import unittest
from unittest.mock import Mock, patch

import requests

from connection_options import AI_MODELS
from services import generate_ai


class ClaudeTests(unittest.TestCase):
    def test_messages_request_and_text_blocks(self):
        response = Mock(ok=True)
        response.json.return_value = {'stop_reason': 'end_turn', 'content': [
            {'type': 'thinking', 'thinking': 'internal'},
            {'type': 'text', 'text': 'Bài viết'}, {'type': 'text', 'text': 'Tiếng Việt'}]}
        model = AI_MODELS['Claude']['text_model'][0]
        with patch('services.requests.post', return_value=response) as post:
            self.assertEqual(generate_ai('Claude', ' test-key ', model, 'Viết bài'), 'Bài viết\nTiếng Việt')
        self.assertEqual(post.call_args.args, ('https://api.anthropic.com/v1/messages',))
        self.assertEqual(post.call_args.kwargs['headers'],
                         {'x-api-key': 'test-key', 'anthropic-version': '2023-06-01'})
        self.assertEqual(post.call_args.kwargs['json'], {
            'model': model, 'max_tokens': 8192,
            'messages': [{'role': 'user', 'content': 'Viết bài'}]})

    def test_images_and_missing_credentials_do_not_send_requests(self):
        with patch('services.requests.post') as post:
            for key, images in [('test-key', True), ('', False)]:
                with self.subTest(images=images), self.assertRaises(ValueError):
                    generate_ai('Claude', key, 'claude-sonnet-5-5', 'Bài', images)
            post.assert_not_called()

    def test_incomplete_and_empty_responses(self):
        for reason, content in [('max_tokens', [{'type': 'text', 'text': 'Bài bị cắt'}]),
                                ('refusal', []), ('end_turn', [])]:
            response = Mock(ok=True)
            response.json.return_value = {'stop_reason': reason, 'content': content}
            with self.subTest(reason=reason), patch('services.requests.post', return_value=response):
                with self.assertRaises(RuntimeError):
                    generate_ai('Claude', 'test-key', 'claude-sonnet-5-5', 'Bài')

    def test_errors_do_not_expose_key(self):
        response = Mock(ok=False, status_code=401)
        response.json.return_value = {'error': {'message': 'secret-key'}}
        for kwargs in [{'return_value': response}, {'side_effect': requests.RequestException('secret-key')}]:
            with self.subTest(kwargs=kwargs), patch('services.requests.post', **kwargs):
                with self.assertRaises(RuntimeError) as error:
                    generate_ai('Claude', 'secret-key', 'claude-sonnet-5-5', 'Bài')
                self.assertNotIn('secret-key', str(error.exception))

    def test_provider_switch_preserves_credentials_and_disables_images(self):
        from main import App
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'claude-test'}):
            app = App()
        app.withdraw()
        try:
            app.vars['openai_key'].set('openai-test')
            app.vars['key'].set('gemini-test')
            app.ai_images.set(True)
            app.vars['provider'].set('Claude')
            self.assertEqual(app.ai_entries['key'][1].get(), 'claude-test')
            self.assertEqual(app.ai_entries['text_model'][1].cget('values'), AI_MODELS['Claude']['text_model'])
            self.assertEqual(app.ai_entries['image_model'][1].cget('state'), 'disabled')
            self.assertFalse(app.ai_images.get())
            self.assertEqual(app.ai_images_switch.cget('state'), 'disabled')
            app.vars['claude_text_model'].set(AI_MODELS['Claude']['text_model'][1])
            for provider, key in [('Gemini', 'gemini-test'), ('GPT / OpenAI', 'openai-test')]:
                app.vars['provider'].set(provider)
                self.assertEqual(app.ai_entries['key'][1].get(), key)
                self.assertEqual(app.ai_images_switch.cget('state'), 'normal')
            app.vars['provider'].set('Claude')
            self.assertEqual(app.ai_entries['text_model'][1].get(), AI_MODELS['Claude']['text_model'][1])
        finally:
            app.destroy()


if __name__ == '__main__':
    unittest.main()
