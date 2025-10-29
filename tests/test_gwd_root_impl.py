import re
from pathlib import Path

from flask import Flask

from wserver.routes.gwd_root_impl import implem_route_gwd_root


def _make_app():
	app = Flask(__name__)
	return app


class _FakePath:
	def __init__(self, name, is_file=True):
		# name should include extension like 'foo.db'
		self.name = name
		self._is_file = is_file

	def is_file(self):
		return self._is_file


def _patch_bases(monkeypatch, names):
	"""Monkeypatch Path.iterdir to return fake files with given names."""

	def fake_iterdir(self):
		return [_FakePath(n) for n in names]

	monkeypatch.setattr(Path, 'iterdir', fake_iterdir)


def test_gwd_root_default_language_contains_en_and_bases_list(monkeypatch):
	app = _make_app()
	# simulate bases folder contents
	_patch_bases(monkeypatch, ['Alpha.db', 'Beta.db'])

	# call without query param -> default lang 'en'
	with app.test_request_context('/gwd'):
		html = implem_route_gwd_root()

	assert 'lang="en"' in html
	# expect links to /gwd/Alpha and /gwd/Beta
	assert re.search(r'href="/gwd/Alpha(\?lang=en)?"', html)
	assert re.search(r'href="/gwd/Beta(\?lang=en)?"', html)
	# title should default to Base
	assert '<title>Base</title>' in html


def test_gwd_root_query_param_overrides_and_render_links_with_lang(monkeypatch):
	app = _make_app()
	_patch_bases(monkeypatch, ['One.db', 'Two.db'])

	with app.test_request_context('/gwd?lang=fr'):
		html = implem_route_gwd_root()

	# when lang query param is provided, links should include it
	assert 'lang="fr"' in html
	assert re.search(r'href="/gwd/One\?lang=fr"', html)
	assert re.search(r'href="/gwd/Two\?lang=fr"', html)
