# Documentation Index

This directory contains comprehensive documentation for the Legacy/GeneWeb project.

## Main Documentation

### 📘 [GWC_IMPLEMENTATION.md](./GWC_IMPLEMENTATION.md) - **START HERE**

**The complete guide to the Python GWC implementation.** This is the main reference document covering:

- Architecture and processing pipeline
- Command-line options (implemented, partial, and planned)
- Parser implementation and fixes
- Dummy person system (OCaml-compatible)
- Converter API reference with code examples
- Usage examples and best practices
- Differences from OCaml version
- Implementation status and roadmap
- Troubleshooting and known issues

**Topics covered**:
- How to use `gwc.py` from command line
- How to use `GwConverter` API programmatically
- Understanding person resolution and dummy handling
- Parser fixes for inline parent definitions
- Type mapping and data enrichment
- Statistics and error handling


## Other Documentation

### 🔄 [OCAML_TO_PYTHON.md](./OCAML_TO_PYTHON.md)
Complete reference for OCaml-to-Python translation differences across the entire codebase.

**Topics**:
- Language-level differences (memory, immutability, pattern matching)
- Type system differences (ADTs, variants, records, generics)
- Module-by-module comparison
- Data structure differences (hash tables, arrays, file I/O)
- Algorithm differences (name matching, consanguinity, indexing)
- File format differences (.gw, .gwo, .gwb vs SQLite)
- Questions and clarifications needed for port
- Implementation checklist

### 🧪 [GOLDEN_MASTER.md](./GOLDEN_MASTER.md)
Testing approach and scenarios for ensuring behavioral compatibility with the legacy application.

**Topics**:
- Golden master testing methodology
- Test scenarios for web interface
- Recording and comparison process
- How to run golden master tests

### 🔒 [QUALITY_INSURANCE.md](./QUALITY_INSURANCE.md)
Quality assurance processes and standards for the project.

**Topics**:
- Branch naming conventions
- Merging rules and PR requirements
- Protected branches
- Code review process

---

## Quick Navigation

### I want to...

**...understand how gwc works**
→ Read [GWC_IMPLEMENTATION.md § Overview](./GWC_IMPLEMENTATION.md#overview)

**...use gwc from command line**
→ Read [GWC_IMPLEMENTATION.md § Command-Line Options](./GWC_IMPLEMENTATION.md#command-line-options) and [§ Usage Examples](./GWC_IMPLEMENTATION.md#usage-examples)

**...understand OCaml-to-Python differences**
→ Read [OCAML_TO_PYTHON.md](./OCAML_TO_PYTHON.md)

**...run tests**
→ Read [GOLDEN_MASTER.md](./GOLDEN_MASTER.md)

**...understand the development workflow**
→ Read [QUALITY_INSURANCE.md](./QUALITY_INSURANCE.md)

## Contributing to Documentation

When updating documentation:

1. **Always update GWC_IMPLEMENTATION.md first** - it's the single source of truth
2. **Add changelog entries** at the bottom of GWC_IMPLEMENTATION.md
3. **Keep examples up to date** with actual working code
4. **Test code snippets** before adding them to docs
5. **Update this index** when adding new doc files

### Documentation Style Guide

- Use clear, concise language
- Include working code examples
- Provide both CLI and API examples where applicable
- Link between related sections
- Keep table of contents updated
