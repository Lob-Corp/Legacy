"""Main parser for GeneWeb .gw files.

Entry point for parsing GeneWeb genealogical data files.
"""

import sys
from typing import List

from .data_types import GwSyntax
from .stream import LineStream, iter_strip_lines
from .block_parser import parse_block


def parse_gw_file(path: str, encoding: str = 'utf-8',
                  no_fail: bool = False) -> List[GwSyntax]:
    """Parse a .gw file producing a list of GwSyntax variant objects.

    Args:
        path: Path to .gw file
        encoding: File encoding (default 'utf-8', can be overridden by
                  encoding directive)
        no_fail: If True, continue parsing after errors (collect errors but
                 don't raise)

    Returns:
        List of parsed GwSyntax blocks
    """
    from . import data_types as dt
    dt.gwplus_mode = False
    dt.no_fail_mode = no_fail

    # Detect encoding directive on first line
    detected_encoding = encoding
    with open(path, 'r', encoding='utf-8', errors='replace') as probe:
        first_line = probe.readline().strip()
        if first_line.startswith('encoding:'):
            enc_name = first_line[len('encoding:'):].strip()
            if enc_name.lower() in ('iso-8859-1', 'iso_8859_1', 'latin1'):
                detected_encoding = 'iso-8859-1'
            elif enc_name.lower() in ('utf-8', 'utf_8'):
                detected_encoding = 'utf-8'

    with open(path, 'r', encoding=detected_encoding) as fh:
        syntaxes: List[GwSyntax] = []
        stream = LineStream(iter_strip_lines(fh))
        line_num = 0

        while True:
            first = stream.pop()
            if first is None:
                break
            line_num += 1

            # Handle directives
            if first.startswith('encoding:'):
                # Already handled, skip
                continue
            if first.strip() == 'gwplus':
                dt.gwplus_mode = True
                continue

            try:
                block = parse_block(first, stream)
                if block is not None:
                    syntaxes.append(block)
            except Exception as e:
                if not dt.no_fail_mode:
                    raise RuntimeError(
                        f"Parse error at line ~{line_num}: {e}") from e
                print(f"Warning: Parse error at line ~{line_num}: {e}",
                      file=sys.stderr)

        return syntaxes
