# OCaml to Python Translation Reference

This document tracks all differences between the original OCaml GeneWeb implementation and the Python reimplementation. It serves as a reference for developers working on the port.

## Key Architectural Difference: Bidirectional Linking

**OCaml**: Uses separate parallel arrays for relationships (ascends, unions, couples, descends) with index-based linking.

**Python**: Uses integrated object references with generic types for bidirectional linking:
- `Person` has 4 type parameters: `[IdxT, PersonT, PersonDescriptorT, FamilyT]`
- `Family` has 3 type parameters: `[IdxT, PersonT, FamilyDescriptorT]`
- Direct object references instead of index lookups
- See [Bidirectional Linking Architecture](#bidirectional-linking-architecture) for details

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
class Person(Generic[IdxT, PersonT, PersonDescriptorT, FamilyT]):
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
    birth_date: CompressedDate
    birth_place: PersonDescriptorT
    birth_note: PersonDescriptorT
    birth_src: PersonDescriptorT
    baptism_date: CompressedDate
    baptism_place: PersonDescriptorT
    baptism_note: PersonDescriptorT
    baptism_src: PersonDescriptorT
    death_status: DeathStatusBase
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
    ascend: Ascendants[FamilyT]
    families: List[FamilyT]
```

**Bidirectional Linking:**

In OCaml, persons and families reference each other through separate types:
- `gen_ascend`: Links person → parent family (where person is a child)
- `gen_union`: Links person → spouse families (where person is a parent)
- `gen_descend`: Links family → children

In Python, these are simplified using generic types:
- `Person.ascend: Ascendants[FamilyT]` - Links to parent family (bidirectional with `Family.children`)
- `Person.families: List[FamilyT]` - Links to spouse families (bidirectional with `Family.parents`)
- `Family.parents: Parents[PersonT]` - Links to parent persons (bidirectional with `Person.families`)
- `Family.children: List[PersonT]` - Links to child persons (bidirectional with `Person.ascend`)

**Key Differences:**

| Field | OCaml | Python | Notes |
|-------|-------|--------|-------|
| `index` | Not in record | `index: IdxT` | Added for tracking |
| `rparents` | Field name | `non_native_parents_relation` | More descriptive |
| `related` | `list iper` | `related_persons: List[PersonT]` | Generic type |
| `access` | Field name | `access_right` | More explicit |
| `birth` | `codate` | `birth_date: Optional[CompressedDate]` | Split into date/place/note/src |
| `death` | `death` variant | `death_status: DeathStatusBase` | Class hierarchy |
| `pevents` | Field name | `personal_events` | More descriptive |
| `psources` | Field name | `src` | Shortened |
| **Ascendants** | Separate `gen_ascend` type | `ascend: Ascendants[FamilyT]` | **Integrated, bidirectional** |
| **Unions** | Separate `gen_union` type | `families: List[FamilyT]` | **Integrated, bidirectional** |

**Type Parameters:**
- OCaml `gen_person` has 3 type params: `('iper, 'person, 'string)`
- Python `Person` has 4 type params: `Generic[IdxT, PersonT, PersonDescriptorT, FamilyT]`
  - Added `FamilyT` for bidirectional linking with families

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
    parents: Parents[PersonT]
    children: List[PersonT]
```

**Bidirectional Linking:**

In OCaml, families store parent/child relationships through separate types:
- `gen_couple`: Stored separately, links family → parents
- `gen_descend`: Stored separately, links family → children

In Python, these are integrated directly into the `Family` dataclass:
- `Family.parents: Parents[PersonT]` - Direct link to parent persons (bidirectional with `Person.families`)
- `Family.children: List[PersonT]` - Direct link to child persons (bidirectional with `Person.ascend`)

**Key Differences:**

| Field | OCaml | Python | Notes |
|-------|-------|--------|-------|
| `witnesses` | `array 'person` | `witnesses: List[PersonT]` | Array→List |
| `relation` | Field name | `relation_kind` | More explicit |
| `divorce` | `divorce` variant | `divorce_status: DivorceStatusBase` | Class hierarchy |
| `fevents` | Field name | `family_events` | More descriptive |
| `fsources` | Field name | `src` | Shortened |
| `fam_index` | In record | `index: IdxT` | Renamed |
| **Couple** | Separate `gen_couple` type | `parents: Parents[PersonT]` | **Integrated, bidirectional** |
| **Descend** | Separate `gen_descend` type | `children: List[PersonT]` | **Integrated, bidirectional** |

**Type Parameters:**
- OCaml `gen_family` has 2 type params: `('person, 'string)`
- Python `Family` has 3 type params: `Generic[IdxT, PersonT, FamilyDescriptorT]`
  - Added `IdxT` for explicit index typing

### Bidirectional Linking Architecture

#### OCaml Approach: Separate Arrays

OCaml stores relationships in separate parallel arrays:

```ocaml
(* Person linking *)
type 'family gen_ascend = { 
  parents : 'family option;     (* Parent family *)
  consang : Adef.fix            (* Consanguinity rate *)
}
type 'family gen_union = { 
  family : 'family array         (* Spouse families *)
}
(* Family linking *)
type 'person gen_descend = { 
  children : 'person array       (* Child persons *)
}
(* gen_couple stored separately, not in gen_family record *)
```

**Storage Model:**
- `persons: array gen_person` - Person data
- `ascends: array gen_ascend` - Person → parent family links (index-aligned with persons)
- `unions: array gen_union` - Person → spouse families links (index-aligned)
- `families: array gen_family` - Family data
- `couples: array gen_couple` - Family → parent persons links (index-aligned with families)
- `descends: array gen_descend` - Family → children links (index-aligned)

**Access Pattern:**
```ocaml
(* Get person's parent family *)
let ascend = ascends.(person_index) in
Option.map (fun fam_idx -> families.(fam_idx)) ascend.parents
(* Get person's spouse families *)
let union = unions.(person_index) in
Array.map (fun fam_idx -> families.(fam_idx)) union.family
```

#### Python Approach: Integrated References

Python integrates relationships directly into dataclass fields using generic types:

```python
@dataclass(frozen=True)
class Person(Generic[IdxT, PersonT, PersonDescriptorT, FamilyT]):
    # ... other fields ...
    ascend: Ascendants[FamilyT]   # Link to parent family (bidirectional)
    families: List[FamilyT]        # Links to spouse families (bidirectional)

@dataclass(frozen=True)  
class Ascendants(Generic[FamilyT]):
    parents: FamilyT | None        # Direct reference to parent Family object
    consanguinity_rate: ConsanguinityRate

@dataclass(frozen=True)
class Family(Generic[IdxT, PersonT, FamilyDescriptorT]):
    # ... other fields ...
    parents: Parents[PersonT]      # Links to parent persons (bidirectional)
    children: List[PersonT]        # Links to child persons (bidirectional)

class Parents(Generic[PersonT]):
    def __init__(self, parents: List[PersonT]):
        self.parents = parents     # Direct references to Person objects
```

**Storage Model:**
- `persons: List[Person]` - Person data with embedded family references
- `families: List[Family]` - Family data with embedded person references
- All links are bidirectional object references

**Access Pattern:**
```python
# Get person's parent family (direct reference)
parent_family = person.ascend.parents

# Get person's spouse families (direct references)
spouse_families = person.families

# Get family's parents (direct references)
parent_persons = family.parents.parents

# Get family's children (direct references)
children = family.children
```

#### Key Architectural Differences

| Aspect | OCaml | Python |
|--------|-------|--------|
| **Separation** | 6 separate parallel arrays | 2 lists with embedded refs |
| **Indirection** | Index-based (integer lookup) | Direct object references |
| **Type safety** | Separate types enforce structure | Generics enforce structure |
| **Memory layout** | Struct-of-arrays | Array-of-structs |
| **Modification** | Update separate array slot | Immutable (use `dataclasses.replace()`) |
| **Traversal** | Requires index → array lookup | Direct object navigation |

**Advantages of Python Approach:**
- More intuitive API (follow references directly)
- Less index management overhead
- Clearer bidirectional relationships
- Better type inference with generics

**Advantages of OCaml Approach:**
- Better cache locality (array access)
- Easier serialization (flat arrays)
- More memory efficient (indices are smaller than references)
- Safer concurrent access (immutable indices)

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

### Bidirectional Linking in Converter

The bidirectional linking architecture affects how the converter builds the data structures:

#### OCaml (`db1link.ml`): Index-based Two-Phase Linking

**Phase 1: Create entries with indices**
```ocaml
(* Add person to persons array, get index *)
let person_idx = add_person person in
(* Add family to families array, get index *)  
let family_idx = add_family family in
(* Store parent/child relationships using indices *)
ascends.(person_idx) <- { parents = Some family_idx; consang = rate };
unions.(father_idx) <- { family = Array.append unions.(father_idx).family [|family_idx|] };
descends.(family_idx) <- { children = [|child_idx1; child_idx2|] };
```

**Phase 2: Build couples array**
```ocaml
(* Link family to parent persons using indices *)
couples.(family_idx) <- (father_idx, mother_idx);
```

#### Python (`gw_converter.py`): Object-based Single-Phase Linking

**Single Phase: Create objects with direct references**
```python
# Create parent persons with bidirectional links
father = Person(
    # ... fields ...
    ascend=Ascendants(parents=None, ...),  # No parent family
    families=[family]  # Will be filled after family creation
)

# Create family with direct object references
family = Family(
    # ... fields ...
    parents=Parents([father, mother]),  # Direct references
    children=[child1, child2]           # Direct references
)

# Update parent persons to reference the family
father = replace(father, families=[family])
mother = replace(mother, families=[family])

# Update children to reference the family as parents
child1 = replace(child1, ascend=Ascendants(parents=family, ...))
child2 = replace(child2, ascend=Ascendants(parents=family, ...))
```

**Key Difference**: Python uses `dataclasses.replace()` to update frozen dataclasses with bidirectional references after initial creation, while OCaml updates mutable parallel arrays by index.

#### Implications

| Aspect | OCaml | Python |
|--------|-------|--------|
| **Creation order** | Can create in any order, link later by index | Must create objects, then update with `replace()` |
| **Circular refs** | No issue (indices don't care) | Requires careful ordering + `replace()` |
| **Memory usage** | Indices are small (4-8 bytes) | Object references larger (~8 bytes + GC overhead) |
| **Verification** | Check index bounds | Type system ensures references are valid |
| **Dummy handling** | Write 'U' marker, upgrade to 'D' later | Create dummy object, `replace()` with real data |

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