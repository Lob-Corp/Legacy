import re
import tempfile
import os
from database.person import DeathStatus


def detect_gedcom_version(path: str) -> str:
    """Detect GEDCOM version (5.5, 5.5.1, 7.0, etc.)"""
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if re.match(r"^\d+\s+VERS\s+", line):
                return line.strip().split()[-1]
    return "unknown"


def parse_with_ged4py(path: str) -> list | None:
    """Try parsing with ged4py."""
    try:
        from ged4py.parser import GedcomReader
        with GedcomReader(path) as parser:
            data = []
            for indi in parser.records0("INDI"):
                death_tag = indi.sub_tag("DEAT")
                death_date = indi.sub_tag_value("DEAT/DATE")
                death_place = indi.sub_tag_value("DEAT/PLAC")
                death_reason = indi.sub_tag_value("DEAT/CAUSE")
                print(death_reason)
                death_note = ""
                death_src = ""

                # Notes and sources can be multiple, so collect them
                if death_tag is not None:
                    notes = [note.value for note in death_tag.sub_tags("NOTE")]
                    death_note = "\n".join(notes) if notes else ""
                    sources = [src.value for src in death_tag.sub_tags("SOUR")]
                    death_src = "\n".join(sources) if sources else ""

                    if death_date:
                        death_status = DeathStatus.DEAD
                    else:
                        death_status = DeathStatus.DONT_KNOW_IF_DEAD
                else:
                    death_status = DeathStatus.NOT_DEAD
                data.append({
                    "type": "INDI",
                    "name": indi.name.first,
                    "surname": indi.name.surname,
                    "birth": indi.sub_tag_value("BIRT/DATE"),
                    "birth_place": indi.sub_tag_value("BIRT/PLAC"),
                    "sex": indi.sub_tag_value("SEX"),
                    "occupation": [occu.value for occu in indi.sub_tags("OCCU")],
                    "notes": [note.value for note in indi.sub_tags("NOTE")],
                    "aliases": [alia.value for alia in indi.sub_tags("ALIA")],
                    "death_status": death_status,
                    "death_date": death_date,
                    "death_place": death_place,
                    "death_reason": death_reason,
                    "death_note": death_note,
                    "death_src": death_src,
                })
            return data
    except Exception as e:
        print(f"[ged4py] Failed: {e}")
        return None


def fallback_parse(path: str) -> list:
    """Fallback parser that builds a tree structure from any GEDCOM format."""
    with open(path, encoding="utf-8", errors="ignore") as f:
        lines = [line.strip() for line in f if line.strip()]

    tree, stack = [], []
    for line in lines:
        parts = line.split(" ", 2)
        if len(parts) < 2:
            continue
        level = int(parts[0])
        tag = parts[1]
        data = parts[2] if len(parts) > 2 else ""
        node = {"level": level, "tag": tag, "data": data, "children": []}

        while stack and stack[-1]["level"] >= level:
            stack.pop()

        if stack:
            stack[-1]["children"].append(node)
        else:
            tree.append(node)
        stack.append(node)

    return tree


def parse_gedcom_universal(path: str) -> dict:
    version = detect_gedcom_version(path)
    print(f"Detected GEDCOM version: {version}")

    # 5.5 — try python-gedcom
    if version.startswith("5.5") and not version.startswith("5.5.1"):
        try:
            from gedcom.parser import Parser
            from gedcom.element.individual import IndividualElement
            parser = Parser()
            parser.parse_file(path)
            data = []
            for element in parser.get_root_child_elements():
                if isinstance(element, IndividualElement):
                    data.append({
                        "name": element.get_name()[0],
                        "surname": element.get_name()[1],
                        "birth": element.get_birth_data(),
                        "birth_place": element.get_birth_place(),
                        "death": element.get_death_data(),
                        "death_place": element.get_death_place(),
                        "sex": element.get_gender(),
                        "occupation": element.get_occupation(),
                        "notes": element.get_notes(),
                        "aliases": element.get_aliases(),
                        # Add other fields as needed
                    })
            return {
                "version": version,
                "data": data,
                "method": "python-gedcom"
            }
        except Exception as e:
            print(f"[python-gedcom] Failed: {e}")

    # 5.5.1 and tolerant fallback
    data = parse_with_ged4py(path)
    if data:
        return {"version": version, "data": data, "method": "ged4py"}

    # 7.0
    if version.startswith("7"):
        try:
            import gedcom7
            with open(path, "r", encoding="utf-8") as f:
                string = f.read()
            doc = gedcom7.loads(string)
            data = []
            for r in doc.records:
                if r.tag == "INDI":
                    indi_dict = r.to_dict()
                    data.append({
                        "name": indi_dict.get("NAME"),
                        "birth": indi_dict.get("BIRT", {}).get("DATE"),
                        "birth_place": indi_dict.get("BIRT", {}).get("PLAC"),
                        "death": indi_dict.get("DEAT", {}).get("DATE"),
                        "death_place": indi_dict.get("DEAT", {}).get("PLAC"),
                        "sex": indi_dict.get("SEX"),
                        "occupation": indi_dict.get("OCCU"),
                        "notes": indi_dict.get("NOTE"),
                        "aliases": indi_dict.get("ALIA"),
                        # Add other fields as needed
                    })
            return {
                "version": version,
                "data": data,
                "method": "gedcom7"
            }
        except Exception as e:
            print(f"[gedcom7] Failed: {e}")

    # fallback parser for malformed files
    return {
        "version": version,
        "data": fallback_parse(path),
        "method": "fallback"
    }


def remove_temp_file(path: str) -> None:
    try:
        os.remove(path)
    except OSError as e:
        print(f"Error deleting temporary file {path}: {e}")


def clean_gedcom_file(input_file: str) -> str:
    with tempfile.NamedTemporaryFile(
        mode="w",
        delete=False,
        suffix=".ged",
        encoding="utf-8"
    ) as tmp:
        for line in open(input_file, encoding="utf-8", errors="ignore"):
            if line.strip():
                tmp.write(line)
        return tmp.name


def parse_gedcom(path: str) -> dict:
    clean_file = clean_gedcom_file(path)
    result = parse_gedcom_universal(clean_file)
    remove_temp_file(clean_file)
    return result


if __name__ == "__main__":
    path = "washington.ged"
    clean_file = clean_gedcom_file(path)
    result = parse_gedcom_universal(clean_file)
    remove_temp_file(clean_file)
    print(f"Parsing method: {result['method']}")
    print(f"Data: {result['data'][:10]}...")
