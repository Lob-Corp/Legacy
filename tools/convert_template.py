#!/usr/bin/env python3
"""
GeneWeb to Jinja2 Template Converter - Fixed Version
Handles inline conditionals properly
"""

import re
import sys
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass


@dataclass
class ConversionContext:
    """Context for tracking conversion state"""
    in_macro: bool = False
    macro_params: List[str] = None

    def __post_init__(self):
        if self.macro_params is None:
            self.macro_params = []


class GenWebToJinjaConverter:
    def __init__(self):
        self.macros_defined: Dict[str, List[str]] = {}
        self.macro_calls: List[str] = []

    def convert(self, text: str) -> str:
        """Main conversion function"""
        text = self.convert_interp_blocks(text)
        # Process in order - CRITICAL: order matters!
        text = self.convert_comments(text)
        text = self.convert_special_vars(text)
        text = self.convert_translations(text)
        # Convert macro calls with %end; BEFORE conditionals
        text = self.convert_macro_calls(text)
        text = self.convert_macros(text)
        text = self.convert_includes(text)
        text = self.convert_lets(text)
        # NEW: Convert inline conditionals BEFORE block conditionals
        text = self.convert_inline_conditionals(text)
        text = self.convert_conditionals(text)
        text = self.convert_loops(text)
        text = self.convert_end_tags(text)
        text = self.convert_variables(text)
        text = self.fix_exprs_in_jinja_tags(text)
        text = self.cleanup(text)
        # CRITICAL: Fix any remaining = that should be ==
        text = self.fix_remaining_comparisons(text)
        text = self.fix_nested_jinja_calls(text)
        return text

    def fix_exprs_in_jinja_tags(self, text: str) -> str:
        """
        Remove '{{ ... }}' that appear inside Jinja block tags '{% ... %}'.
        This avoids producing invalid constructs like:
          {% set l1 = {{ language(i) }} %}
        by turning them into:
          {% set l1 = language(i) %}
        """
        import re

        def repl_tag(m):
            inner = m.group(1)
            # remove any {{ ... }} wrappers inside the tag content
            inner_clean = re.sub(r'\{\{\s*(.*?)\s*\}\}', r'\1', inner, flags=re.DOTALL)
            return '{% ' + inner_clean.strip() + ' %}'

        return re.sub(r'\{%\s*(.*?)\s*%\}', repl_tag, text, flags=re.DOTALL)

    def convert_interp_blocks(self, text: str) -> str:
        """
        Convert GeneWeb %apply;interp([ ... ]) blocks into a Jinja interp(mapping)
        where mapping values are expressions that concatenate literals and variables
        using Jinja ~ so variables are evaluated (not left inside quoted literals).

        Example input:
          %apply;interp([
          af: Daar was %nb_accesses; besoeke
          en: There has been %nb_accesses; accesses
          ])
        becomes:
          {{ interp({'af': 'Daar was ' ~ nb_accesses ~ ' besoeke', 'en': 'There has been ' ~ nb_accesses ~ ' accesses'}) }}
        """

        import re

        out = []
        i = 0
        n = len(text)
        while True:
            m = re.search(r'%apply;interp\(\[', text[i:], flags=re.DOTALL)
            if not m:
                out.append(text[i:])
                break
            start = i + m.start()
            out.append(text[i:start])
            # find the closing "])" corresponding to this opening
            j = start + m.end() - m.start()  # position after "%apply;interp(["
            # scan until we find the sequence "])" (we assume no nested brackets in interp block)
            close_idx = text.find('])', j)
            if close_idx == -1:
                # malformed: no closing ]) -> leave as-is and continue
                out.append(text[start:start + 1])
                i = start + 1
                continue
            block = text[j:close_idx]  # content between '[' and ']'
            # parse block lines into language entries
            lines = block.splitlines()
            entries = {}
            cur_code = None
            cur_buf = []
            code_re = re.compile(r'^\s*([a-zA-Z0-9_+-]+)\s*:\s*(.*)$')
            for line in lines:
                mcode = code_re.match(line)
                if mcode:
                    # store previous
                    if cur_code is not None:
                        entries[cur_code] = '\n'.join([l.rstrip() for l in cur_buf]).rstrip()
                    cur_code = mcode.group(1)
                    cur_buf = [mcode.group(2) or ""]
                else:
                    # continuation line
                    if cur_code is not None:
                        cur_buf.append(line)
                    else:
                        # stray line before first code -> ignore or attach to default
                        pass
            if cur_code is not None:
                entries[cur_code] = '\n'.join([l.rstrip() for l in cur_buf]).rstrip()

            # helper to build a Jinja concatenation expression from a template string
            ph_re = re.compile(r'%([a-zA-Z0-9_]+);')
            def make_concat_expr(s: str) -> str:
                parts = []
                last = 0
                for mm in ph_re.finditer(s):
                    lit = s[last:mm.start()]
                    if lit:
                        # escape single quotes
                        lit_escaped = lit.replace("'", "\\'")
                        parts.append(f"'{lit_escaped}'")
                    var = mm.group(1)
                    # variable name as Jinja expression (no {{ }})
                    parts.append(var)
                    last = mm.end()
                # trailing literal
                tail = s[last:]
                if tail:
                    tail_escaped = tail.replace("'", "\\'")
                    parts.append(f"'{tail_escaped}'")
                if not parts:
                    return "''"
                if len(parts) == 1:
                    return parts[0]
                return ' ~ '.join(parts)

            # build mapping string
            mapping_items = []
            for code, val in entries.items():
                expr = make_concat_expr(val)
                # keys must be quoted
                key = code.replace("'", "\\'")
                mapping_items.append(f"'{key}': {expr}")
            mapping = '{' + ', '.join(mapping_items) + '}'

            replacement = '{{ interp(' + mapping + ') }}'

            out.append(replacement)
            # advance i past the closing '])'
            i = close_idx + 2

        return ''.join(out)

    def fix_nested_jinja_calls(self, text: str) -> str:
        """
        Fix cases where the converter produced a premature '}}' inside a macro call,
        e.g.:
          {{ date(_('date/dates') }}, "e_datexcnt", "event_date")
        should become:
          {{ date(_('date/dates'), "e_datexcnt", "event_date") }}
        This function scans for '{{ name(' occurrences, detects a '}}' that occurs
        before the macro's closing ')', and moves the '}}' after that closing ')'.
        """
        import re

        i = 0
        while True:
            m = re.search(r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\(', text[i:])
            if not m:
                break
            match_start = i + m.start()
            name = m.group(1)
            pos_open = i + m.end() - 1  # index of '('
            pos_close_braces = text.find('}}', pos_open)
            if pos_close_braces == -1:
                # no closing braces, nothing to fix for this occurrence
                i = pos_open + 1
                continue

            # If there's no comma right after the '}}', it's likely fine
            after = text[pos_close_braces + 2 : pos_close_braces + 4]
            if not after or after.lstrip().startswith(','):
                # compute paren balance between opening paren and the '}}'
                sub = text[pos_open:pos_close_braces]
                depth = sub.count('(') - sub.count(')')
                # if depth > 0, the macro call is not closed yet -> '}}' is premature
                if depth > 0:
                    # find the position where depth goes to zero scanning after pos_close_braces
                    k = pos_close_braces + 2
                    n = len(text)
                    while k < n:
                        ch = text[k]
                        if ch == '(':
                            depth += 1
                        elif ch == ')':
                            depth -= 1
                            if depth == 0:
                                break
                        k += 1
                    if k < n and depth == 0:
                        # Move '}}' to just after that closing parenthesis (index k)
                        # Build new text:
                        before = text[:pos_close_braces]                    # up to '}}'
                        middle = text[pos_close_braces + 2 : k + 1]        # contents between '}}' and the closing ')'
                        after_rest = text[k + 1:]                          # remainder
                        # Ensure spacing is OK
                        new_expr = before + middle + ' }}' + after_rest
                        text = new_expr
                        # continue scanning after the moved '}}' to avoid infinite loop
                        i = match_start + len(name) + 4
                        continue
            # nothing to fix here, continue after this match
            i = pos_close_braces + 2
        return text

        # Keep applying until no more matches (handle nested cases)
        prev_text = None
        while prev_text != text:
            prev_text = text
            text = pattern.sub(replacer, text)

        return text

    def convert_inline_conditionals(self, text: str) -> str:
        """
        Convert inline conditionals like:
        %if;friend;primary%elseif;wizard;success%end;
        to: {% if friend %}primary{% elif wizard %}success{% endif %}

        These are conditionals WITHOUT parentheses, used for inline values.
        """
        # Pattern: %if;condition;value%elseif;condition2;value2%end;
        # or: %if;condition;value%else;value2%end;
        # or: %if;condition;value%end;

        def normalize_condition(cond: str) -> str:
            """Normalize a condition (convert = to ==, handle comparisons)"""
            # Handle != first
            cond = re.sub(
                r'([a-zA-Z_][a-zA-Z0-9_.]*?)\s*!=\s*"([^"]*)"', r"\1 != '\2'", cond)
            cond = re.sub(
                r'([a-zA-Z_][a-zA-Z0-9_.]*?)\s*!=\s*([a-zA-Z0-9_]+)', r'\1 != \2', cond)

            # Handle = with quotes
            cond = re.sub(
                r'([a-zA-Z_][a-zA-Z0-9_.]*?)\s*=\s*"([^"]*)"', r"\1 == '\2'", cond)

            # Handle = with numbers
            cond = re.sub(
                r'([a-zA-Z_][a-zA-Z0-9_.]*?)\s*=\s*(\d+)', r'\1 == \2', cond)

            # Handle = with variables (but not ==)
            cond = re.sub(
                r'([a-zA-Z_][a-zA-Z0-9_.]*?)\s*=(?!=)\s*([a-zA-Z_][a-zA-Z0-9_]*)\b', r"\1 == '\2'", cond)

            return cond.strip()

        def convert_inline(match):
            full_match = match.group(0)

            # Parse the inline conditional
            parts = []
            pos = 0

            # Match %if;condition;value
            if_match = re.match(r'%if;([^;%]+);([^%]+)', full_match[pos:])
            if not if_match:
                return full_match

            condition = normalize_condition(if_match.group(1))
            value = if_match.group(2).strip()
            parts.append(('if', condition, value))
            pos += if_match.end()

            # Look for %elseif; or %else; or %end;
            while pos < len(full_match):
                remaining = full_match[pos:]

                # Check for %elseif;condition;value
                elseif_match = re.match(r'%elseif;([^;%]+);([^%]+)', remaining)
                if elseif_match:
                    condition = normalize_condition(elseif_match.group(1))
                    value = elseif_match.group(2).strip()
                    parts.append(('elif', condition, value))
                    pos += elseif_match.end()
                    continue

                # Check for %else;value
                else_match = re.match(r'%else;([^%]+)', remaining)
                if else_match:
                    value = else_match.group(1).strip()
                    parts.append(('else', None, value))
                    pos += else_match.end()
                    continue

                # Check for %end;
                if remaining.startswith('%end;'):
                    break

                # Unknown pattern, bail out
                return full_match

            # Build Jinja2 output
            result = []
            for i, (kind, condition, value) in enumerate(parts):
                if kind == 'if':
                    result.append(f'{{% if {condition} %}}{value}')
                elif kind == 'elif':
                    result.append(f'{{% elif {condition} %}}{value}')
                elif kind == 'else':
                    result.append(f'{{% else %}}{value}')
            result.append('{% endif %}')

            return ''.join(result)

        # Match inline conditionals (no parens after %if;)
        # Must not match %if;( which is a block conditional
        text = re.sub(
            r'%if;(?!\()([^;%]+);([^%]+)(?:%elseif;[^;%]+;[^%]+)*(?:%else;[^%]+)?%end;',
            convert_inline,
            text
        )

        return text

    def convert_conditionals(self, text: str) -> str:
        """
        Convert GeneWeb block conditionals to Jinja2.

        Handles forms:
          - %if;(condition)  ... %elseif;(cond) ... %else; ... %end;
          - %if;condition;      (no-paren inline/block form)
        Also fixes artifacts like "{{ if }}cond;" emitted by earlier passes.
        """
        import re

        def normalize_condition(cond: str) -> str:
            # Normalize comparisons: !=, = -> == (but keep existing ==)
            cond = cond.strip()

            # protect existing == and !=
            cond = re.sub(r'(?<![=!])=(?!=)', ' == ', cond)
            # convert typical quoted values to single-quoted for Jinja
            cond = re.sub(r'==\s*"([^"]*)"', r"== '\1'", cond)
            cond = re.sub(r'!=\s*"([^"]*)"', r"!= '\1'", cond)

            # convert evar_foo or evar.foo style used in GeneWeb to evar.foo
            cond = re.sub(r'\bevar_([a-zA-Z_][a-zA-Z0-9_]*)\b', r'evar.\1', cond)
            cond = re.sub(r'\bbvar_([a-zA-Z_][a-zA-Z0-9_]*)\b', r'bvar.\1', cond)

            # map some GeneWeb shorthands
            cond = re.sub(r'\bcnt\b', 'loop.index', cond)
            cond = re.sub(r'\bis_last\b', 'loop.last', cond)
            cond = re.sub(r'\bis_first\b', 'loop.first', cond)

            return cond.strip()

        def find_matching_paren(s: str, open_pos: int) -> int:
            depth = 1
            i = open_pos + 1
            while i < len(s) and depth > 0:
                if s[i] == '(':
                    depth += 1
                elif s[i] == ')':
                    depth -= 1
                i += 1
            return i - 1 if depth == 0 else -1

        # 1) Convert parenthesized %if;( ... ) and %elseif;( ... ) forms (scan to handle nested parentheses)
        out = []
        pos = 0
        while True:
            m = re.search(r'%if;\(', text[pos:])
            if not m:
                out.append(text[pos:])
                break
            start = pos + m.start()
            out.append(text[pos:start])
            paren_open = start + m.group(0).rfind('(')
            paren_close = find_matching_paren(text, paren_open)
            if paren_close == -1:
                # malformed, append token as-is and continue
                out.append(text[start:start + len(m.group(0))])
                pos = start + len(m.group(0))
                continue
            cond = text[paren_open + 1:paren_close]
            out.append(f'{{% if {normalize_condition(cond)} %}}')
            pos = paren_close + 1
        text = ''.join(out)

        # %elseif;(...) same technique (simple replace now because parens handled above)
        out = []
        pos = 0
        while True:
            m = re.search(r'%elseif;\(', text[pos:])
            if not m:
                out.append(text[pos:])
                break
            start = pos + m.start()
            out.append(text[pos:start])
            paren_open = start + m.group(0).rfind('(')
            paren_close = find_matching_paren(text, paren_open)
            if paren_close == -1:
                out.append(text[start:start + len(m.group(0))])
                pos = start + len(m.group(0))
                continue
            cond = text[paren_open + 1:paren_close]
            out.append(f'{{% elif {normalize_condition(cond)} %}}')
            pos = paren_close + 1
        text = ''.join(out)

        # 2) Convert no-paren form: %if;cond;  and %elseif;cond;
        # Use non-greedy match for cond up to the terminating semicolon
        text = re.sub(r'%if;\s*([^;()]+);', lambda m: f'{{% if {normalize_condition(m.group(1))} %}}', text)
        text = re.sub(r'%elseif;\s*([^;()]+);', lambda m: f'{{% elif {normalize_condition(m.group(1))} %}}', text)

        # 3) Convert %else; -> {% else %}
        text = text.replace('%else;', '{% else %}')

        # 4) Fix artifacts like "{{ if }}cond;" produced by earlier passes:
        #    Replace patterns "{{ if }}COND;" -> "{% if COND %}"
        def fix_artifact(m):
            cond = m.group(1).strip()
            if cond.endswith(';'):
                cond = cond[:-1].strip()
            return '{% if ' + normalize_condition(cond) + ' %}'
        text = re.sub(r'\{\{\s*if\s*\}\}\s*([^%<\n]+);', fix_artifact, text)

        # Also fix "{{ elif }}COND;" and "{{ else }}" if present
        def fix_elif_artifact(m):
            cond = m.group(1).strip()
            if cond.endswith(';'):
                cond = cond[:-1].strip()
            return '{% elif ' + normalize_condition(cond) + ' %}'
        text = re.sub(r'\{\{\s*elif\s*\}\}\s*([^%<\n]+);', fix_elif_artifact, text)
        text = re.sub(r'\{\{\s*else\s*\}\}', '{% else %}', text)

        return text

    def convert_comments(self, text: str) -> str:
        """Convert %( comment %) to {# comment #}"""
        def replace_comment(match):
            return '{# ' + match.group(1) + ' #}'
        text = re.sub(r'%\((.*?)%\)', replace_comment, text, flags=re.DOTALL)
        return text

    def convert_special_vars(self, text: str) -> str:
        """Convert special variables like %sq;, %nn;, %nl;"""
        text = re.sub(r'%sq;\s*', '', text)
        text = re.sub(r'%nn;[ \t\r]*\n?[ \t\r]*', '', text)
        text = text.replace('%nl;', '\n')
        return text

    def convert_translations(self, text: str) -> str:
        """Convert [translation] to {{ _('translation') }} or just _('translation') if inside %apply;"""
        # [!dates order]0 -> dates_order (special variable, not translation)
        text = re.sub(
            r'\[!([a-zA-Z0-9_ ]+)\](\d+)',
            lambda m: m.group(1).replace(' ', '_'),
            text
        )

        def should_convert(text: str, pos: int) -> bool:
            """Check if we should convert bracket at position"""
            start = max(0, pos - 200)
            snippet = text[start:pos + 100]
            pattern_idx = snippet.rfind('pattern="')
            if pattern_idx == -1:
                return True
            after_pattern = snippet[pattern_idx + 9:]
            our_pos = pos - start - pattern_idx - 9
            if our_pos < 0:
                return True
            close_quote = after_pattern.find('"')
            return close_quote != -1 and our_pos > close_quote

        def is_inside_apply(text: str, pos: int) -> bool:
            """Check if position is inside an %apply; call"""
            # Look backwards for %apply; within reasonable distance
            start = max(0, pos - 100)
            snippet = text[start:pos]
            apply_pos = snippet.rfind('%apply;')
            if apply_pos == -1:
                return False
            # Check if there's a closing ) before our position
            after_apply = snippet[apply_pos:]
            paren_open = after_apply.find('(')
            if paren_open == -1:
                return False
            return True

        def convert_translation(match):
            if not should_convert(text, match.start()):
                return match.group(0)
            # If inside %apply;, don't wrap in {{ }}
            if is_inside_apply(text, match.start()):
                return f"_('{match.group(1)}')"
            return f"{{{{ _('{match.group(1)}') }}}}"

        text = re.sub(r'\[\*([a-zA-Z0-9_/:. -]+)\]\d*',
                    convert_translation, text)

        def convert_simple_translation(match):
            if len(match.group(1)) <= 2 or not should_convert(text, match.start()):
                return match.group(0)
            # If inside %apply;, don't wrap in {{ }}
            if is_inside_apply(text, match.start()):
                return f"_('{match.group(1)}')"
            return f"{{{{ _('{match.group(1)}') }}}}"

        text = re.sub(r'\[([a-zA-Z][a-zA-Z0-9_/:. -]+)\]\d*',
                    convert_simple_translation, text)

        return text

    def convert_macros(self, text: str) -> str:
        """Convert %define; macros to {% macro %}"""
        macros = []
        pos = 0

        while True:
            match = re.search(
                r'%define;([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)', text[pos:])
            if not match:
                break

            start = pos + match.start()
            name = match.group(1)
            params_str = match.group(2)
            params = [p.strip() for p in params_str.split(',') if p.strip()]

            body_start = start + len(match.group(0))
            body_end = self.find_matching_end(text, body_start)
            body = text[body_start:body_end]

            macros.append({
                'start': start,
                'end': body_end + 5,
                'name': name,
                'params': params,
                'body': body
            })

            self.macros_defined[name] = params
            pos = body_start

        for macro in reversed(macros):
            ctx = ConversionContext(
                in_macro=True, macro_params=macro['params'])
            body = self.convert_macro_body(macro['body'], ctx)
            params_str = ', '.join(macro['params']) if macro['params'] else ''
            replacement = f'{{% macro {macro["name"]}({params_str}) %}}\n{body}\n{{% endmacro %}}'
            text = text[:macro['start']] + replacement + text[macro['end']:]

        return text

    def find_matching_end(self, text: str, start: int) -> int:
        """Find matching %end; for a construct by tracking nesting"""
        depth = 1
        pos = start
        openers = [
            (r'%if;', 4),
            (r'%foreach;', 9),
            (r'%for;', 5),
            (r'%define;', 8)
        ]

        while pos < len(text) and depth > 0:
            candidates = []
            for pattern, length in openers:
                match_pos = text.find(pattern, pos)
                if match_pos != -1:
                    candidates.append(('open', match_pos, length))

            end_pos = text.find('%end;', pos)
            if end_pos != -1:
                candidates.append(('close', end_pos, 5))

            if not candidates:
                break

            candidates.sort(key=lambda x: x[1])
            kind, cand_pos, length = candidates[0]

            if kind == 'close':
                depth -= 1
                if depth == 0:
                    return cand_pos
                pos = cand_pos + length
            else:
                depth += 1
                pos = cand_pos + length

        return len(text)

    def convert_macro_body(self, body: str, ctx: ConversionContext) -> str:
        """Convert macro body with parameter substitution"""
        body = self.convert_special_vars(body)
        body = self.convert_lets(body)
        body = self.convert_conditionals(body)
        body = self.convert_loops(body)

        for param in ctx.macro_params:
            body = re.sub(r'%' + re.escape(param) + r';',
                          lambda m: f'{{{{ {param} }}}}', body)
            pattern = r'(name|id|for)="(' + re.escape(param) + \
                r')(_[a-zA-Z0-9_]+)"'
            def replacement(
                m): return f'{m.group(1)}="{{{{ {param} }}}}{m.group(3)}"'
            body = re.sub(pattern, replacement, body)

        return body

    def convert_lets(self, text: str) -> str:
        """Convert %let;var;value%in; to {% set var = value %}"""
        def convert_let(match):
            var = match.group(1)
            value = match.group(2).strip()
            if '=' in value:
                value_escaped = value.replace("'", "\\'")
                return f'{{% set {var} = \'{value_escaped}\' %}}'
            else:
                return f'{{% set {var} = {value} %}}'

        text = re.sub(
            r'%let;([a-zA-Z_][a-zA-Z0-9_]*);([^%]+)%in;', convert_let, text)
        return text

    def convert_loops(self, text: str) -> str:
        """Convert %foreach; and %for; to Jinja2"""
        text = re.sub(
            r'%foreach;([a-zA-Z_][a-zA-Z0-9_]*);',
            lambda m: f'{{% for {m.group(1)} in {m.group(1)}s %}}',
            text
        )
        text = re.sub(
            r'%for;([a-zA-Z_]+);(\d+);(\d+);',
            lambda m: f'{{% for {m.group(1)} in range({m.group(2)}, {m.group(3)}+1) %}}',
            text
        )
        text = text.replace('%cnt;', '{{ loop.index }}')
        text = re.sub(r'%if;\(is_last\)', '{% if loop.last %}', text)
        text = re.sub(r'%if;\(is_first\)', '{% if loop.first %}', text)
        return text

    def convert_includes(self, text: str) -> str:
        """Convert %include; to {% include %}"""
        text = re.sub(
            r'%include;([a-zA-Z_][a-zA-Z0-9_]*)',
            r"{% include '\1.html' %}",
            text
        )
        text = re.sub(
            r'%include_([a-zA-Z_]+);',
            r'{{ \1|safe }}',
            text
        )
        return text

    def convert_macro_calls(self, text: str) -> str:
        """Convert %apply; to {{ macro() }}"""
        def convert_with_and_call(match):
            name = match.group(1)
            full_args = match.group(2)
            self.macro_calls.append(name)
            args = re.split(r'%and;', full_args)
            clean_args = []
            for arg in args:
                arg = arg.strip()
                if not arg:
                    continue
                if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', arg):
                    clean_args.append(arg)
                elif (arg.startswith('"') and arg.endswith('"')) or \
                     (arg.startswith("'") and arg.endswith("'")):
                    clean_args.append(arg)
                else:
                    clean_args.append(f'"{arg}"')
            args_str = ', '.join(clean_args)
            return f'{{{{ {name}({args_str}) }}}}'

        text = re.sub(
            r'%apply;([a-zA-Z_][a-zA-Z0-9_]*)%with;(.+?)%end;',
            convert_with_and_call,
            text,
            flags=re.DOTALL
        )

        text = re.sub(
            r'%apply;([a-zA-Z_][a-zA-Z0-9_]*)\(([^)]+)\)',
            lambda m: (self.macro_calls.append(m.group(1)),
                       f'{{{{ {m.group(1)}({m.group(2)}) }}}}')[1],
            text
        )

        text = re.sub(
            r'%apply;([a-zA-Z_][a-zA-Z0-9_]*)(?!%with;|%and;|\()',
            lambda m: (self.macro_calls.append(m.group(1)),
                       f'{{{{ {m.group(1)}() }}}}')[1],
            text
        )

        return text

    def convert_end_tags(self, text: str) -> str:
        """
        Replace legacy '%end;' by the correct Jinja closing tag.

        Strategy:
        - Scan the (already partially converted) text for Jinja open/close tags
          and for remaining legacy openers (%if;, %foreach;, %for;, %define;).
        - Maintain a LIFO stack of openers; when seeing a %end; pop the last opener
          and emit the corresponding Jinja closing tag ({% endif %}, {% endfor %}, ...).
        - Preserve other text and existing Jinja tags unchanged.
        This handles cases where conditionals were already converted to Jinja
        before %end; replacement.
        """
        token_re = re.compile(
            r'(\{\%\s*(if|for|macro|elif|else|endif|endfor|endmacro)\b.*?\%\}|%foreach;|%for;|%define;|%if;|%end;)',
            re.DOTALL
        )

        out_parts: List[str] = []
        stack: List[str] = []
        pos = 0

        for m in token_re.finditer(text):
            start, endp = m.start(), m.end()
            token = m.group(1)
            # append text before token
            if pos < start:
                out_parts.append(text[pos:start])

            # Jinja tag (already converted)
            if token.startswith('{%'):
                inner = token[2:-2].strip()
                first = inner.split()[0] if inner else ''
                tag = first.lower()
                if tag in ('if', 'for', 'macro'):
                    stack.append(tag)
                elif tag in ('endif', 'endfor', 'endmacro'):
                    # keep stack consistent if possible
                    if stack:
                        stack.pop()
                # emit Jinja tag unchanged
                out_parts.append(token)

            # Legacy openers that may remain
            elif token.startswith('%if;'):
                # push an 'if' opener; emit nothing (we assume conditionals were converted earlier)
                stack.append('if')
                out_parts.append(token)
            elif token.startswith('%foreach;') or token.startswith('%for;'):
                stack.append('for')
                out_parts.append(token)
            elif token.startswith('%define;'):
                stack.append('macro')
                out_parts.append(token)

            # %end; -> pop last opener and emit matching Jinja end
            elif token == '%end;':
                if stack:
                    opener = stack.pop()
                    if opener == 'if':
                        out_parts.append('{% endif %}')
                    elif opener == 'for':
                        out_parts.append('{% endfor %}')
                    elif opener == 'macro':
                        out_parts.append('{% endmacro %}')
                    else:
                        out_parts.append('{% endif %}')
                else:
                    # fallback if nothing to close
                    out_parts.append('{% endif %}')
            else:
                # unknown token, keep as-is
                out_parts.append(token)

            pos = endp

        # append remainder
        out_parts.append(text[pos:])
        return ''.join(out_parts)

    def convert_variables(self, text: str) -> str:
        """Convert %variable; to {{ variable }}"""
        special = {
            '%lang;': '{{ lang }}',
            '%images_prefix;': "{{ url_for('static', filename='images/') }}",
            '%action;': '{{ action }}',
            '%digest;': '{{ digest }}',
            '%body_prop;': '{{ body_prop }}',
            '%comment;': '{{ comment }}',
            '%fsources;': '{{ fsources }}',
            '%origin_file;': '{{ origin_file }}',
            '%message_to_wizard;': '{{ message_to_wizard }}',
            '%base_trailer;': '{{ base_trailer|safe }}',
            '%prefix_base_password;': "{{ url_for('index') }}",
            '%hidden;': '',
        }

        for gw, jinja in special.items():
            text = text.replace(gw, jinja)

        text = re.sub(r'%evar_([a-zA-Z_][a-zA-Z0-9_]*);',
                      r'{{ evar.\1 }}', text)
        text = re.sub(r'%evar\.([a-zA-Z_][a-zA-Z0-9_]*);',
                      r'{{ evar.\1 }}', text)
        text = re.sub(r'%bvar\.([a-zA-Z_][a-zA-Z0-9_]*);',
                      r'{{ bvar.\1 }}', text)
        text = re.sub(r'%([a-zA-Z_][a-zA-Z0-9_.]+);', r'{{ \1 }}', text)
        text = re.sub(
            r'(?<!\{)%([a-zA-Z_][a-zA-Z0-9_]*);(?!\})', r'{{ \1 }}', text)

        return text

    def cleanup(self, text: str) -> str:
        """Final cleanup"""
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'\{%\s+', '{% ', text)
        text = re.sub(r'\s+%\}', ' %}', text)
        text = re.sub(r'\{\{\s+', '{{ ', text)
        text = re.sub(r'\s+\}\}', ' }}', text)
        return text

    def fix_remaining_comparisons(self, text: str) -> str:
        """Fix any remaining single = in conditionals that should be =="""
        # Fix in {% if %} blocks
        def fix_if_condition(match):
            full_tag = match.group(0)
            # Only fix single = that's not already == or !=
            # Match var=value or var=1 but not var==value or var!=value
            fixed = re.sub(
                r'([a-zA-Z_][a-zA-Z0-9_.]*)\s*=(?!=)(?!!)\s*([a-zA-Z0-9_]+|"[^"]*")',
                r'\1 == \2',
                full_tag
            )
            return fixed

        # Fix {% if ... %} tags
        text = re.sub(
            r'\{%\s*if\s+[^%]+%\}',
            fix_if_condition,
            text
        )

        # Fix {% elif ... %} tags
        text = re.sub(
            r'\{%\s*elif\s+[^%]+%\}',
            fix_if_condition,
            text
        )

        return text

    def convert_file(self, input_file: str, output_file: str = None) -> str:
        """Convert a GeneWeb template file to Jinja2."""
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        converted = self.convert(content)

        header = """{# 
  Converted from GeneWeb template to Jinja2
  Generated automatically - ready to use
#}

"""
        converted = header + converted

        if output_file is None:
            output_file = input_file.replace('.txt', '.html')

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(converted)

        print(f"✓ Converted {input_file} -> {output_file}")
        print(f"✓ Found {len(self.macros_defined)} macros")
        print(f"✓ Converted {len(self.macro_calls)} macro calls")
        return converted


def main():
    if len(sys.argv) < 2:
        print("Usage: python genweb_to_jinja.py <input_file> [output_file]")
        print("Example: python genweb_to_jinja.py updfam.txt updfam.html")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    converter = GenWebToJinjaConverter()
    try:
        result = converter.convert_file(input_file, output_file)
        print("\n✓ Conversion completed successfully!")
        print("  The template is ready to use with Flask/Jinja2")
    except Exception as e:
        print(f"\n✗ Error during conversion: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
