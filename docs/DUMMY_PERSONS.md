# Dummy Person Implementation Summary

## What Was Changed

I've updated the `gw_converter.py` to implement OCaml gwc's behavior for handling undefined person references.

## Key Changes

### 1. Added Dummy Person Tracking

```python
class GwConverter:
    def __init__(self):
        ...
        # Track which persons are dummies (undefined references)
        self.dummy_persons: set[Tuple[str, str, int]] = set()
```

### 2. Created `_create_dummy_person()` Method

This method creates a minimal placeholder person when an undefined reference is encountered:

```python
def _create_dummy_person(self, key: Key) -> Person[int, int, str]:
    """Create a minimal dummy person for an undefined reference."""
    # Creates Person with:
    # - Just first_name, surname, occ
    # - Sex = UNKNOWN
    # - All other fields empty/default
    # - Assigned index
```

### 3. Updated `resolve_somebody()` Logic

The method now handles three scenarios:

**Scenario A: SomebodyDefined (Full Definition)**
```python
if isinstance(somebody, SomebodyDefined):
    # If this was a dummy, override it (keep same index)
    if key_tuple in self.dummy_persons:
        self.dummy_persons.remove(key_tuple)
        old_person = self.person_by_key[key_tuple]
        somebody.person.index = old_person.index  # Preserve index!
    
    # Register/update the person
    self.person_by_key[key_tuple] = somebody.person
```

**Scenario B: SomebodyUndefined (Already Exists)**
```python
elif isinstance(somebody, SomebodyUndefined):
    if key_tuple in self.person_by_key:
        # Return existing (dummy or defined)
        return self.person_by_key[key_tuple]
```

**Scenario C: SomebodyUndefined (First Reference)**
```python
    else:
        # Create dummy person
        dummy = self._create_dummy_person(somebody.key)
        self.person_by_key[key_tuple] = dummy
        self.dummy_persons.add(key_tuple)  # Mark as dummy
        return dummy
```

### 4. Added Statistics Methods

```python
def get_dummy_persons(self) -> List[Person[int, int, str]]:
    """Get all persons that remain as dummies."""
    
def get_statistics(self) -> Dict[str, int]:
    """Get conversion statistics including dummy count."""
```

### 5. Updated gwc.py to Show Warnings

```python
# Get statistics
stats = converter.get_statistics()

if verbose:
    print(f"  Converted {stats['defined_persons']} persons...")
    if stats['dummy_persons'] > 0:
        print(f"  Warning: {stats['dummy_persons']} undefined person(s)")
```

## How It Works

### Processing Order Example

```
File contains:
1. fam John DOE + Jane SMITH
   - witnesses: Bob WITNESS
2. (Bob WITNESS is never defined)

Processing:
├─ Family block processed
│  ├─ John DOE → SomebodyDefined → person created
│  ├─ Jane SMITH → SomebodyDefined → person created
│  └─ Bob WITNESS → SomebodyUndefined → DUMMY created ⚠️
│
└─ End of file

Result:
- 2 fully defined persons (John, Jane)
- 1 dummy person (Bob) ← Remains undefined
```

### Override Example

```
File contains:
1. fam John DOE + Jane SMITH
   - witnesses: Bob WITNESS
2. Bob WITNESS (full definition)

Processing:
├─ Family block processed
│  ├─ John DOE → person created (index 0)
│  ├─ Jane SMITH → person created (index 1)
│  └─ Bob WITNESS → DUMMY created (index 2) ⚠️
│
├─ Bob WITNESS definition block
│  └─ Bob WITNESS → OVERRIDES dummy (keeps index 2) ✓
│
└─ End of file

Result:
- 3 fully defined persons
- 0 dummies
```

## Benefits

1. **Matches OCaml behavior**: Files can be processed even with forward references
2. **Flexible ordering**: Person definitions can appear after family blocks
3. **Warning system**: Can detect and report undefined persons
4. **Index stability**: Dummy persons keep their index when overridden
5. **No errors**: Processing doesn't fail on missing definitions

## Usage

### Check for undefined persons

```python
converter = GwConverter()
converter.convert_all(blocks)

# Get dummies
dummies = converter.get_dummy_persons()
if dummies:
    print("Warning: The following persons are referenced but not defined:")
    for person in dummies:
        print(f"  - {person.first_name} {person.surname}")
```

### Get statistics

```python
stats = converter.get_statistics()
print(f"Total: {stats['total_persons']}")
print(f"Defined: {stats['defined_persons']}")
print(f"Dummies: {stats['dummy_persons']}")
print(f"Families: {stats['families']}")
```

## Comparison with OCaml

| Feature | OCaml gwc | Python gwc (now) |
|---------|-----------|------------------|
| Dummy creation | ✅ Yes ('U' marker) | ✅ Yes (dummy_persons set) |
| Override later | ✅ Yes | ✅ Yes (preserves index) |
| Index preservation | ✅ Yes | ✅ Yes |
| Warning for undefined | ✅ Yes | ✅ Yes |
| Forward references | ✅ Allowed | ✅ Allowed |

## Testing

The converter now handles:
- ✅ Families with undefined witnesses
- ✅ Families with undefined parents
- ✅ Person definitions appearing after references
- ✅ Multiple references to same undefined person
- ✅ Override of dummy with full definition
- ✅ Statistics and warnings

## Next Steps

1. Test with real `.gw` files
2. Add more detailed warnings (show which families reference undefined persons)
3. Consider adding a "strict mode" that errors on undefined persons
4. Implement the database saving with proper handling of dummies
