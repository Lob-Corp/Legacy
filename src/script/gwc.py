import argparse
import os
import sys


def check_magic(fname: str, ic) -> None:
    magic_gwo: str = "GnWo000o"
    b: str = ic.read(len(magic_gwo))
    if b != magic_gwo:
        if b[:4] == magic_gwo[:4]:
            raise Exception(
                f'"{fname}" is a GeneWeb object file, but not compatible')
        else:
            raise Exception(
                f'"{fname}" is not a GeneWeb object file, or it is a very old version')


def appendFileData(files: list[tuple[str, bool, str, int]],
                   x: str, separate: bool, bnotes: str, shift: int) -> None:
    if x.endswith(".gw"):
        pass  # Compilation handled later
    else:
        raise argparse.ArgumentTypeError(f'Don\'t know what to do with "{x}"')
    files.append((x, separate, bnotes, shift))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="GeneWeb Compiler/Linker",
        usage="gwc [options] [files]\n"
              "where [files] are a list of files:\n"
              "  source files end with .gw\n"
              "and [options] are:"
    )
    parser.add_argument(
        "-bnotes", type=str, default="merge",
        help="[drop|erase|first|merge] Behavior for base notes of the next file.")
    parser.add_argument("-c", action="store_true", help="Only compiling")
    parser.add_argument(
        "-cg",
        action="store_true",
        help="Compute consanguinity")
    parser.add_argument(
        "-ds", type=str, default="",
        help="Set the source field for persons and families without source data")
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
        "-o", type=str, default="a.gwb",
        help="Output database (default: a.gwb)")
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

    out_file: str = args.o if hasattr(args, 'o') else "a.gwb"
    input_file_data: list[tuple[str, bool, str, int]] = []
    separate: bool = args.sep
    bnotes: str = args.bnotes
    shift: int = args.sh

    # Validate output file name
    basename: str = os.path.basename(out_file)
    if not all(c.isalnum() or c == '-' for c in basename):
        print(
            f'The database name "{out_file}" contains a forbidden character.')
        print("Allowed characters: a..z, A..Z, 0..9, -")
        sys.exit(2)

    # Collect files
    for x in args.files:
        appendFileData(input_file_data, x, separate, bnotes, shift)
        separate = False
        bnotes = "merge"

    for x, separate, bnotes, shift in input_file_data:
        if x.endswith(".gw"):
            # TODO: Parse .gw file and create app types
            pass
        else:
            raise argparse.ArgumentTypeError(
                f'Don\'t know what to do with "{x}"')


if __name__ == "__main__":
    main()
