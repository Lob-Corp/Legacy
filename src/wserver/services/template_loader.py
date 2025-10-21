from pathlib import Path
import re
import html
from typing import Dict, Optional, Tuple


class TemplateService:
    """
    Small service to load and render 'setup' templates (gwsetup):
      - search order: legacy/bin/setup/lang -> legacy/hd/etc (txt)
      - basic templm handling: remove %define/%let blocks, %include;, %fsetup.css;, %G/%D minimal
      - variables: %l; %m; %P; %a; %lang;
    Public API:
      TemplateService(repo_root).render_setup_template(fname, lang, params_dict) -> str
    """

    def __init__(self, repo_root: Optional[Path] = None):
        # TODO change Path to not use the legacy one
        self.repo_root = (
            Path(__file__).resolve().parents[3]
            if repo_root is None else Path(repo_root)
        )
        self.setup_lang_dir = (
            self.repo_root / "legacy" / "bin" / "setup" / "lang"
        )
        self.setup_dir = self.repo_root / "legacy" / "bin" / "setup"
        self.assets_dir = self.repo_root / "legacy" / "hd" / "etc"
        self.local_css = (
            self.repo_root / "src" / "wserver" / "css" / "setup.css"
        )
        self._lexicon = None

    # --- lexicon minimal loader used for %D translation ---
    def _parse_lexicon_file(self, p: Path):
        d = {}
        if not p.exists():
            return d
        with p.open(encoding="utf-8", errors="ignore") as fh:
            current_key = None
            current_trans = {}
            for ln in fh:
                ln = ln.rstrip("\n")
                m_key = re.match(r'^\s{4}(.+)\s*$', ln)
                m_trans = re.match(r'^([a-z]{2}(?:-[a-z]+)?):\s*(.*)$', ln)
                if m_key:
                    if current_key:
                        d.setdefault(current_key, {}).update(current_trans)
                    current_key = m_key.group(1).strip()
                    current_trans = {}
                elif m_trans and current_key is not None:
                    lang = m_trans.group(1)
                    txt = m_trans.group(2)
                    current_trans[lang] = txt
                elif ln.strip() == "":
                    if current_key:
                        d.setdefault(current_key, {}).update(current_trans)
                    current_key = None
                    current_trans = {}
                else:
                    continue
            if current_key:
                d.setdefault(current_key, {}).update(current_trans)
        return d

    def _load_lexicon(self):
        if self._lexicon is not None:
            return self._lexicon
        combined = {}
        for p in (
            self.assets_dir / "lexicon.txt",
            self.setup_lang_dir / "lexicon.txt"
        ):
            combined.update(self._parse_lexicon_file(p))
        self._lexicon = combined
        return combined

    def _translate_key(self, key: str, lang: str) -> str:
        lex = self._load_lexicon()
        if key in lex:
            entry = lex[key]
            if lang in entry:
                return entry[lang]
            if "en" in entry:
                return entry["en"]
            for v in entry.values():
                return v
        return key

    def _read_tail_of_file(self, p: Path, max_chars: int = 3000) -> str:
        try:
            if not p.exists():
                return ""
            s = p.read_text(encoding="utf-8", errors="ignore")
            return s[-max_chars:] if len(s) > max_chars else s
        except Exception:
            return ""

    def _resolve_template_file(self, fname: str) -> 'Tuple[Optional[Path], Optional[Path]]':
        """
        Return (file_path, base_dir) where the template is found.
        Search order: setup_lang_dir/fname, assets_dir/fname(.txt)
        """
        p1 = self.setup_lang_dir / fname
        if p1.exists():
            return p1, self.setup_lang_dir
        p2 = self.assets_dir / fname.replace('.htm', '.txt')
        if p2.exists():
            return p2, self.assets_dir
        return None, None

    def _load_css_text(self) -> str:
        for p in (
            self.setup_lang_dir / "setup.css",
            self.setup_dir / "setup.css",
            self.local_css
        ):
            if p.exists():
                try:
                    raw = p.read_text(encoding="utf-8", errors="ignore")
                    # remove possible HTML wrappers conservatively
                    m = re.search(
                        r'<style[^>]*>(.*?)</style>',
                        raw, flags=re.S | re.I
                    )
                    if m:
                        return m.group(1).strip()
                    raw = re.sub(r'<!--(.*?)-->', r'\1', raw, flags=re.S)
                    raw = re.sub(r'<[^>]+>', '', raw)
                    return raw.strip()
                except Exception:
                    continue
        return ""

    def render_setup_template(
            self, fname: str, lang: str, params: Dict[str, str]) -> str:
        """
        Main entry: fname like "welcome.htm", lang like "fr", params from URL query.
        Returns rendered HTML string (not Response).
        """
        fname = Path(fname).name  # sanitize
        file_path, base_dir = self._resolve_template_file(fname)
        if file_path is None:
            raise FileNotFoundError(f"Template {fname} not found")
        raw = file_path.read_text(encoding="utf-8", errors="ignore")

        # Inject <base href="/"> so relative URLs like "images/gwlogo.png" resolve to "/images/..."
        # This mirrors legacy behaviour where assets are served from repository root.
        raw = re.sub(
            r'(<head[^>]*>)',
            r'\1<base href="/">',
            raw, flags=re.I, count=1
        )

        # remove definitions and let-blocks
        raw = re.sub(r'%define;.*?%end;', '', raw, flags=re.DOTALL)
        raw = re.sub(r'%let;.*?%in;', '', raw, flags=re.DOTALL)
        raw = raw.replace('%end;', '')
        css_text = self._load_css_text()
        raw = raw.replace(
            '%fsetup.css;', f"<style>{css_text}</style>" if css_text else "")

        def include_repl(m):
            name = m.group(1)
            for ext in ("htm", "html", "txt"):
                p = base_dir / f"{name}.{ext}"
                if p.exists():
                    try:
                        return p.read_text(encoding="utf-8", errors="ignore")
                    except Exception:
                        return ""
            for ext in ("htm", "html", "txt"):
                p = self.assets_dir / f"{name}.{ext}"
                if p.exists():
                    try:
                        return p.read_text(encoding="utf-8", errors="ignore")
                    except Exception:
                        return ""
            return ""
        raw = re.sub(r'%include;([A-Za-z0-9_/-]+)', include_repl, raw)

        # variable substitutions minimal: handle both %name; and %name (legacy)
        ctx = {
            "l": lang,
            "lang": lang,
            "Vbody_prop": "",
            "m": params.get("host", ""),  # passed by caller (or empty)
            "P": params.get("port", ""),
            "a": params.get("o", ""),
        }
        # Replace %name; style first (preserve HTML escaping for values)
        raw = re.sub(
            r'%([A-Za-z0-9_]+);', lambda m: html.escape(
                str(ctx.get(m.group(1), ""))), raw)
        # Also replace bare %l and %lang occurrences left in some setup templates
        raw = raw.replace('%l', html.escape(str(ctx.get("l", ""))))
        raw = raw.replace('%lang', html.escape(str(ctx.get("lang", ""))))

        # %G{file} or %G -> tail of a log file (setup_dir candidates)
        def repl_G(m):
            fname_arg = m.group(1)
            candidates = []
            if fname_arg:
                candidates.append(self.setup_dir / fname_arg)
            candidates += [
                self.setup_dir / "gwsetup.log",
                self.setup_dir / "comm.log",
                self.setup_dir / "history",
                Path("gwsetup.log"),
            ]
            for p in candidates:
                if p.exists():
                    tail = self._read_tail_of_file(p, max_chars=3000)
                    return "<pre>{}</pre>".format(html.escape(tail))
            return ""
        raw = re.sub(r'%G(?:\{([^}]+)\})?', repl_G, raw)

        # %D -> translate !doc key from lexicon (fallback to key)
        doc_txt = self._translate_key("!doc", lang)
        raw = raw.replace('%D', html.escape(doc_txt))

        raw = re.sub(r'%[A-Za-z0-9_;().,-]+', '', raw)
        raw = raw.replace('%%', '%')

        # append trailer/footer minimal (same as legacy)
        trailer_html = (
            '<br><div id="footer"><hr><div><em>'
            '<a href="https://github.com/geneweb/geneweb/">'
            '<img src="/images/logo_bas.png" style="border:0"></a> '
            'Version - Copyright &copy; 1998-2021'
            '</em></div></div>'
        )
        return raw + trailer_html
