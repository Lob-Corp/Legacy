# GeneWeb to Application Type Converter

This module provides a conversion layer from parsed GeneWeb syntax (`GwSyntax`) to your application's strongly-typed models defined in `libraries/`.

## Overview

The conversion process:
1. **Parse** `.gw` files using `gw_parser` → produces `GwSyntax` objects
2. **Convert** `GwSyntax` to application types using `gw_converter` → produces `Person` and `Family` objects
3. **Use** the strongly-typed application models in your app

## Quick Start

```python
from script.gw_parser.parser import parse_gw_file
from script.gw_converter import convert_gw_file

# Parse and convert in one step
parsed_blocks = parse_gw_file("family.gw")
persons, families = convert_gw_file(parsed_blocks)

# Now you have typed Person and Family objects!
for person in persons:
    print(f"{person.first_name} {person.surname}")
```

## Type Mapping

### GwSyntax Types → Application Types

| GwSyntax Type | Application Type | Description |
|---------------|------------------|-------------|
| `FamilyGwSyntax` | `Family[int, Person[int, int, str], str]` | Family unit with marriage info |
| `NotesGwSyntax` | Merged into `Person.notes` | Person notes/biography |
| `RelationsGwSyntax` | Merged into `Person.non_native_parents_relation` | Adoptions, godparents, etc. |
| `PersonalEventsGwSyntax` | Merged into `Person.personal_events` | Life events beyond birth/death |
| `Somebody` references | `Person[int, int, str]` | Person references resolved |

### Key Features

- **Automatic person resolution**: `Somebody` references (both defined and undefined) are automatically resolved to actual `Person` objects
- **Data enrichment**: Notes, relations, and personal events from separate blocks are merged into the corresponding `Person` objects
- **Type safety**: Converts loosely-typed parsed data into strongly-typed application models
- **Index management**: Automatically assigns unique indices to persons and families

## Usage Examples

### Basic Conversion

```python
from script.gw_parser.parser import parse_gw_file
from script.gw_converter import convert_gw_file

# Parse .gw file
blocks = parse_gw_file("my_family.gw")

# Convert to app types
persons, families = convert_gw_file(blocks)

print(f"Loaded {len(persons)} persons, {len(families)} families")
```

### Step-by-Step Processing

```python
from script.gw_parser.parser import parse_gw_file
from script.gw_converter import GwConverter

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

### Looking Up Persons

```python
converter = GwConverter()
converter.convert_all(blocks)

# Find a specific person
person = converter.get_person_by_key("John", "Smith", 0)
if person:
    print(f"Found: {person.first_name} {person.surname}")
    print(f"Born: {person.birth_date} in {person.birth_place}")
```

### Accessing Enriched Data

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

### Working with Families

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

## Architecture

### GwConverter Class

The main converter class that manages the conversion process:

```python
class GwConverter:
    def __init__(self):
        # Tracking structures for persons, families, notes, etc.
        
    def convert(self, gw_syntax: GwSyntax) -> None:
        """Convert a single GwSyntax block"""
        
    def convert_all(self, gw_blocks: List[GwSyntax]) -> None:
        """Convert multiple blocks"""
        
    def get_enriched_persons(self) -> List[Person[int, int, str]]:
        """Get all persons with merged data"""
        
    def get_all_families(self) -> List[Family[...]]:
        """Get all families"""
```

### Conversion Flow

```
.gw file
   ↓
[Parser]
   ↓
GwSyntax blocks (FamilyGwSyntax, NotesGwSyntax, etc.)
   ↓
[Converter]
   ↓
Application types (Person, Family)
   ↓
Your application logic
```

## Type Parameters

The application types use generic type parameters:

- `Person[IdxT, PersonT, PersonDescriptorT]`
  - `IdxT`: Index type (typically `int`)
  - `PersonT`: Person reference type (typically `int` for cross-references)
  - `PersonDescriptorT`: String descriptor type (typically `str`)

- `Family[IdxT, PersonT, FamilyDescriptorT]`
  - `IdxT`: Index type (typically `int`)
  - `PersonT`: Person reference type (full `Person` objects after conversion)
  - `FamilyDescriptorT`: String descriptor type (typically `str`)

After conversion, you get:
- `Person[int, int, str]` - Persons with integer indices and string descriptors
- `Family[int, Person[int, int, str], str]` - Families with full Person references

## Error Handling

The converter raises exceptions for:
- **Undefined person references**: If a `SomebodyUndefined` cannot be resolved
- **Unknown GwSyntax types**: If an unrecognized syntax block is encountered

```python
try:
    converter.convert(block)
except ValueError as e:
    print(f"Cannot resolve person: {e}")
except TypeError as e:
    print(f"Unknown syntax type: {e}")
```

## See Also

- `script/gw_parser/` - GeneWeb file parser
- `libraries/person.py` - Person data type
- `libraries/family.py` - Family data types
- `libraries/events.py` - Event data types
- `examples/gw_converter_example.py` - More usage examples
