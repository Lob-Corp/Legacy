# GeneWeb Parser

A Python package for parsing GeneWeb genealogical data files (.gw format).

## Structure

The parser has been refactored into coherent, maintainable modules:

### Module Organization

```
gw_parser/
├── __init__.py          # Package interface and exports
├── data_types.py        # Core data structures and type definitions
├── utils.py             # Utility functions (tokenization, field extraction)
├── date_parser.py       # Date parsing with precision markers and calendars
├── person_parser.py     # Person and name parsing
├── event_parser.py      # Family and personal event parsing
├── stream.py            # Line stream with lookahead/pushback
├── block_parser.py      # Block-level parsers (family, notes, relations, etc.)
└── parser.py            # Main entry point (parse_gw_file)
```

### Module Descriptions

#### `data_types.py`
- **Purpose**: Defines core data structures
- **Contents**: 
  - `Key`, `Somebody`, `SomebodyUndefined`, `SomebodyDefined`
  - `GwSyntax` base class and block variants (`FamilyGwSyntax`, `NotesGwSyntax`, etc.)
  - Global flags (`gwplus_mode`, `no_fail_mode`, `create_all_keys`)

#### `utils.py`
- **Purpose**: Low-level text processing utilities
- **Functions**:
  - `fields()` - Tokenize line with underscore/escape handling
  - `copy_decode()` - Decode escaped characters and underscores
  - `get_field()` - Extract labeled fields from tokens
  - `cut_space()` - Trim whitespace

#### `date_parser.py`
- **Purpose**: Parse dates in GeneWeb format
- **Features**:
  - Precision markers: `~` (about), `?` (maybe), `<` (before), `>` (after)
  - Date formats: year, month/year, day/month/year
  - OrYear (`|`) and YearInt (`..`) ranges
  - Calendar suffixes: G (Gregorian), J (Julian), F (French), H (Hebrew)
  - Text dates: `0(text description)`

#### `person_parser.py`
- **Purpose**: Parse person references and full person definitions
- **Functions**:
  - `parse_person_ref()` - Parse person references
  - `parse_first_name()` - Extract first name with occurrence number
  - `parse_name()` - Extract surname
  - `build_person()` - Build complete Person object from tokens
  - Helper functions for aliases, titles, access rights, etc.

#### `event_parser.py`
- **Purpose**: Parse family and personal events
- **Features**:
  - Event name mapping (40+ event types)
  - Witness parsing with kinds (godparent, officer, informant, etc.)
  - Event notes parsing
  - Family events (`#marr`, `#div`, etc.)
  - Personal events (`#birt`, `#bapt`, `#deat`, etc.)

#### `stream.py`
- **Purpose**: Line stream abstraction
- **Features**:
  - `peek()` - Look at next line without consuming
  - `pop()` - Consume next line
  - `push_back()` - Push line back onto stream
  - Filters empty lines automatically

#### `block_parser.py`
- **Purpose**: Parse different block types
- **Functions**:
  - `parse_family_block()` - Family blocks with children, events, witnesses
  - `parse_notes_block()` - Person notes
  - `parse_relations_block()` - Adoption, godparent, foster relations
  - `parse_personal_events_block()` - Personal events
  - Special blocks: `notes-db`, `wizard-note`, `page-ext`

#### `parser.py`
- **Purpose**: Main entry point
- **Function**: `parse_gw_file(path, encoding, no_fail)` 
- **Features**:
  - Encoding directive detection (`encoding:` header)
  - `gwplus` directive support
  - Error recovery mode (`no_fail=True`)
  - Line number tracking for errors

## Usage

```python
from script.gw_parser import parse_gw_file, FamilyGwSyntax

# Parse a .gw file
blocks = parse_gw_file('data.gw')

# Filter for family blocks
families = [b for b in blocks if isinstance(b, FamilyGwSyntax)]

# Error recovery mode
blocks = parse_gw_file('data.gw', no_fail=True)
```

## Testing

All tests pass after refactoring:
```bash
pytest tests/import_tests/gw/test_gw_import.py -v
```

30 tests covering:
- Family blocks (8 variants)
- Relations (6 types)
- Personal events (5 cases)
- Notes (3 types)
- Directives (encoding, gwplus)
- Error recovery

## Benefits of Refactoring

1. **Modularity**: Each module has a single, clear responsibility
2. **Maintainability**: Easier to locate and modify specific functionality
3. **Testability**: Individual modules can be tested in isolation
4. **Readability**: Smaller files are easier to understand
5. **Reusability**: Modules can be imported independently
6. **Documentation**: Clear module-level documentation

## Migration from gwcomp.py

The old monolithic `gwcomp.py` (1600+ lines) has been split into 9 focused modules (~100-400 lines each). The public API remains identical - just update imports:

```python
# Old import
from script.gwcomp import parse_gw_file, FamilyGwSyntax

# New import
from script.gw_parser import parse_gw_file, FamilyGwSyntax
```

All functionality has been preserved and all tests pass.
