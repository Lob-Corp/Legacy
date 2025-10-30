import os
import re


class Translator:
    """Load translations from the legacy gwd lexicon.txt format.
    """

    def __init__(self, lexicon_path=None):
        # default path relative to this file
        if lexicon_path:
            self.lexicon_path = lexicon_path
        else:
            self.lexicon_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..',
                             'static', 'lang', 'gwd', 'lexicon.txt')
            )
        self._data = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.lexicon_path):
            return
        key = None
        lang_re = re.compile(r"^(?P<lang>[a-z\-]+):\s*(?P<text>.*)$")
        with open(self.lexicon_path, 'r', encoding='utf-8',
                  errors='replace') as f:
            for raw in f:
                line = raw.rstrip('\n')
                if not line:
                    key = None
                    continue
                if line.lstrip().startswith('#'):
                    continue
                s = line.strip()
                m = lang_re.match(s)
                if m and key:
                    lang = m.group('lang')
                    text = m.group('text')
                    self._data.setdefault(key, {})[lang] = text
                    continue
                if s and not s.startswith('!'):
                    key = s
                    self._data.setdefault(key, {})
                    continue

    def gettext(self, key, lang='en', capitalize_first=False):
        """Return the translated string for `key` in `lang`.

        If `capitalize_first` is True, the returned string will have its
        first character upper-cased (Unicode-aware). If the key is not
        found, the key itself is returned (same behaviour as before).
        """
        if key in self._data:
            entry = self._data[key]
            if lang in entry:
                text = entry[lang]
            elif 'en' in entry:
                text = entry['en']
            else:
                text = next(iter(entry.values()))
        else:
            text = key

        if capitalize_first and text:
            # upper-case the first character correctly for Unicode
            first = text[0].upper()
            return first + text[1:]
        return text


_module_translator = None


def get_translator():
    global _module_translator
    if _module_translator is None:
        _module_translator = Translator()
    return _module_translator
