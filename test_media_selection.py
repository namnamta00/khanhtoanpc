import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from PIL import Image

from media_selection import MediaSelection, facebook_media_plan
from services import Facebook


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        self.paths = []
        for name in ('a.png', 'b.png', 'c.png'):
            path = self.directory / name
            Image.new('RGB', (24, 24), 'green').save(path)
            self.paths.append(str(path))
        self.video = self.directory / 'clip.mp4'
        self.video.write_bytes(b'test-placeholder')

    def tearDown(self):
        self.temp.cleanup()

    def test_checked_order_and_snapshot(self):
        selection = MediaSelection()
        selection.add(self.paths)
        selection.items[1].selected = False
        selection.move(2, 0)
        chosen = selection.chosen()
        self.assertEqual([Path(item.path).name for item in chosen], ['c.png', 'a.png'])
        selection.items[0].selected = False
        self.assertTrue(chosen[0].selected)
        self.assertEqual(facebook_media_plan(chosen), ([self.paths[2], self.paths[0]], None))

    def test_mixed_and_multiple_video_rejected(self):
        selection = MediaSelection()
        selection.add([self.paths[0], self.video])
        with self.assertRaises(ValueError):
            facebook_media_plan(selection.chosen())
        selection.items[0].selected = False
        self.assertEqual(facebook_media_plan(selection.chosen()), ([], str(self.video)))
        other_video = self.directory / 'second.mp4'
        other_video.write_bytes(b'test-placeholder')
        selection.add([other_video])
        with self.assertRaises(ValueError):
            facebook_media_plan(selection.chosen())

    def test_missing_file_and_deduplication(self):
        selection = MediaSelection()
        selection.add(self.paths + [self.paths[0]])
        self.assertEqual(len(selection.items), 3)
        Path(self.paths[1]).unlink()
        with self.assertRaises(ValueError):
            facebook_media_plan(selection.chosen())

    def test_photo_api_payload_preserves_order(self):
        client = Facebook('123', 'test-token', 'v24.0')
        with patch.object(client, 'request', side_effect=[{'id': '123'}, {'id': 'photoC'}, {'id': 'photoA'}, {'id': 'post'}]) as request:
            client.publish('Bài thử', [self.paths[2], self.paths[0]])
            attached = json.loads(request.call_args.kwargs['data']['attached_media'])
            self.assertEqual(attached, [{'media_fbid': 'photoC'}, {'media_fbid': 'photoA'}])
        with patch.object(client, 'request') as request:
            with self.assertRaises(ValueError):
                client.publish('Bài thử', self.paths, str(self.video))
            request.assert_not_called()

    def test_drag_checkbox_publish_and_export(self):
        from main import App
        app = App()
        try:
            app.media_selection.add(self.paths)
            app.media_list.refresh()
            app.tabs.set('Ảnh & video')
            app.update()
            widget = app.media_list
            widget.toggle(app.media_selection.items[1], False)
            widget.start_drag(self.paths[2])
            row = widget.rows[0]
            event = SimpleNamespace(y_root=row.winfo_rooty()+row.winfo_height()/2)
            widget.drag(event)
            widget.drop(event)
            self.assertEqual([Path(item.path).name for item in app.media_selection.chosen()], ['c.png', 'a.png'])
            app.post.insert('1.0', 'Bài thử')
            app.run_job = lambda label, work, done: done(work())
            with patch.object(app, 'facebook') as facebook, patch('main.messagebox.askyesno', return_value=True), patch.object(app, 'published'):
                facebook.return_value.verify.return_value = {'id': '123', 'name': 'Trang thử'}
                facebook.return_value.publish.return_value = 'post'
                app.publish()
                facebook.return_value.publish.assert_called_once_with('Bài thử', [self.paths[2], self.paths[0]], None)
            app.media_selection.add([self.video])
            with patch.object(app, 'facebook') as facebook, patch('main.messagebox.showerror') as error:
                app.publish()
                facebook.assert_not_called()
                error.assert_called_once()
            with patch('main.filedialog.askdirectory', return_value=str(self.directory)), patch('main.os.startfile'):
                app.export_selected_media()
            exported = next(self.directory.glob('BaiDang_*'))
            entries = json.loads((exported / 'thu_tu_media.json').read_text(encoding='utf-8'))
            self.assertEqual([item['file'] for item in entries], ['001_c.png', '002_a.png', '003_clip.mp4'])
            self.assertTrue((exported / '003_clip.mp4').is_file())
        finally:
            # Cancel Tcl timers without deleting commands still owned by widgets.
            for timer in app.tk.call('after', 'info'):
                app.tk.call('after', 'cancel', timer)
            app.destroy()


if __name__ == '__main__':
    unittest.main()
