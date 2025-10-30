import sys
from pathlib import Path

# Ensure repository root is on sys.path so `src` package can be imported
repo_root = str(Path(__file__).resolve().parents[1])
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.wserver.i18n.translator import Translator


def test_translator_loads_and_gettext(tmp_path):
    lex = tmp_path / "lexicon.txt"
    lex.write_text("""
greeting
en: Hello
fr: Bonjour

farewell
fr: Au revoir
""", encoding='utf-8')

    t = Translator(str(lex))
    assert t.gettext('greeting', 'en') == 'Hello'
    assert t.gettext('greeting', 'fr') == 'Bonjour'
    # fallback to available language when requested missing
    assert t.gettext('farewell', 'en') == 'Au revoir'
    # unknown key returns key
    assert t.gettext('unknown', 'en') == 'unknown'
