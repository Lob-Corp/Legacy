# Python GWC Implementation Guide

This document provides comprehensive documentation for the Python implementation of `gwc` (GeneWeb Compiler), including architecture, features, parser fixes, and dummy person handling.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Command-Line Options](#command-line-options)
4. [Parser Implementation](#parser-implementation)
5. [Dummy Person System](#dummy-person-system)
6. [Usage Examples](#usage-examples)
7. [Differences from OCaml](#differences-from-ocaml)
8. [Implementation Status](#implementation-status)

---

## Overview

The Python version of `gwc` is a complete rewrite that parses GeneWeb `.gw` files and converts them to application types for database storage. Key differences from the OCaml original:

- **No `.gwo` support**: Direct parsing, no intermediate object files
- **SQLite output**: Uses SQLite instead of custom `.gwb` binary format
- **Single-pass processing**: Parse and convert in one step
- **Modern Python**: Type hints, dataclasses, clear separation of concerns

### Project Structure

```
src/script/
├── gwc.py                    # Main entry point (CLI)
└── gw_parser/
    ├── parser.py             # Top-level file parser
    ├── block_parser.py       # Block-level parsing (fam, pevt, etc.)
    ├── person_parser.py      # Person/name parsing with inline definitions
    ├── event_parser.py       # Event parsing
    ├── date_parser.py        # Date parsing
    ├── gw_converter.py       # Convert GwSyntax → Application types
    ├── data_types.py         # Intermediate data structures
    └── utils.py              # Helper functions
```

---

## Architecture

### Processing Pipeline

```
┌─────────────┐
│  .gw file   │  (GeneWeb source format)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  gw_parser  │  Parse → GwSyntax blocks
└──────┬──────┘  (FamilyGwSyntax, PersonalEventsGwSyntax, etc.)
       │
       ▼
┌─────────────┐
│gw_converter │  Convert → Application types
└──────┬──────┘  (Person, Family with proper indexes)
       │
       ▼
┌─────────────┐
│   SQLite    │  (Future: database persistence)
└─────────────┘
```

### Key Components

#### 1. **Parser (`gw_parser/`)**

Converts `.gw` text files into structured `GwSyntax` objects:

- **`parser.py`**: Top-level file parser, identifies block types
- **`block_parser.py`**: Parses different block types (fam, pevt, notes, etc.)
- **`person_parser.py`**: Parses person references and inline definitions
- **`event_parser.py`**: Parses family and personal events
- **`date_parser.py`**: Parses dates in GeneWeb format

#### 2. **Converter (`gw_converter.py`)**

Converts parsed `GwSyntax` to application types:

- Assigns sequential indices to persons and families
- Resolves person references (creates dummies for undefined)
- Merges notes, events, and relations into person objects
- Tracks statistics (defined/dummy persons, families)

#### 3. **CLI (`gwc.py`)**

Command-line interface:

- Parses arguments
- Processes multiple input files
- Displays statistics and progress
- (Future) Outputs to SQLite database

---

## Command-Line Options

### Implemented Options

| Option | Description | Status |
|--------|-------------|--------|
| `-v` | Verbose mode - show detailed progress | ✅ Working |
| `-stats` | Display compilation statistics | ✅ Working |
| `-q` | Quiet mode - suppress output | ✅ Working |
| `-nofail` | Continue processing on errors | ✅ Working |
| `-o <file>` | Output database file | ✅ Recognized (output pending) |
| `-bnotes <mode>` | Base notes strategy (merge/erase/first/drop) | ✅ Implemented - merges base notes, wizard notes, page extensions |

### Partially Implemented

| Option | Description | Status |
|--------|-------------|--------|
| `-sep` | Separate persons per file | 🚧 Recognized, not implemented |
| `-sh <n>` | Shift person indices by n | 🚧 Recognized, not implemented |

### Not Yet Implemented

| Option | Description | Status |
|--------|-------------|--------|
| `-cg` | Compute consanguinity | ❌ Awaiting algorithm |
| `-ds <text>` | Default source field | ❌ Awaiting database |
| `-f` | Force overwrite | ❌ Awaiting database |
| `-nc` | No consistency check | ❌ Awaiting validation |
| `-nolock` | No database locking | ❌ Awaiting database |
| `-nopicture` | No picture associations | ❌ Awaiting database |
| `-particles <file>` | Custom particles file | ❌ Awaiting name processing |

### Removed Features

| Option | Description | Reason |
|--------|-------------|--------|
| `-c` | Compile-only mode | No `.gwo` support in Python |
| `-mem` | Memory optimization | Not applicable to Python |

### The `-bnotes` Option

The `-bnotes` option controls how database-level notes (base notes, wizard notes, page extensions) from multiple `.gw` files are merged during compilation. The option applies to the **next file** in the command line.

#### Modes

**`merge`** (default): Concatenates new content to existing content
```bash
gwc file1.gw file2.gw  # file2's notes appended to file1's
```

**`erase`**: Replaces all existing content with new content
```bash
gwc file1.gw -bnotes erase file2.gw  # file2's notes replace all previous
```

**`first`**: Keeps existing content if not empty, otherwise uses new content
```bash
gwc file1.gw -bnotes first file2.gw  # file2's notes only if no previous notes
```

**`drop`**: Ignores notes from the file entirely
```bash
gwc file1.gw -bnotes drop file2.gw  # file2's notes are discarded
```

#### Behavior

The option affects three types of data:
- **Base notes** (`notes-db` blocks): Merged per page name
- **Wizard notes** (`wizard-note` blocks): Merged per wizard ID
- **Page extensions** (`page-ext` blocks): Merged per page name

After each file is processed, the option resets to `merge` for subsequent files.

#### Example

```bash
# Start with base notes from file1
gwc file1.gw \
    -bnotes first file2.gw \    # Add file2's notes only if pages empty
    -bnotes merge file3.gw \    # Append file3's notes
    -bnotes drop file4.gw       # Ignore file4's notes
```

---

## Parser Implementation

### Key Parser Functions

#### `parse_parent()` (person_parser.py)
- Used for parsing parents in family lines
- Detects inline definitions vs. simple references
- Calls `build_person()` when inline data present

#### `parse_person_ref()` (person_parser.py)
- Used for references (witnesses, relations)
- Always returns `SomebodyUndefined` (just a key)

#### `build_person()` (person_parser.py)
- Parses all person attributes: aliases, titles, dates, places, events
- Returns complete `Person` object

### Occurrence Numbers

Occurrence numbers distinguish between people with the same name. Two formats are supported:

**Dot notation** (OCaml standard):
```gw
John.0 DOE    # First John Doe
John.1 DOE    # Second John Doe
```

**Bracket notation** (Python extension):
```gw
John[0] DOE
John[1] DOE
```

The occurrence number defaults to 0 if not specified. When parsing names, the parser uses `rfind('.')` to locate the last dot, then validates that what follows is a numeric occurrence.

### Child Sex Tokens

In family blocks, children can have their sex specified inline before their name:

**OCaml standard format** (without colon):
```gw
fam John DOE + Jane SMITH
beg
- h Bob    # homme (male)
- f Alice  # female
end
```

**Extended format** (with colon, for compatibility):
```gw
beg
- m: Bob   # male
- f: Alice # female
end
```

Both formats are accepted. If no sex token is present, the sex must be inferred or left as unknown.

### Database-Level Data

GeneWeb supports three types of database-level data that apply to the entire database rather than individual persons:

#### Base Notes (`notes-db` blocks)

Database-wide documentation pages. Each note has:
- A page name (empty string "" for main database note)
- Content (the note text)

```gw
notes-db
This is the main database note.
end notes

notes-db INTRO
This is the introduction page.
end notes
```

#### Wizard Notes (`wizard-note` blocks)

Notes specific to wizard (genealogy researcher) identifiers:

```gw
wizard-note john_researcher
Research notes for John's work.
end wizard-note
```

#### Page Extensions (`page-ext` blocks)

Extended page content for custom pages:

```gw
page-ext custom_page
Extended content for this page.
end page-ext
```

The converter stores these separately from person/family data and provides getter methods to retrieve them.

### Origin File Tracking

Each family records which source file it came from in the `origin_file` field. When compiling multiple `.gw` files, the converter automatically populates this field with the filename being processed.

**Purpose**: Track data provenance for debugging, auditing, and multi-file database management.

**Example**:
```bash
gwc file1.gw file2.gw file3.gw
```

All families from `file1.gw` will have `origin_file='file1.gw'`, families from `file2.gw` will have `origin_file='file2.gw'`, etc.

This allows you to:
- Identify which file introduced problematic data
- Filter or query families by source
- Understand the composition of merged databases

---

## Dummy Person System

### Overview

The dummy person system allows `.gw` files to reference persons before they're fully defined, matching OCaml gwc's behavior.

### How It Works

#### OCaml Approach
- Writes 'U' (Undefined) marker when person first referenced
- Writes 'D' (Defined) marker when full definition found
- Uses hash table for fast lookup
- Preserves index when upgrading U → D

#### Python Approach
- Tracks dummies in-memory via `set[Tuple[str, str, int]]`
- Creates placeholder `Person` objects with `Sex.UNKNOWN`
- Removes from set when full definition found
- Preserves index when upgrading (using `dataclasses.replace()`)

### Implementation

#### 1. Dummy Tracking

```python
class GwConverter:
    def __init__(self):
        self.person_by_key: Dict[Tuple[str, str, int], Person] = {}
        self.dummy_persons: set[Tuple[str, str, int]] = set()
        self.person_index_counter: int = 0
```

#### 2. Create Dummy Person

```python
def _create_dummy_person(self, key: Key) -> Person[int, int, str]:
    """Create minimal placeholder person for undefined reference."""
    person = Person(
        index=self.person_index_counter,
        first_name=key.pk_first_name,
        surname=key.pk_surname,
        occ=key.pk_occ,
        sex=Sex.UNKNOWN,  # Placeholder
        # All other fields empty/default
    )
    self.person_index_counter += 1
    return person
```

#### 3. Resolve Person References

```python
def resolve_somebody(self, somebody: Somebody) -> Person[int, int, str]:
    """Resolve a person reference, creating dummy if needed."""
    
    if isinstance(somebody, SomebodyDefined):
        # Full person definition
        key_tuple = (somebody.person.first_name, 
                     somebody.person.surname, 
                     somebody.person.occ)
        
        if key_tuple in self.dummy_persons:
            # Override dummy - preserve index!
            self.dummy_persons.remove(key_tuple)
            old_person = self.person_by_key[key_tuple]
            # Use replace() because Person is frozen
            new_person = replace(somebody.person, index=old_person.index)
            self.person_by_key[key_tuple] = new_person
            return new_person
        else:
            # New person - assign index
            new_person = replace(somebody.person, 
                                index=self.person_index_counter)
            self.person_index_counter += 1
            self.person_by_key[key_tuple] = new_person
            return new_person
    
    elif isinstance(somebody, SomebodyUndefined):
        # Reference to person
        key_tuple = (somebody.key.pk_first_name,
                     somebody.key.pk_surname,
                     somebody.key.pk_occ)
        
        if key_tuple in self.person_by_key:
            # Already exists
            return self.person_by_key[key_tuple]
        else:
            # Create dummy
            dummy = self._create_dummy_person(somebody.key)
            self.person_by_key[key_tuple] = dummy
            self.dummy_persons.add(key_tuple)
            return dummy
```

#### 4. Upgrade Dummies with Events

When personal events are added to a dummy, mark it as defined:

```python
def convert_personal_events(self, gw_events: PersonalEventsGwSyntax):
    """Store personal events for a person."""
    person = self.resolve_somebody(gw_events.person)
    key_tuple = (person.first_name, person.surname, person.occ)
    
    # Store events
    self.personal_events[key_tuple] = converted_events
    
    # If this person was a dummy, mark as defined now
    if key_tuple in self.dummy_persons:
        self.dummy_persons.remove(key_tuple)
```

### Processing Examples

#### Example 1: Forward Reference

```gw
fam John DOE + Jane SMITH
wit: Bob WITNESS

Bob WITNESS
birt: 1950
```

**Processing**:
1. Parse family → `John DOE` (inline def) → Person #0
2. Parse family → `Jane SMITH` (inline def) → Person #1  
3. Parse witness → `Bob WITNESS` (undefined) → **Dummy #2** ✓
4. Parse Bob's block → Override dummy #2 with full data ✓
5. Remove from dummy_persons set ✓

**Result**: 3 persons, all fully defined, Bob keeps index=2

#### Example 2: Never Defined

```gw
fam John DOE + Jane SMITH
wit: Bob WITNESS
```

**Processing**:
1. `John DOE` → Person #0
2. `Jane SMITH` → Person #1
3. `Bob WITNESS` → **Dummy #2** ⚠️
4. End of file → Bob stays as dummy ⚠️

**Result**: 
- 3 total persons
- 2 fully defined
- 1 dummy (warning shown)

### Statistics

```python
stats = converter.get_statistics()
# Returns:
{
    'total_persons': len(self.person_by_key),
    'defined_persons': len(self.person_by_key) - len(self.dummy_persons),
    'dummy_persons': len(self.dummy_persons),
    'families': len(self.families)
}
```

### Comparison Table

| Feature | OCaml gwc | Python gwc |
|---------|-----------|------------|
| **Undefined marker** | Write 'U' byte to file | Add to `dummy_persons` set |
| **Defined marker** | Write 'D' byte (overwrites 'U') | Remove from `dummy_persons` |
| **Index preservation** | File position stays same | Store and reuse index |
| **Lookup** | `Hashtbl.find_all g_names` | Dict `person_by_key` |
| **Detection** | Read 'U'/'D' marker from file | Check if in `dummy_persons` |
| **Statistics** | Count 'U' markers in file | `len(dummy_persons)` |

---

## Usage Examples

### Basic Usage

```bash
# Process a single file
python -m src.script.gwc mydata.gw -o mybase.sqlite

# Or use vpython alias (if configured)
vpython src/script/gwc.py mydata.gw -o mybase.sqlite
```

### Verbose Mode

```bash
vpython src/script/gwc.py mydata.gw -v

# Output:
# Processing 1 file(s)...
#
# [1/1] Processing mydata.gw...
#   Parsing mydata.gw...
#   Parsed 15 blocks
#   Converting to application types...
#   Converted 45 persons, 12 families
#   Warning: 2 undefined person(s)
#
# ==================================================
# Parsing Statistics:
# ==================================================
# Total persons: 45
# Total families: 12
# Files processed: 1
```

### Multiple Files

```bash
vpython src/script/gwc.py file1.gw file2.gw file3.gw -o combined.sqlite -v
```

### Continue on Errors

```bash
vpython src/script/gwc.py -nofail -v incomplete.gw broken.gw -o output.sqlite
```

### Quiet Mode

```bash
vpython src/script/gwc.py -q mydata.gw -o mybase.sqlite
```

---

## Differences from OCaml

### Architectural Differences

| Aspect | OCaml gwc | Python gwc |
|--------|-----------|------------|
| **Compilation model** | Two-phase (`.gw` → `.gwo` → `.gwb`) | Single-phase (`.gw` → types → SQLite) |
| **Intermediate files** | Uses `.gwo` object files | No intermediate files |
| **Output format** | Custom `.gwb` binary | SQLite database |
| **Type system** | OCaml's strong typing | Python type hints + dataclasses |
| **Memory model** | Manual memory management | Automatic garbage collection |

### Parser Differences

| Feature | OCaml | Python |
|---------|-------|--------|
| **Inline parent parsing** | `parse_parent` checks for `+` | Fixed: `parse_parent()` added |
| **Person building** | `set_infos` function | `build_person()` function |
| **Name lookup** | Hash with `crush_lower` | Dict by tuple (can enhance) |
| **Error handling** | Exceptions with line numbers | Exceptions with context |

### Dummy Person Handling

| Feature | OCaml | Python |
|---------|-------|--------|
| **Storage** | 'U'/'D' markers in `.g_per` file | In-memory `set` |
| **Persistence** | File-based, across runs | In-memory, per-run |
| **Lookup** | File position + marker read | Set membership check |
| **Override** | Overwrite 'U' with 'D' at same position | Remove from set, keep index |

### Not Yet Ported

- **Name normalization**: OCaml's `Name.crush_lower` for fuzzy matching
- **Consanguinity**: Relationship computation algorithm
- **Particles**: Name particle handling (de, von, etc.)
- **Picture associations**: Linking photos to persons
- **Database locking**: Multi-user access control

---

## Implementation Status

### Current State (October 2025)

#### ✅ Fully Working
- Parse `.gw` files with all block types
- Handle inline person definitions in family lines
- Create dummy persons for undefined references
- Override dummies when definitions found
- Assign proper sexes to parents (Male/Female)
- Parse birth dates, places, and other inline attributes
- Track statistics (persons, families, dummies)
- Verbose and quiet modes
- Multiple file processing
- Error handling with `-nofail`

#### 🚧 In Progress
- SQLite database output (structure defined, writing pending)
- Base notes merging strategies
- Person index shifting

#### ❌ Not Started
- Consanguinity computation
- Consistency checking
- Picture associations
- Custom particles files
- Database locking

### Test Results

**Test file**: `release/bases/baseaa.gw`
- **Input**: 5 families with inline parent definitions
- **Output**: 10 persons correctly parsed
- **No warnings**: All persons fully defined
- **Sexes**: Correctly assigned (5 male, 5 female)
- **Dates**: Birth dates correctly parsed from inline definitions

### Known Limitations

1. **No name fuzzy matching**: Duplicate detection less robust than OCaml
2. **No cross-file dummy persistence**: Dummies don't survive between runs
3. **Limited validation**: No consistency checks yet
4. **No database output**: SQLite writing pending

---

## Converter API Reference

This section describes the `GwConverter` class API for programmatic use.

### Quick Start

```python
from src.script.gw_parser import parse_gw_file, GwConverter

# Parse and convert in one step
blocks = parse_gw_file("family.gw")
converter = GwConverter()
converter.convert_all(blocks)

persons = converter.get_all_persons()
families = converter.get_all_families()

# Now you have typed Person and Family objects!
for person in persons:
    print(f"{person.first_name} {person.surname}")
```

### Type Mapping

| GwSyntax Type | Application Type | Description |
|---------------|------------------|-------------|
| `FamilyGwSyntax` | `Family[int, Person[int, int, str], str]` | Family with marriage info |
| `NotesGwSyntax` | Merged into `Person.notes` | Person biography |
| `RelationsGwSyntax` | Merged into `Person.non_native_parents_relation` | Adoptions, godparents |
| `PersonalEventsGwSyntax` | Merged into `Person.personal_events` | Life events |
| `Somebody` (Defined/Undefined) | `Person[int, int, str]` | Resolved persons |

### GwConverter Class Methods

#### Conversion Methods

```python
def convert(self, gw_syntax: GwSyntax) -> None:
    """Convert a single GwSyntax block.
    
    Dispatches to appropriate handler based on block type.
    """

def convert_all(self, gw_blocks: List[GwSyntax]) -> None:
    """Convert multiple GwSyntax blocks in sequence."""

def convert_family(self, gw_family: FamilyGwSyntax) -> Tuple[Family, List[Person]]:
    """Convert a family block, resolving parents and witnesses."""

def convert_notes(self, gw_notes: NotesGwSyntax) -> None:
    """Store notes for a person (merged later)."""

def convert_relations(self, gw_relations: RelationsGwSyntax) -> None:
    """Store relations for a person (merged later)."""

def convert_personal_events(self, gw_events: PersonalEventsGwSyntax) -> None:
    """Store personal events for a person (merged later).
    
    Also removes person from dummy_persons set if they were a dummy.
    """

def convert_base_notes(self, gw_base_notes: BaseNotesGwSyntax) -> None:
    """Store base notes (database-wide notes)."""

def convert_wizard_notes(self, gw_wizard_notes: WizardNotesGwSyntax) -> None:
    """Store wizard notes."""

def convert_page_ext(self, gw_page_ext: PageExtGwSyntax) -> None:
    """Store page extension content."""
```

#### Retrieval Methods

```python
def get_all_persons(self) -> List[Person[int, int, str]]:
    """Get all registered persons (including dummies)."""

def get_enriched_persons(self) -> List[Person[int, int, str]]:
    """Get all persons with notes, relations, and events merged in."""

def get_all_families(self) -> List[Family[int, Person[int, int, str], str]]:
    """Get all registered families."""

def get_person_by_key(self, first_name: str, surname: str, occ: int = 0) -> Optional[Person]:
    """Look up a person by their key (first name, surname, occurrence)."""

def get_dummy_persons(self) -> List[Person[int, int, str]]:
    """Get all persons that remain as dummies (undefined references)."""

def get_base_notes(self) -> List[Tuple[str, str]]:
    """Get all database-wide notes.
    
    Returns list of (page, content) tuples.
    """

def get_wizard_notes(self) -> Dict[str, str]:
    """Get all wizard notes.
    
    Returns dictionary mapping wizard_id to content.
    """

def get_page_extensions(self) -> Dict[str, str]:
    """Get all page extensions.
    
    Returns dictionary mapping page_name to content.
    """

def get_statistics(self) -> Dict[str, int]:
    """Get conversion statistics.
    
    Returns:
        {
            'total_persons': int,      # All persons (defined + dummy)
            'defined_persons': int,    # Fully defined persons
            'dummy_persons': int,      # Undefined references
            'families': int,           # Total families
            'base_notes': int,         # Database-wide notes
            'wizard_notes': int,       # Wizard-specific notes
            'page_extensions': int     # Page extensions
        }
    """
```

#### Person Resolution

```python
def resolve_somebody(self, somebody: Somebody) -> Person[int, int, str]:
    """Resolve a Somebody reference to a Person object.
    
    Handles three scenarios:
    1. SomebodyDefined + exists as dummy → Override dummy, preserve index
    2. SomebodyDefined + new → Create new person with new index
    3. SomebodyUndefined + exists → Return existing person
    4. SomebodyUndefined + new → Create dummy person
    
    Args:
        somebody: SomebodyDefined (full person) or SomebodyUndefined (reference)
    
    Returns:
        Resolved Person object
    """
```

### Usage Examples

#### Basic Conversion

```python
from src.script.gw_parser import parse_gw_file, convert_gw_file

# One-liner conversion
blocks = parse_gw_file("my_family.gw")
persons, families = convert_gw_file(blocks)

print(f"Loaded {len(persons)} persons, {len(families)} families")
```

#### Step-by-Step Processing

```python
from src.script.gw_parser import parse_gw_file, GwConverter

blocks = parse_gw_file("my_family.gw")
converter = GwConverter()

# Process blocks individually
for block in blocks:
    converter.convert(block)
    # Can add custom logic here (validation, logging, etc.)

# Get results
persons = converter.get_enriched_persons()
families = converter.get_all_families()
```

#### Check for Dummies

```python
converter = GwConverter()
converter.convert_all(blocks)

# Get statistics
stats = converter.get_statistics()
print(f"Total persons: {stats['total_persons']}")
print(f"Defined: {stats['defined_persons']}")
print(f"Dummies: {stats['dummy_persons']}")

# Get list of undefined persons
if stats['dummy_persons'] > 0:
    dummies = converter.get_dummy_persons()
    print("\nUndefined persons:")
    for dummy in dummies:
        print(f"  - {dummy.first_name} {dummy.surname}")
```

#### Lookup Persons

```python
converter = GwConverter()
converter.convert_all(blocks)

# Find a specific person
person = converter.get_person_by_key("John", "Smith", 0)
if person:
    print(f"Found: {person.first_name} {person.surname}")
    print(f"Born: {person.birth_date} in {person.birth_place}")
    print(f"Index: {person.index}")
```

#### Access Enriched Data

```python
persons = converter.get_enriched_persons()

for person in persons:
    # Base person data
    print(f"{person.first_name} {person.surname}")
    
    # Enriched with notes (from NotesGwSyntax blocks)
    if person.notes:
        print(f"  Notes: {person.notes}")
    
    # Enriched with relations (from RelationsGwSyntax blocks)
    for relation in person.non_native_parents_relation:
        print(f"  Relation: {relation.type.value}")
        if relation.father:
            print(f"    Father: {relation.father.first_name}")
    
    # Enriched with personal events (from PersonalEventsGwSyntax blocks)
    for event in person.personal_events:
        print(f"  Event: {event.name.value} on {event.date}")
```

#### Work with Families

```python
families = converter.get_all_families()

for family in families:
    print(f"Family {family.index}")
    print(f"  Marriage: {family.marriage_date} at {family.marriage_place}")
    print(f"  Status: {family.relation_kind.value}")
    print(f"  Divorce: {type(family.divorce_status).__name__}")
    
    # Witnesses
    for witness in family.witnesses:
        print(f"  Witness: {witness.first_name} {witness.surname}")
    
    # Family events
    for event in family.family_events:
        print(f"  Event: {event.name.value}")
```

### Type Parameters

The application types use generic type parameters for flexibility:

**Person Type**: `Person[IdxT, PersonT, PersonDescriptorT]`
- `IdxT`: Index type (typically `int`)
- `PersonT`: Person reference type (typically `int` for DB foreign keys)
- `PersonDescriptorT`: String descriptor type (typically `str`)

**Family Type**: `Family[IdxT, PersonT, FamilyDescriptorT]`
- `IdxT`: Index type (typically `int`)
- `PersonT`: Person reference type (full `Person` objects after conversion)
- `FamilyDescriptorT`: String descriptor type (typically `str`)

After conversion, you get:
- `Person[int, int, str]` - Persons with integer indices and string descriptors
- `Family[int, Person[int, int, str], str]` - Families with full Person references

### Error Handling

The converter may raise exceptions:

```python
try:
    converter.convert(block)
except ValueError as e:
    # Person resolution failed
    print(f"Cannot resolve person: {e}")
except TypeError as e:
    # Unknown syntax block type
    print(f"Unknown syntax type: {e}")
```

**Note**: With the dummy person system, `ValueError` for undefined persons is rare (only if dummy creation fails).

---

## Future Enhancements

### Short Term
1. Implement SQLite database output
2. Add name normalization for better duplicate detection
3. Implement `-sep` (separate persons per file)
4. Implement `-sh` (index shifting)

### Medium Term
1. Port consanguinity computation algorithm
2. Add consistency checking (`-nc` flag)
3. Implement base notes merging
4. Add comprehensive test suite

### Long Term
1. Optimize for large genealogy files (100k+ persons)
2. Add incremental updates (don't reprocess unchanged files)
3. Implement database locking for multi-user
4. Add picture association logic

---

## Contributing

When modifying the parser or converter:

1. **Test with real data**: Use actual GeneWeb files, not just synthetic tests
2. **Check dummy handling**: Verify undefined references work correctly
3. **Preserve indices**: Ensure person/family indices remain stable
4. **Update statistics**: Keep tracking accurate
5. **Document changes**: Update this file with new features

### Common Pitfalls

- **Frozen dataclasses**: Use `replace()`, not direct assignment
- **Index assignment**: Assign before first registration, not after
- **Dummy detection**: Check `dummy_persons` set, not person attributes
- **Token consumption**: Ensure parser functions consume correct tokens

---

## References

- **OCaml source**: `legacy/bin/gwc/gwcomp.ml`, `db1link.ml`
- **GeneWeb format**: See `.gw` files after exporting an existing database
- **Parser implementation**: `src/script/gw_parser/`
- **Converter implementation**: `src/script/gw_parser/gw_converter.py`
- **CLI implementation**: `src/script/gwc.py`

