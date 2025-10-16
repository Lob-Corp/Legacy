# OCaml to Python Translation Reference

This document tracks all differences between the original OCaml GeneWeb implementation and the Python reimplementation. It serves as a reference for developers working on the port.

---

## Table of Contents

1. [Language-Level Differences](#language-level-differences)
2. [Type System Differences](#type-system-differences)
3. [Module-by-Module Comparison](#module-by-module-comparison)
4. [Data Structures](#data-structures)
5. [Algorithm Differences](#algorithm-differences)
6. [File Format Differences](#file-format-differences)
7. [Questions & Clarifications Needed](#questions--clarifications-needed)

---

## Language-Level Differences

### Memory Management

| Aspect | OCaml | Python |
|--------|-------|--------|
| **Memory model** | Manual/compiler-controlled | Automatic garbage collection |
| **Reference counting** | Not used | CPython uses refcounting + GC |
| **Stack vs Heap** | Explicitly controlled | Managed by runtime |
| **Memory optimization flags** | `-mem` flag in gwc | Not applicable (removed) |

### Immutability

| Aspect | OCaml | Python |
|--------|-------|--------|
| **Default mutability** | Immutable by default | Mutable by default |
| **Immutable data** | Native support | `@dataclass(frozen=True)` |
| **String mutation** | Strings immutable | Strings immutable |
| **List mutation** | `ref` for mutable cells | Lists mutable by default |

### Pattern Matching

| Feature | OCaml | Python |
|---------|-------|--------|
| **Variant matching** | `match` expression | `isinstance()` + `if/elif` |
| **Exhaustiveness** | Compiler-checked | No compile-time check |
| **Guard clauses** | `when` keyword | Nested `if` inside branches |

**OCaml Example:**
```ocaml
match person with
| Undefined key -> create_dummy key
| Defined p when is_dummy p -> override_dummy p
| Defined p -> p
```

**Python Equivalent:**
```python
if isinstance(somebody, SomebodyUndefined):
    return create_dummy(somebody.key)
elif isinstance(somebody, SomebodyDefined):
    if is_dummy(somebody.person):
        return override_dummy(somebody.person)
    else:
        return somebody.person
```

### Function Definition

| Aspect | OCaml | Python |
|--------|-------|--------|
| **Currying** | Automatic | Must use `functools.partial` |
| **Type annotations** | Required in `.mli` files | Optional (type hints) |
| **Named parameters** | `~name:` syntax | Standard `name=` syntax |
| **Optional parameters** | `?name:` syntax | `name: Optional[T] = None` |

---

## Type System Differences

### Algebraic Data Types (ADTs)

#### Variant Types

**OCaml:**
```ocaml
type somebody =
  | Undefined of key
  | Defined of person

type death_status =
  | NotDead
  | Dead
  | DeadYoung
  | DeadDontKnowWhen
  | DontKnowIfDead
  | OfCourseDead
```

**Python:**
```python
@dataclass(frozen=True)
class SomebodyUndefined:
    key: Key

@dataclass(frozen=True)
class SomebodyDefined:
    person: Person

Somebody = Union[SomebodyUndefined, SomebodyDefined]

# For death_status - using class hierarchy
class DeathStatusBase:
    pass

class NotDead(DeathStatusBase):
    pass

class Dead(DeathStatusBase):
    def __init__(self, reason: DeathReason, date: CompressedDate):
        self.reason = reason
        self.date = date
```

**Key Difference**: OCaml variants are a single type with multiple constructors. Python uses separate classes + union types or inheritance.

#### Record Types

**OCaml:**
```ocaml
type ('iper, 'person, 'string) gen_person = {
  first_name : 'string;
  surname : 'string;
  occ : int;
  image : 'string;
  public_name : 'string;
  (* ... *)
}
```

**Python:**
```python
@dataclass(frozen=True)
class Person(Generic[IdxT, PersonT, PersonDescriptorT]):
    index: IdxT
    first_name: PersonDescriptorT
    surname: PersonDescriptorT
    occ: int
    sex: Sex
    # ...
```

**Key Difference**: Python uses `@dataclass(frozen=True)` to emulate OCaml's immutable records while Generics are added to emumale Ocaml's polymorphic type variables.

### Option Types

| OCaml | Python |
|-------|--------|
| `'a option` | `Optional[T]` or `T \| None` |
| `Some x` | `x` (not None) |
| `None` | `None` |

**OCaml:**
```ocaml
let birth_place : string option = Some "Paris"
let death_place : string option = None
```

**Python:**
```python
birth_place: Optional[str] = "Paris"
death_place: Optional[str] = None
```

### Parametric Polymorphism (Generics)

**OCaml:**
```ocaml
type 'a list = 
  | [] 
  | (::) of 'a * 'a list

type ('idx, 'person, 'string) gen_person = {
  index : 'idx;
  first_name : 'string;
  (* ... *)
}
```

**Python:**
```python
# Built-in list is already generic
data: List[int] = [1, 2, 3]

# Custom generic types
IdxT = TypeVar('IdxT')
PersonT = TypeVar('PersonT')
PersonDescriptorT = TypeVar('PersonDescriptorT')

@dataclass(frozen=True)
class Person(Generic[IdxT, PersonT, PersonDescriptorT]):
    index: IdxT
    first_name: PersonDescriptorT
    # ...
```

**Key Difference**: Python's generics are runtime-only (via `typing` module). OCaml's are compile-time with full type erasure.

---

## Module-by-Module Comparison

### gwc (GeneWeb Compiler)

Check [gwc Differences from OCaml](./GWC_IMPLEMENTATION.mdGWD)

### Date

TBA

### Person Data Structure

#### OCaml: `legacy/lib/def/def.ml`

```ocaml
type gen_person 'person 'string = {
  first_name : 'string;
  surname : 'string;
  occ : iper;
  image : 'string;
  first_names_aliases : list 'string;
  surnames_aliases : list 'string;
  public_name : 'string;
  qualifiers : list 'string;
  titles : list (gen_title 'string);
  rparents : list (gen_relation 'person 'string);
  related : list iper;
  aliases : list 'string;
  occupation : 'string;
  sex : sex;
  access : access;
  birth : codate;
  birth_place : 'string;
  birth_note : 'string;
  birth_src : 'string;
  baptism : codate;
  baptism_place : 'string;
  baptism_note : 'string;
  baptism_src : 'string;
  death : death;
  death_place : 'string;
  death_note : 'string;
  death_src : 'string;
  burial : burial;
  burial_place : 'string;
  burial_note : 'string;
  burial_src : 'string;
  pevents : list (gen_pers_event 'person 'string);
  notes : 'string;
  psources : 'string;
}
```

#### Python: `src/libraries/person.py`

```python
@dataclass(frozen=True)
class Person(Generic[IdxT, PersonT, PersonDescriptorT]):
    index: IdxT
    first_name: PersonDescriptorT
    surname: PersonDescriptorT
    occ: int
    image: str
    public_name: PersonDescriptorT
    qualifiers: List[PersonDescriptorT]
    aliases: List[PersonDescriptorT]
    first_names_aliases: List[PersonDescriptorT]
    surname_aliases: List[PersonDescriptorT]
    titles: List[Title[PersonDescriptorT]]
    non_native_parents_relation: List[Relation[PersonT, PersonDescriptorT]]
    related_persons: List[PersonT]
    occupation: PersonDescriptorT
    sex: Sex
    access_right: AccessRight
    birth_date: Optional[CompressedDate]
    birth_place: PersonDescriptorT
    birth_note: PersonDescriptorT
    birth_src: PersonDescriptorT
    baptism_date: Optional[CompressedDate]
    baptism_place: PersonDescriptorT
    baptism_note: PersonDescriptorT
    baptism_src: PersonDescriptorT
    death: DeathStatusBase
    death_place: PersonDescriptorT
    death_note: PersonDescriptorT
    death_src: PersonDescriptorT
    burial: BurialInfoBase
    burial_place: PersonDescriptorT
    burial_note: PersonDescriptorT
    burial_src: PersonDescriptorT
    personal_events: List[PersonalEvent[PersonT, PersonDescriptorT]]
    notes: PersonDescriptorT
    src: PersonDescriptorT
```

**Key Differences:**

| Field | OCaml | Python | Notes |
|-------|-------|--------|-------|
| `index` | Not in record | `index: IdxT` | Added for tracking |
| `rparents` | Field name | `non_native_parents_relation` | More descriptive |
| `related` | `list iper` | `related_persons: List[PersonT]` | Generic type |
| `access` | Field name | `access_right` | More explicit |
| `birth` | `codate` | `birth_date: Optional[CompressedDate]` | Split into date/place/note/src |
| `death` | `death` variant | `death: DeathStatusBase` | Class hierarchy |
| `pevents` | Field name | `personal_events` | More descriptive |
| `psources` | Field name | `src` | Shortened |

**Question**: What is `iper` in OCaml? It appears to be a person index type. In Python, we use the generic `PersonT` type variable.

### Family Data Structure

#### OCaml: `legacy/lib/def/def.ml`

```ocaml
type gen_family 'person 'string = {
  marriage : codate;
  marriage_place : 'string;
  marriage_note : 'string;
  marriage_src : 'string;
  witnesses : array 'person;
  relation : relation_kind;
  divorce : divorce;
  fevents : list (gen_fam_event 'person 'string);
  comment : 'string;
  origin_file : 'string;
  fsources : 'string;
  fam_index : ifam;
}
```

#### Python: `src/libraries/family.py`

```python
@dataclass(frozen=True)
class Family(Generic[IdxT, PersonT, FamilyDescriptorT]):
    index: IdxT
    marriage_date: CompressedDate
    marriage_place: FamilyDescriptorT
    marriage_note: FamilyDescriptorT
    marriage_src: FamilyDescriptorT
    witnesses: List[PersonT]
    relation_kind: MaritalStatus
    divorce_status: DivorceStatusBase
    family_events: List[FamilyEvent[PersonT, FamilyDescriptorT]]
    comment: FamilyDescriptorT
    origin_file: FamilyDescriptorT
    src: FamilyDescriptorT
```

**Key Differences:**

| Field | OCaml | Python | Notes |
|-------|-------|--------|-------|
| `witnesses` | `array 'person` | `witnesses: List[PersonT]` | Array→List |
| `relation` | Field name | `relation_kind` | More explicit |
| `divorce` | `divorce` variant | `divorce_status: DivorceStatusBase` | Class hierarchy |
| `fevents` | Field name | `family_events` | More descriptive |
| `fsources` | Field name | `src` | Shortened |
| `fam_index` | In record | `index: IdxT` | Renamed |

---

## Data Structures

### Hash Tables vs Dictionaries

#### OCaml Hash Tables

```ocaml
let g_names : (int, person) Hashtbl.t = Hashtbl.create 5003

(* Insert *)
Hashtbl.add g_names (person_hash key) person

(* Lookup *)
let persons = Hashtbl.find_all g_names hash
```

**Features:**
- Multiple values per key (with `find_all`)
- Hash function customizable
- Mutable

#### Python Dictionaries

```python
person_by_key: Dict[Tuple[str, str, int], Person] = {}

# Insert
person_by_key[(first_name, surname, occ)] = person

# Lookup
person = person_by_key.get((first_name, surname, occ))
```

**Differences:**

| Aspect | OCaml | Python |
|--------|-------|--------|
| **Multiple values** | `Hashtbl.find_all` returns list | Must use `Dict[K, List[V]]` |
| **Hash function** | `person_hash` with `Name.crush_lower` | Tuple hash (default) |
| **Missing keys** | Raises `Not_found` | Returns `None` with `.get()` |

**Missing**: Python version doesn't implement `Name.crush_lower` for fuzzy name matching.

**Question**: Should we implement name normalization (`crush_lower`) for better duplicate detection?

### Arrays vs Lists

#### OCaml Arrays

```ocaml
let witnesses : person array = [| p1; p2; p3 |]
let first = witnesses.(0)
```

**Features:**
- Fixed size
- O(1) indexed access
- Mutable elements

#### Python Lists

```python
witnesses: List[Person] = [p1, p2, p3]
first = witnesses[0]
```

**Features:**
- Dynamic size
- O(1) indexed access
- Mutable

**Key Difference**: OCaml arrays are fixed-size, Python lists are dynamic. Functionally equivalent for our use case.

### File I/O

#### OCaml: Binary Files with Markers

```ocaml
(* Write person to .gwb file *)
output_char oc 'D';  (* Defined marker *)
output_binary_int oc person.index;
output_value oc person;

(* Write dummy *)
output_char oc 'U';  (* Undefined marker *)
output_binary_int oc key_hash;
```

**Features:**
- Custom binary format
- Single-byte markers for state ('U'/'D')
- Uses OCaml's `output_value` for serialization
- File position = person index

#### Python: In-Memory + SQLite (Planned)

```python
# In-memory tracking
dummy_persons: set[Tuple[str, str, int]] = set()
person_by_key: Dict[Tuple[str, str, int], Person] = {}

# Mark as dummy
dummy_persons.add((first_name, surname, occ))

# Mark as defined
dummy_persons.remove((first_name, surname, occ))

# Future: SQLite persistence
# CREATE TABLE persons (
#     id INTEGER PRIMARY KEY,
#     is_dummy BOOLEAN,
#     ...
# );
```

**Key Differences:**

| Aspect | OCaml | Python |
|--------|-------|--------|
| **Storage** | Binary file with markers | In-memory, then SQLite |
| **Persistence** | File-based, across runs | In-memory per run |
| **State tracking** | 'U'/'D' markers | Set membership |
| **Lookup** | File seek by index | Dict lookup by key |

---

## Algorithm Differences

TBA

## File Format Differences

### Input: .gw Files

**Status**: ✅ COMPATIBLE - Same format in OCaml and Python

**Format Example:**
```gw
encoding: utf-8

fam John DOE 1/1/1950 + Jane SMITH 1/2/1952
beg
- m: Bob DOE 1/1/1980
end

pevt Bob DOE
#birt 1/1/1980 #p Paris
end pevt
```

### Intermediate: .gwo Files

**OCaml**: Used for two-phase compilation
- Phase 1: `.gw` → `.gwo` (parsed, not linked)
- Phase 2: `.gwo` → `.gwb` (linked)

**Python**: ❌ NOT USED - Single-phase compilation

### Output: .gwb vs SQLite

#### OCaml: .gwb Format

**Structure:**
```
base.gwb/
├── base           # Base info
├── base.acc       # Access rights
├── base.inx       # Person index
├── patches/       # Updates
├── particles.txt  # Name particles
└── *.gwb files    # Binary data
```

**Features:**
- Custom binary format
- Optimized for read performance
- In-place updates via patches
- File locking for multi-user

#### Python: SQLite (Planned)

**Structure:**
```sql
CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    surname TEXT,
    occ INTEGER,
    is_dummy BOOLEAN,
    sex TEXT,
    birth_date TEXT,
    -- ... all other fields
);

CREATE TABLE families (
    id INTEGER PRIMARY KEY,
    father_id INTEGER REFERENCES persons(id),
    mother_id INTEGER REFERENCES persons(id),
    marriage_date TEXT,
    -- ...
);
```

**Features:**
- Standard SQL format
- ACID transactions
- Query flexibility
- Standard locking mechanisms

**Status**: 🚧 SCHEMA DEFINED, NOT YET IMPLEMENTED

## Contributing

When porting OCaml code to Python:

1. **Document differences** in this file
2. **Add questions** to the Questions section if behavior is unclear
3. **Update the checklist** when completing features
4. **Note algorithm changes** if the Python version differs
5. **Keep examples** showing both OCaml and Python versions

