# GeneWeb Converter with Dummy Person Support

## Implementation Complete

The `gw_converter.py` now implements OCaml gwc's approach for handling undefined person references.

## Key Features

### 1. **Dummy Person Creation** (OCaml's 'U' Marker Equivalent)

When an undefined person reference is encountered:
```python
# OCaml: output_char gen.g_per 'U'
# Python: Add to dummy_persons set
dummy = self._create_dummy_person(key)
self.person_by_key[key_tuple] = dummy
self.dummy_persons.add(key_tuple)
```

### 2. **Person Override** (OCaml's 'D' Marker Equivalent)

When a full definition is found for a previously undefined person:
```python
# OCaml: output_char gen.g_per 'D' (overwrites 'U')
# Python: Remove from dummy_persons, preserve index
if key_tuple in self.dummy_persons:
    self.dummy_persons.remove(key_tuple)
    old_person = self.person_by_key[key_tuple]
    somebody.person.index = old_person.index  # Preserve!
```

### 3. **Hash Table Lookup** (Like OCaml's g_names)

```python
# OCaml: Hashtbl.find_all gen.g_names key
# Python: Dict lookup with key_tuple
self.person_by_key: Dict[Tuple[str, str, int], Person]
```

## Processing Flow

### Example: Witness Defined After Family

```gw
fam John DOE + Jane SMITH
wit: Bob WITNESS

Bob WITNESS
birt: 1950
```

**Processing Steps:**

1. **Family Block**
   ```
   John DOE    → SomebodyDefined → Create person #0
   Jane SMITH  → SomebodyDefined → Create person #1
   Bob WITNESS → SomebodyUndefined → Create DUMMY #2 ✓
   ```

2. **Bob's Definition Block**
   ```
   Bob WITNESS → SomebodyDefined → OVERRIDE dummy #2 ✓
                                    (keeps index=2)
   ```

**Result:**
- 3 persons total
- 3 defined (0 dummies remaining)
- Bob's index stays as #2

### Example: Person Never Defined

```gw
fam John DOE + Jane SMITH
wit: Bob WITNESS

(Bob is never defined)
```

**Processing:**

1. **Family Block**
   ```
   John DOE    → person #0
   Jane SMITH  → person #1  
   Bob WITNESS → DUMMY #2 ⚠️
   ```

2. **End of File**
   ```
   Bob remains as dummy
   ```

**Statistics:**
```python
stats = converter.get_statistics()
# {
#   'total_persons': 3,
#   'defined_persons': 2,
#   'dummy_persons': 1,  # Bob!
#   'families': 1
# }
```

## Comparison with OCaml

| Feature | OCaml gwc | Python gwc (now) |
|---------|-----------|------------------|
| **Undefined reference** | Write 'U' marker to file | Add to `dummy_persons` set |
| **Full definition** | Write 'D' marker (overwrites 'U') | Remove from `dummy_persons` |
| **Index preservation** | File position stays same | Store and reuse index |
| **Lookup** | `Hashtbl.find_all g_names` | Dict `person_by_key` |
| **Detection** | Read 'U'/'D' marker | Check if in `dummy_persons` |
| **Statistics** | Count 'U' markers | `len(dummy_persons)` |

## API Usage

### Get Dummy Persons

```python
converter = GwConverter()
converter.convert_all(blocks)

# Get list of undefined persons
dummies = converter.get_dummy_persons()
for dummy in dummies:
    print(f"Warning: Undefined - {dummy.first_name} {dummy.surname}")
```

### Get Statistics

```python
stats = converter.get_statistics()
print(f"Total persons: {stats['total_persons']}")
print(f"Fully defined: {stats['defined_persons']}")
print(f"Dummies: {stats['dummy_persons']}")
print(f"Families: {stats['families']}")
```

### Check if Person is Dummy

```python
key_tuple = (person.first_name, person.surname, person.occ)
is_dummy = key_tuple in converter.dummy_persons
```

## Integration with gwc.py

The `gwc.py` script now automatically shows warnings:

```bash
$ python -m src.script.gwc myfile.gw -v

Processing 1 file(s)...

[1/1] Processing myfile.gw...
  Parsing myfile.gw...
  Parsed 10 blocks
  Converting to application types...
  Converted 25 persons, 8 families
  Warning: 3 undefined person(s)  ← Automatic warning!

==================================================
Compilation Statistics:
==================================================
Total persons: 25
Fully defined: 22
Dummies: 3
Families: 8
==================================================
```

## Dummy Person Structure

A dummy person has:
- ✅ `first_name`, `surname`, `occ` (from key)
- ✅ `index` (assigned)
- ✅ `sex = UNKNOWN`
- ❌ All other fields empty/None

```python
Person(
    index=42,
    first_name="Unknown",
    surname="Person",
    occ=0,
    sex=Sex.UNKNOWN,
    # ... all other fields empty ...
)
```

## Benefits

1. **No blocking errors**: Files can be processed even with missing definitions
2. **Forward references**: Define person after referencing them
3. **Flexible file structure**: No required ordering
4. **Clear warnings**: Identify which persons need definitions
5. **Index stability**: References work correctly even for dummies
6. **OCaml compatibility**: Matches original behavior

## Future: Database Persistence

When implementing SQLite storage, add a flag:

```sql
CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    surname TEXT,
    occ INTEGER,
    is_dummy BOOLEAN,  -- TRUE if undefined reference
    ...
);
```

This allows:
- Saving dummy state to database
- Loading and checking dummy status
- Updating dummies when definitions found later
- Querying for undefined persons

## Testing

The converter now handles:
- ✅ Undefined witnesses in families
- ✅ Undefined parents in relations
- ✅ Undefined persons in events
- ✅ Person defined after first reference
- ✅ Multiple references to same undefined person
- ✅ Override preserves index
- ✅ Statistics tracking
- ✅ Warnings in verbose mode
