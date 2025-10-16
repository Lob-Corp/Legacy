# Python GWC Implementation

This document describes the Python implementation of `gwc` (GeneWeb Compiler).

## Overview

The Python version of `gwc` differs from the OCaml original in several key ways:

1. **No `.gwo` support**: Intermediate object files are not used - parsing is direct
2. **SQLite output**: Uses SQLite instead of the custom `.gwb` binary format
3. **Single-pass processing**: Files are parsed and converted in one step

## Current Implementation Status

### ✅ Implemented Features

- **File parsing**: Parse `.gw` files using `gw_parser`
- **Type conversion**: Convert GwSyntax to application types using `gw_converter`
- **Multiple files**: Process multiple input files in sequence
- **Verbose mode**: `-v` flag for detailed progress output
- **Statistics**: `-stats` flag to show compilation statistics
- **Error handling**: `-nofail` to continue on errors
- **Quiet mode**: `-q` to suppress output

### 🚧 Partially Implemented

These features are recognized but not yet fully functional:

- **`-bnotes`**: Base notes merging strategy (recognized but merge logic not implemented)
- **`-sep`**: Separate persons mode (recognized but not implemented)
- **`-sh`**: Shift person numbers (recognized but not implemented)

### ❌ Not Yet Implemented

Features that require additional infrastructure:

- **`-o`**: SQLite database output (awaiting database module)
- **`-cg`**: Consanguinity computation (awaiting algorithm implementation)
- **`-ds`**: Default source field (awaiting database module)
- **`-f`**: Force overwrite (awaiting database module)
- **`-mem`**: Memory optimization (not applicable to Python version)
- **`-nc`**: No consistency check (awaiting validation module)
- **`-nolock`**: No database locking (awaiting database module)
- **`-nopicture`**: No picture associations (awaiting database module)
- **`-particles`**: Custom particles file (awaiting name processing module)

### 🚫 Removed Features

Features that have been intentionally removed in the Python version:

- **`-c`**: Compile-only mode (no `.gwo` intermediate files)
- **`.gwo` files**: No support for pre-compiled object files
- **Two-phase compilation**: Direct parsing only

## Usage

### Basic Usage

```bash
python -m src.script.gwc mydata.gw -o mybase.sqlite
```

### Multiple Files

Process multiple `.gw` files into a single database:

```bash
python -m src.script.gwc file1.gw file2.gw file3.gw -o combined.sqlite
```

### With Verbose Output

```bash
python -m src.script.gwc -v mydata.gw -o mybase.sqlite
```

### With Statistics

```bash
python -m src.script.gwc -stats mydata.gw -o mybase.sqlite
```

### Continue on Errors

```bash
python -m src.script.gwc -nofail -v incomplete.gw -o mybase.sqlite
```

## Architecture

```
┌─────────────┐
│   .gw file  │
└──────┬──────┘
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│  gw_parser  │   │  gw_parser  │
└──────┬──────┘   └──────┬──────┘
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│  GwSyntax   │   │  GwSyntax   │
└──────┬──────┘   └──────┬──────┘
       │                 │
       └────────┬────────┘
                │
                ▼
         ┌─────────────┐
         │gw_converter │
         └──────┬──────┘
                │
                ▼
    ┌───────────────────────┐
    │  Application Types    │
    │  - Person[]           │
    │  - Family[]           │
    └───────────┬───────────┘
                │
                ▼
         ┌─────────────┐
         │   SQLite    │  ← TODO
         │  Database   │
         └─────────────┘
```

## Implementation Details

### File Processing Loop

```python
for filename, separate, bnotes_mode, shift in input_files:
    # 1. Parse .gw file
    gw_syntax_blocks = parse_gw_file(content, filename)
    
    # 2. Convert to application types
    persons, families = convert_gw_file(gw_syntax_blocks)
    
    # 3. Accumulate results
    all_persons.extend(persons)
    all_families.extend(families)
```

### Error Handling

```python
try:
    # Process file
    ...
except Exception as e:
    if args.nofail:
        # Log error and continue
        continue
    else:
        # Stop processing
        sys.exit(1)
```

### Statistics Output

```
==================================================
Compilation Statistics:
==================================================
Total persons: 1234
Total families: 567
Files processed: 3
==================================================
```

## Differences from OCaml Version

| Feature | OCaml `gwc` | Python `gwc` |
|---------|-------------|--------------|
| Input files | `.gw` or `.gwo` | `.gw` only |
| Intermediate format | `.gwo` files | None (direct parsing) |
| Database format | `.gwb` binary | SQLite database |
| Memory mode | `-mem` flag | Not needed (Python GC) |
| Processing | Two-phase (compile→link) | Single-phase (parse→convert) |
| Locking | File-based | Database-based |

## Next Steps

To complete the Python `gwc` implementation:

1. **Database Module**: Implement SQLite schema and insertion logic
2. **Consanguinity**: Port consanguinity calculation algorithm
3. **Name Processing**: Implement particle handling
4. **Validation**: Add consistency checking
5. **Shift/Separate**: Implement person ID shifting and separation
6. **Notes Merging**: Implement base notes merging strategies

## Example Workflow

```bash
# Step 1: Parse and convert
python -m src.script.gwc -v -stats mydata.gw -o mybase.sqlite

# Output:
# Processing 1 file(s)...
#
# [1/1] Processing mydata.gw...
#   Parsing mydata.gw...
#   Parsed 150 blocks
#   Converting to application types...
#   Converted 234 persons, 89 families
#
# ==================================================
# Compilation Statistics:
# ==================================================
# Total persons: 234
# Total families: 89
# Files processed: 1
# ==================================================
#
# Database output: mybase.sqlite
# Note: SQLite database saving not yet implemented
# Data has been parsed and converted to application types
#
# Processing complete!
```

## Testing

To test the current implementation:

```bash
# Test parsing only (no database)
python -m src.script.gwc -v test_fam.gw -o test.sqlite

# Test with multiple files
python -m src.script.gwc -v file1.gw file2.gw -o combined.sqlite

# Test error handling
python -m src.script.gwc -nofail -v bad_data.gw -o test.sqlite
```

## Code Structure

```
src/script/
├── gwc.py              # Main compiler logic (this file)
├── gw_parser/          # Parser module
│   ├── __init__.py
│   ├── parser.py       # Main parsing logic
│   ├── data_types.py   # GwSyntax types
│   └── ...
└── gw_converter.py     # GwSyntax → App types converter
```

## API

### Main Function

```python
def main() -> int:
    """
    Main entry point for gwc compiler.
    
    Returns:
        0 on success, non-zero on error
    """
```

### Helper Functions

```python
def appendFileData(
    files: list[tuple[str, bool, str, int]],
    x: str,
    separate: bool,
    bnotes: str,
    shift: int
) -> None:
    """Validate and append file data to the list."""
```
