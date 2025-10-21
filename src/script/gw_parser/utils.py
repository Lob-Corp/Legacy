"""Utility functions for parsing GeneWeb files.

Contains helper functions for tokenization, field extraction,
and text processing.
"""

from typing import List, Sequence, Tuple


def copy_decode(s: str, i1: int, i2: int) -> str:
    """Decode word slice, translating '\\x' (escaped) and '_' -> ' '.

    In the OCaml code: replaces "\\" sequences and underscores.
    Here we simplify:
    - backslash followed by any char copies that char
    - '_' becomes space
    """
    out: List[str] = []
    i = i1
    while i < i2:
        c = s[i]
        if c == '\\' and i + 1 < i2:
            out.append(s[i + 1])
            i += 2
            continue
        if c == '_':
            out.append(' ')
        else:
            out.append(c)
        i += 1
    return ''.join(out)


def fields(line: str) -> List[str]:
    """Split line into tokens, decoding each token."""
    tokens: List[str] = []
    n = len(line)
    i = 0
    while i < n:
        while i < n and line[i] in (' ', '\t'):
            i += 1
        if i >= n:
            break
        start = i
        while i < n and line[i] not in (' ', '\t'):
            i += 1
        tokens.append(copy_decode(line, start, i))
    return tokens


def cut_space(x: str) -> str:
    """Trim whitespace from string."""
    return x.strip()


def get_field(label: str, tokens: Sequence[str]) -> Tuple[str, List[str]]:
    """Extract a labeled field from token list.

    Args:
        label: The field label (e.g., '#p', '#c')
        tokens: Token sequence

    Returns:
        Tuple of (field_value, remaining_tokens)
    """
    if len(tokens) >= 2 and tokens[0] == label:
        return cut_space(tokens[1]), list(tokens[2:])
    return "", list(tokens)


def strip_trailing_spaces(text: str) -> str:
    """Strip trailing spaces from each line and remove trailing empty lines."""
    lines = text.split('\n')
    cleaned = [ln.rstrip(' \t') for ln in lines]
    # Remove trailing empty lines
    while cleaned and cleaned[-1] == '':
        cleaned.pop()
    return '\n'.join(cleaned)
