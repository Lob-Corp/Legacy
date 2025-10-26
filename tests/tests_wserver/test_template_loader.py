import unittest
from pathlib import Path
from wserver.services.template_loader import TemplateService


class TestTemplateService(unittest.TestCase):
    def setUp(self):
        self.service = TemplateService(
            repo_root=Path(__file__).resolve().parents[4])

    def test_resolve_template_file_not_found(self):
        file_path, base_dir = self.service._resolve_template_file(
            'notfound.htm')
        self.assertIsNone(file_path)
        self.assertIsNone(base_dir)

    def test_load_css_text_returns_str(self):
        css = self.service._load_css_text()
        self.assertIsInstance(css, str)

    def test_render_gwsetup_template_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.service.render_gwsetup_template('notfound.htm', 'fr')


if __name__ == '__main__':
    unittest.main()
