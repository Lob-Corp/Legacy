# mutils.py
# A modern Python conversion of Geneweb's mutil.ml module.

import os
import shutil
import time
import re
import unicodedata
import pickle
import hashlib
from pathlib import Path
from typing import List, Optional, Callable, Dict, Any, Tuple, TypeVar, Iterable
from dataclasses import dataclass, field
from urllib.parse import quote_plus, unquote_plus

# Platform-specific file locking
try:
    import fcntl
    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False
    
# --- Data Structures (equivalent to OCaml records) ---
# These would typically be in a separate `definitions.py` file.
# The `field(default_factory=list)` is needed for mutable default values.
@dataclass
class Person:
    first_name: str = "empty"
    surname: str = "empty"
    # ... other fields from Def.person would go here
    aliases: List[str] = field(default_factory=list)

@dataclass
class Family:
    marriage_place: str = "empty"
    # ... other fields from Def.family would go here
    witnesses: List[Person] = field(default_factory=list)

# --- Debugging and Performance ---

def bench(name: str, fn: Callable[[], Any]) -> Any:
    """
    Benchmarks a function's execution time (wall and CPU) and prints the result.
    Note: Python's GC stats are not as detailed as OCaml's.
    """
    print(f"Benchmarking '{name}'...")
    start_wall_time = time.perf_counter()
    start_cpu_time = time.process_time()
    
    result = fn()
    
    end_wall_time = time.perf_counter()
    end_cpu_time = time.process_time()
    
    wall_duration = end_wall_time - start_wall_time
    cpu_duration = end_cpu_time - start_cpu_time
    
    print(f"[{name}]: {wall_duration:.6f}s wall time (~{cpu_duration:.6f}s CPU time)")
    return result

# --- File System Operations ---

def mkdir_p(path: str, perm: int = 0o755):
    """Recursively creates a directory, equivalent to 'mkdir -p'."""
    Path(path).mkdir(parents=True, exist_ok=True, mode=perm)

def rm_rf(path: str):
    """
    Removes a file or a directory tree recursively. Does not fail if path does not exist.
    """
    p = Path(path)
    if p.is_dir():
        shutil.rmtree(p, ignore_errors=True)
    elif p.exists():
        p.unlink()

# --- Domain-Specific String Manipulation (Geneweb Logic) ---

def decline(case: str, s: str) -> str:
    """
    A direct translation of the OCaml 'decline' logic.
    This seems to be a legacy format for handling grammatical cases in names.
    Example: 'n' for nominative case.
    """
    # This complex logic is preserved as it is highly domain-specific.
    # In a real-world scenario, this might be re-evaluated for a simpler approach.
    def colon_to_at(text: str) -> str:
        # A simplified Python version of the complex recursive logic
        # It seems to transform "Name:variant" into "Name@(variant)"
        parts = []
        current_part = ""
        for char in text:
            if char in (' ', '<', '/'):
                if current_part:
                    parts.append(current_part.replace(':', '@(', 1) + ')')
                    current_part = ""
                parts.append(char)
            else:
                current_part += char
        if current_part:
             parts.append(current_part.replace(':', '@(', 1) + ')')
        return "".join(parts)
        
    if ':' not in s:
        return s
    return f"@(@({case}){colon_to_at(s)})"

def nominative(s: str) -> str:
    """If a colon is present, applies the 'nominative' decline rule."""
    if ':' in s:
        return decline('n', s)
    return s

def get_surname_pieces(surname: str, saints: List[str] = ["saint", "sainte"]) -> List[str]:
    """
    Splits a surname into significant pieces, ignoring saints and short parts.
    """
    surname_lower = surname.lower()
    words = surname_lower.split()
    
    pieces = []
    current_piece = []
    for word in words:
        if word in saints or len(word) <= 3:
            current_piece.append(word)
        else:
            if current_piece:
                pieces.append(" ".join(current_piece))
            current_piece = [word]
    
    if current_piece:
        pieces.append(" ".join(current_piece))
        
    return [p for p in pieces if len(p) > 3]

# --- General String & Text Processing ---

def translate_chars(text: str, char_from: str, char_to: str) -> str:
    """Replaces all occurrences of one character with another. Python's str.replace is better."""
    return text.replace(char_from, char_to)

def normalize_utf8_nfc(text: str) -> str:
    """Normalizes a UTF-8 string to NFC form."""
    return unicodedata.normalize('NFC', text)

def strip_all_trailing_spaces(s: str) -> str:
    """
    Removes trailing spaces and newlines from the end of the string,
    and reduces internal whitespace around newlines.
    """
    # Python's re module is great for this.
    # 1. Remove trailing whitespace from the whole string
    s = s.rstrip()
    # 2. Replace horizontal whitespace followed by a newline with just a newline
    s = re.sub(r'[ \t]+\n', '\n', s)
    # 3. Replace newline followed by horizontal whitespace with just a newline
    s = re.sub(r'\n[ \t]+', '\n', s)
    return s

# --- Roman Numerals ---

def to_roman(n: int) -> str:
    """Converts an integer to a Roman numeral."""
    if not 0 < n < 4000:
        raise ValueError("Input must be between 1 and 3999")
    
    val_map = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"),
        (1, "I")
    ]
    
    roman_num = []
    for val, numeral in val_map:
        count, n = divmod(n, val)
        roman_num.append(numeral * count)
    return "".join(roman_num)

def from_roman(s: str) -> int:
    """Converts a Roman numeral string to an integer."""
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    s = s.upper()
    for i in range(len(s)):
        # Subtraction rule (e.g., IV, IX)
        if i > 0 and roman_map[s[i]] > roman_map[s[i-1]]:
            result += roman_map[s[i]] - 2 * roman_map[s[i-1]]
        else:
            result += roman_map[s[i]]
    return result

# --- Internationalization (i18n) ---

def load_lexicon(lang: str, lexicon_file: str) -> Dict[str, str]:
    """
    Loads translations for a given language from a lexicon file.
    A simple Python implementation of the logic.
    """
    lexicon = {}
    lang_code = lang.split('.')[0].split('-')[0].split('_')[0]
    
    try:
        with open(lexicon_file, 'r', encoding='utf-8') as f:
            current_key = None
            for line in f:
                if not line.strip() or line.startswith('#'):
                    continue
                
                # A line starting with spaces defines a key
                if line.startswith('    '):
                    current_key = line.strip()
                # A line with a colon is a translation
                elif ':' in line and current_key:
                    code, value = line.split(':', 1)
                    if code.strip() == lang_code:
                        lexicon[current_key] = value.strip()
    except FileNotFoundError:
        print(f"Warning: Lexicon file not found at {lexicon_file}")
    
    return lexicon

# --- Serialization & Concurrency ---
T = TypeVar('T')

def read_or_create_value(
    fname: str,
    create_func: Callable[[], T],
    magic_word: Optional[str] = None,
    wait: bool = False
) -> T:
    """
    Atomically reads a pickled object from a file or creates it if it doesn't exist.
    Uses file locking to prevent race conditions.
    """
    filepath = Path(fname)
    
    if not filepath.exists():
        # If file doesn't exist, create it.
        try:
            with open(filepath, 'wb') as f:
                if HAS_FCNTL:
                    fcntl.flock(f, fcntl.LOCK_EX) # Exclusive lock
                
                value = create_func()
                if magic_word:
                    f.write(magic_word.encode('utf-8'))
                pickle.dump(value, f)
                
                if HAS_FCNTL:
                    fcntl.flock(f, fcntl.LOCK_UN) # Unlock
                return value
        except Exception as e:
            print(f"Error creating file {fname}: {e}")
            # In case of error, clean up and fall back to create_func
            rm_rf(str(filepath))
            return create_func()
            
    # If file exists, read it.
    with open(filepath, 'rb') as f:
        if HAS_FCNTL:
            lock_type = fcntl.LOCK_SH if not wait else fcntl.LOCK_EX
            fcntl.flock(f, lock_type)
        
        try:
            if magic_word:
                magic_read = f.read(len(magic_word))
                if magic_read != magic_word.encode('utf-8'):
                    raise ValueError("Magic word mismatch.")
            
            value = pickle.load(f)
            return value
        except (pickle.UnpicklingError, EOFError, ValueError) as e:
             # File is corrupt or invalid, handle by recreating
            print(f"File {fname} is corrupt ({e}), recreating...")
            f.close() # Close before rm_rf
            rm_rf(str(filepath))
            return read_or_create_value(fname, create_func, magic_word, wait)
        finally:
            if HAS_FCNTL:
                fcntl.flock(f, fcntl.LOCK_UN)

# --- Web-related Utilities ---

# URL encoding and decoding are directly replaced by urllib.parse functions
# OCaml: encode "a b+c" -> Python: quote_plus("a b+c") -> 'a+b%2Bc'
# OCaml: decode "a+b%2Bc" -> Python: unquote_plus("a+b%2Bc") -> 'a b+c'

def extract_param(name: str, params: List[str], stop_char: str = ';') -> str:
    """
    Extracts a parameter value from a list of 'key=value' strings. Case-insensitive key.
    """
    name_lower = name.lower()
    for param in params:
        if param.lower().startswith(name_lower):
            value = param[len(name):]
            if value.startswith('='): # Common format key=value
                value = value[1:]
            
            stop_index = value.find(stop_char)
            if stop_index != -1:
                return value[:stop_index]
            return value
    return ""
    
# --- Miscellaneous ---

def is_good_name(s: str) -> bool:
    """Checks if a string contains only alphanumeric characters and hyphens."""
    # A simple regex is cleaner and more explicit.
    return bool(re.match(r'^[a-zA-Z0-9-]+$', s))

def list_map_sort_uniq(fn: Callable[[Any], Any], data: Iterable) -> List:
    """
    Applies a function to each element of a list, then returns a sorted list
    of the unique results.
    """
    # This is the Pythonic one-liner for the complex OCaml implementation.
    return sorted(list(set(map(fn, data))))

def groupby(data: Iterable[T], key_func: Callable[[T], Any]) -> Dict[Any, List[T]]:
    """
    Groups elements of a list by a key function.
    Note: Python's `itertools.groupby` is more powerful but requires sorted input.
    This implementation mimics the OCaml version's behavior.
    """
    grouped: dict = {}
    for item in data:
        key = key_func(item)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(item)
    return grouped
    
def get_digest(s: str) -> str:
    """Returns the hex digest (hash) of a string."""
    return hashlib.md5(s.encode('utf-8')).hexdigest()

# Example of creating an empty person
def create_empty_person(what: str = "empty") -> Person:
    """Creates a default/empty Person object."""
    return Person(first_name=what, surname=what)