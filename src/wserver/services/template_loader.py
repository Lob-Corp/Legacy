from pathlib import Path
import re
from typing import Dict, Optional, Tuple


class TemplateService:
    """
    Template service for rendering templates.
    Notes:
    - need to support both gwsetup and gwd templates
    - Searches for templates in sensible locations
      (src/wserver/templates/gwsetup) WE HAVE TO ADD THE GWD TEMPLATE
    - Loads static/css/setup.css (if present) and injects it for %fsetup.css;
      (WORK ONLY FOR GWSETUP HAVE TO BE CHANGED/IMPROVED for gwd)
    """

    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = Path(__file__).resolve(
        ).parents[3] if repo_root is None else Path(repo_root)
        self.setup_lang_dir = (self.repo_root /
                               "src" / "wserver" / "templates" / "gwsetup")
        # css location requested: src/wserver/static/css (project layout)
        self.static_css_dir = (
            self.repo_root / "src" / "wserver" / "static" / "css"
        )
        # handle all '%' that refer to template directives

    def _resolve_template_file(self, fname: str
                               ) -> Tuple[Optional[Path], Optional[Path]]:
        """
        Try to find the template file and return (file_path,)
        TO BE MODIFIED FOR GWD AND FIX ODD SEARCH
        """
        name = Path(fname).name  # sanitize
        candidates_dirs = [self.setup_lang_dir]

        exts = ["", ".htm", ".html", ".txt"]
        for d in candidates_dirs:
            if d is None:
                continue
            for ext in exts:
                p = d / f"{name}{ext}"
                try:
                    if p.exists() and p.is_file():
                        return p, d
                except Exception:
                    continue
        return None, None

    def _load_css_text(self) -> str:
        """
        TO BE MODIFIED FOR GWD
        Load css
        """
        p = self.static_css_dir / "setup.css"
        try:
            if p.exists() and p.is_file():
                return p.read_text(encoding="utf-8", errors="ignore").strip()
        except Exception:
            pass
        return ""

    def translate(self, key: str, lang: str) -> str:
        """
        Minimal translation helper placeholder.
        """
        return key

    def render_gwsetup_template(self, fname: str) -> str:
        """
        Render a template
        """
        fname = Path(fname).name  # sanitize
        file_path, base_dir = self._resolve_template_file(fname)
        if file_path is None:
            raise FileNotFoundError(f"Template {fname} not found")
        raw = file_path.read_text(encoding="utf-8", errors="ignore")

        # TODO: VERIFIE HOW TO HANDLE REDIRECT PROPERLY
        raw = re.sub(r'(<head[^>]*>)', r'\1<base href="/">',
                     raw, flags=re.I, count=1)

        # inject css
        css_text = self._load_css_text()
        raw = raw.replace(
            '%fsetup.css;', f"<style>{css_text}</style>" if css_text else "")

        # remove stray %... (cleanup template artifacts)
        raw = re.sub(r'%[A-Za-z0-9_;().,-]+', '', raw)
        raw = raw.replace('%%', '%')

        # trailer/footer (legacy)
        trailer_html = (
            '<br><div id="footer"><hr><div><em>'
            '<a href="https://github.com/geneweb/geneweb/">'
            '<img src="/images/logo_bas.png" style="border:0"></a> '
            'Version - Copyright &copy; 1998-2021'
            '</em></div></div>'
        )
        return raw + trailer_html

    def render_gwd_template(
            self, fname: str, lang: str, params: Dict[str, str]) -> str:
        """
        Render a GWD template
        TO BE IMPLEMENTED
        """
        raise NotImplementedError("GWD template rendering not yet implemented")
