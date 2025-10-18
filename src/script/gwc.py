import argparse
import os
import sys
from typing import Dict, List, Tuple

# TODO: complete when database is implemented

from script.gw_parser import parse_gw_file, GwConverter
from libraries.person import Person
from libraries.family import Family


def appendFileData(
    files: list[tuple[str, bool, str, int]],
    x: str,
    separate: bool,
    bnotes: str,
    shift: int
) -> None:
    """Validate and append file data to the list."""
    if x.endswith(".gw"):
        if not os.path.exists(x):
            raise FileNotFoundError(f'File "{x}" not found')
    else:
        raise argparse.ArgumentTypeError(
            f'Don\'t know what to do with "{x}"'
        )
    files.append((x, separate, bnotes, shift))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="GeneWeb Compiler/Linker",
        usage="gwc [options] [files]\n"
              "where [files] are a list of files:\n"
              "  source files end with .gw\n"
              "and [options] are:"
    )
    parser.add_argument(
        "-bnotes", type=str, default="merge",
        help="[drop|erase|first|merge] Behavior "
        "for base notes of the next file.")
    parser.add_argument(
        "-cg",
        action="store_true",
        help="Compute consanguinity")
    parser.add_argument(
        "-ds", type=str, default="",
        help="Set the source field for persons and "
        "families without source data")
    parser.add_argument(
        "-f",
        action="store_true",
        help="Remove database if already existing")
    parser.add_argument(
        "-mem",
        action="store_true",
        help="Save memory, but slower")
    parser.add_argument(
        "-nc",
        action="store_true",
        help="No consistency check")
    parser.add_argument(
        "-nofail",
        action="store_true",
        help="No failure in case of error")
    parser.add_argument(
        "-nolock",
        action="store_true",
        help="Do not lock database")
    parser.add_argument(
        "-nopicture", action="store_true",
        help="Do not create associative pictures")
    parser.add_argument(
        "-o", type=str, default="a.sql",
        help="Output database (default: a.sql)")
    parser.add_argument(
        "-particles", type=str, default="",
        help="Particles file (default = predefined particles)")
    parser.add_argument("-q", action="store_true", help="Quiet")
    parser.add_argument(
        "-sep",
        action="store_true",
        help="Separate all persons in next file")
    parser.add_argument(
        "-sh", type=int, default=0,
        help="Shift all persons numbers in next files")
    parser.add_argument("-stats", action="store_true", help="Print statistics")
    parser.add_argument("-v", action="store_true", help="Verbose")
    parser.add_argument("files", nargs="*", help="Input .gw files")

    args = parser.parse_args()

    out_file: str = args.o if hasattr(args, 'o') else "a.sql"
    input_file_data: list[tuple[str, bool, str, int]] = []
    separate: bool = args.sep
    bnotes: str = args.bnotes
    shift: int = args.sh

    # Validate output file name
    basename: str = os.path.basename(out_file)
    if not all((c.isalnum() or c == '-' or c == '.') for c in basename):
        print(
            f'The database name "{out_file}" contains a forbidden character.')
        print("Allowed characters: a..z, A..Z, 0..9, -")
        sys.exit(2)

    # Collect files
    for x in args.files:
        appendFileData(input_file_data, x, separate, bnotes, shift)
        separate = False
        bnotes = "merge"

    # Process files
    if not input_file_data:
        parser.print_help()
        sys.exit(1)

    verbose: bool = args.v and not args.q
    all_persons: list[Person] = []
    all_families: list[Family] = []
    all_base_notes: list[tuple[str, str]] = []
    all_wizard_notes: dict[str, str] = {}
    all_page_extensions: dict[str, str] = {}

    if verbose:
        print(f"Processing {len(input_file_data)} file(s)...")

    for idx, (filename, separate, bnotes_mode, shift) in enumerate(
        input_file_data, 1
    ):
        if verbose:
            print(f"\n[{idx}/{len(input_file_data)}] Processing {filename}...")

        try:
            # Parse the .gw file
            if verbose:
                print(f"  Parsing {filename}...")

            gw_syntax_blocks = parse_gw_file(filename)

            if verbose:
                print(f"  Parsed {len(gw_syntax_blocks)} blocks")
                print("  Converting to application types...")

            converter = GwConverter()
            converter.convert_all(gw_syntax_blocks)
            persons = converter.get_all_persons()
            families = converter.get_all_families()
            base_notes = converter.get_base_notes()
            wizard_notes = converter.get_wizard_notes()
            page_extensions = converter.get_page_extensions()
            stats = converter.get_statistics()

            if verbose:
                print(
                    f"  Converted {stats['defined_persons']} persons, "
                    f"{stats['families']} families"
                )
                if stats['dummy_persons'] > 0:
                    print(
                        f"  Warning: {stats['dummy_persons']} "
                        f"undefined person(s)"
                    )
                if stats['base_notes'] > 0:
                    print(f"  Found {stats['base_notes']} base note(s)")
                if stats['wizard_notes'] > 0:
                    print(f"  Found {stats['wizard_notes']} wizard note(s)")
                if stats['page_extensions'] > 0:
                    print(
                        f"  Found {stats['page_extensions']} "
                        f"page extension(s)"
                    )

            # TODO: Apply shift if specified
            if shift != 0 and verbose:
                print(f"  Note: -sh {shift} specified but not yet implemented")

            # TODO: Apply separate if specified
            if separate and verbose:
                print("  Note: -sep specified but not yet implemented")

            from dataclasses import replace
            families_with_origin = [
                replace(fam, origin_file=filename) for fam in families
            ]

            all_persons.extend(persons)
            all_families.extend(families_with_origin)

            match bnotes_mode:
                case "merge":
                    all_base_notes.extend(base_notes)
                    all_wizard_notes.update(wizard_notes)
                    all_page_extensions.update(page_extensions)
                case "first" if not all_base_notes:
                    all_base_notes.extend(base_notes)
                    all_wizard_notes.update(wizard_notes)
                    all_page_extensions.update(page_extensions)
                case "drop":
                    pass
                case "erase":
                    all_base_notes = list(base_notes)
                    all_wizard_notes = dict(wizard_notes)
                    all_page_extensions = dict(page_extensions)

            if bnotes_mode != "merge" and verbose:
                print(
                    f"  Applied -bnotes {bnotes_mode} "
                    f"for database-level data"
                )

        except Exception as e:
            if args.nofail:
                print(f"Error processing {filename}: {e}", file=sys.stderr)
                if verbose:
                    import traceback
                    traceback.print_exc()
                continue
            else:
                print(f"Error processing {filename}: {e}", file=sys.stderr)
                if verbose:
                    import traceback
                    traceback.print_exc()
                sys.exit(1)

    # Print statistics
    if args.stats or verbose:
        print("\n" + "=" * 50)
        print("Parsing Statistics:")
        print("=" * 50)
        print(f"Total persons: {len(all_persons)}")
        print(f"Total families: {len(all_families)}")
        print(f"Total base notes: {len(all_base_notes)}")
        print(f"Total wizard notes: {len(all_wizard_notes)}")
        print(f"Total page extensions: {len(all_page_extensions)}")
        print(f"Files processed: {len(input_file_data)}")
        # TODO: temporary, until database is implemented
        print_data(
            all_persons,
            all_families,
            all_base_notes,
            all_wizard_notes,
            all_page_extensions
        )
        print("=" * 50)

    # TODO: Save to SQLite database
    if verbose:
        print(f"\nDatabase output: {out_file}")
        print("Note: SQLite database saving not yet implemented")
        print("Data has been parsed and converted to application types")

    # TODO: Compute consanguinity if requested
    if args.cg and verbose:
        print("Note: -cg (consanguinity) not yet implemented")

    # TODO: Handle default source
    if args.ds and verbose:
        print(f"Note: -ds '{args.ds}' (default source) not yet implemented")

    # TODO: Handle particles file
    if args.particles and verbose:
        print(
            f"Note: -particles '{args.particles}' "
            f"not yet implemented"
        )

    # TODO: No consistency check
    if args.nc and verbose:
        print("Note: -nc (no consistency check) not yet implemented")

    if verbose:
        print("\nProcessing complete!")

    return 0


def print_data(
        all_persons: List[Person],
        all_families: List[Family],
        all_base_notes: List[Tuple[str, str]],
        all_wizard_notes: Dict[str, str],
        all_page_extensions: Dict[str, str]):
    """Serve as a temporary function to print parsed data.
    To remove when database saving is implemented."""

    def _get(obj, *names):
        for n in names:
            if hasattr(obj, n):
                val = getattr(obj, n)
                if val is not None:
                    return val
        if hasattr(obj, "__dict__"):
            d = obj.__dict__
            for k, v in d.items():
                for n in names:
                    if n in k and v is not None:
                        return v
        return None

    def _id_of(o):
        return _get(o, "id", "pid", "fid", "xref") or str(o)

    def _format_person(p):
        pid = _id_of(p)
        name = _get(p, "name", "full_name", "fullname")
        if not name:
            given = _get(p, "given", "given_name", "firstname", "first")
            family = _get(p, "surname", "last", "lastname", "family")
            if given or family:
                name = " ".join(filter(None, (given, family)))
        sex = _get(p, "sex", "gender")
        birth = _get(p, "birth", "bdate", "born")
        death = _get(p, "death", "ddate", "died")
        parts = [f"id={pid}"]
        if name:
            parts.append(f"name=\"{name}\"")
        if sex:
            parts.append(f"sex={sex}")
        if birth or death:
            parts.append(f"b:{birth or '?'} d:{death or '?'}")
        return "  - " + " | ".join(parts)

    def _format_family(f):
        fid = _id_of(f)
        hus = _get(f, "husband", "husb", "hus", "h", "father")
        wife = _get(f, "wife", "w", "mother", "m")
        children = _get(
            f,
            "children",
            "kids",
            "children_list",
            "childs",
            "child")

        def _ref(x):
            if hasattr(x, "__dict__"):
                return _id_of(x)
            return str(x)
        child_ids = []
        if children is not None:
            if isinstance(children, (list, tuple)):
                child_ids = [_ref(c) for c in children]
            else:
                child_ids = [_ref(children)]
        parts = [f"id={fid}"]
        if hus:
            parts.append(f"H={_ref(hus)}")
        if wife:
            parts.append(f"W={_ref(wife)}")
        if child_ids:
            parts.append(f"children={len(child_ids)}")
        tail = f" -> [{', '.join(child_ids)}]" if child_ids else ""
        return "  - " + " | ".join(parts) + tail

    print("\nPersons:")
    if not all_persons:
        print("  (none)")
    else:
        for p in all_persons:
            try:
                print(_format_person(p))
            except Exception:
                print("  -", str(p))

    print("\nFamilies:")
    if not all_families:
        print("  (none)")
    else:
        for f in all_families:
            try:
                print(_format_family(f))
            except Exception:
                print("  -", str(f))

    print("\nBase Notes:")
    if not all_base_notes:
        print("  (none)")
    else:
        for page, content in all_base_notes:
            content_preview = (
                content[:80] + "..." if len(content) > 80 else content
            )
            print(f"  - Page: {page!r}")
            print(f"    Content: {content_preview!r}")

    print("\nWizard Notes:")
    if not all_wizard_notes:
        print("  (none)")
    else:
        for wizard_id, content in all_wizard_notes.items():
            content_preview = (
                content[:80] + "..." if len(content) > 80 else content
            )
            print(f"  - Wizard ID: {wizard_id!r}")
            print(f"    Content: {content_preview!r}")

    print("\nPage Extensions:")
    if not all_page_extensions:
        print("  (none)")
    else:
        for page_name, content in all_page_extensions.items():
            content_preview = (
                content[:80] + "..." if len(content) > 80 else content
            )
            print(f"  - Page: {page_name!r}")
            print(f"    Content: {content_preview!r}")


if __name__ == "__main__":
    sys.exit(main())
