"""Preview or apply a Multi Commander colour or keyboard preset."""

from argparse import ArgumentParser
from copy import deepcopy
from datetime import datetime, timezone
import difflib
from io import BytesIO
import os
from pathlib import Path
import re
import tempfile
import xml.etree.ElementTree as ET


PRESETS = Path(__file__).resolve().parent / "presets"


def merge_colours(target: ET.Element, preset: ET.Element) -> None:
    target.attrib.update(preset.attrib)
    for item in preset:
        existing = target.find(item.tag)
        if existing is None:
            target.append(deepcopy(item))
        else:
            merge_colours(existing, item)


def apply_f1(root: ET.Element) -> None:
    binding = ET.parse(PRESETS / "f1-rename.xml").getroot().find("map")
    matches = [
        item for item in root.findall("map")
        if item.get("key", "").upper() == "F1"
        and not item.get("keymod", "")
        and (item.get("extid"), item.get("ctrl", "0")) == (binding.get("extid"), binding.get("ctrl"))
    ]
    if len(matches) == 1 and matches[0].attrib == binding.attrib:
        return
    if matches:
        position = list(root).index(matches[0])
        for item in matches:
            root.remove(item)
        root.insert(position, binding)
    else:
        root.append(binding)


def xml_bytes(root: ET.Element, original: bytes) -> bytes:
    # Keep the document's encoding and do not change its version/build attributes.
    declaration = re.match(rb'<\?xml[^>]*encoding=["\']([^"\']+)', original.lstrip(b"\xef\xbb\xbf"))
    encoding = declaration.group(1).decode("ascii") if declaration else "utf-8"
    if original.startswith((b"\xff\xfe", b"\xfe\xff")):
        encoding = "utf-16"
    elif original.startswith(b"\xef\xbb\xbf") and encoding.lower() == "utf-8":
        encoding = "utf-8-sig"
    ET.indent(root, space="  ")
    output = BytesIO()
    ET.ElementTree(root).write(output, encoding=encoding, xml_declaration=True)
    return output.getvalue()


def write_with_backup(target: Path, original: bytes | None, updated: bytes) -> Path | None:
    temporary = None
    backup = None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(updated)
        if original is not None:
            if target.read_bytes() != original:
                raise OSError("Configuration changed while preparing the preset. Run it again.")
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            backup = target.with_name(f"{target.name}.{stamp}.bak")
            with backup.open("xb") as handle:
                handle.write(original)
            os.replace(temporary, target)
        else:
            # Exclusive creation ensures a config created in the meantime is preserved.
            with target.open("xb") as handle:
                handle.write(updated)
        return backup
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("preset", choices=("soft-gray", "f1-rename"))
    parser.add_argument("--config-dir", type=Path, metavar="DIR")
    parser.add_argument("--apply", action="store_true", help="write the preset and back up the existing file")
    args = parser.parse_args()

    appdata = os.environ.get("APPDATA")
    config_dir = args.config_dir or (Path(appdata) / "MultiCommander/Config" if appdata else None)
    if config_dir is None or not config_dir.is_dir():
        parser.error("Pass --config-dir with the existing Multi Commander Config directory.")

    filename = "ExplorerPanel.xml" if args.preset == "soft-gray" else "CustomKeymappings.xml"
    target = config_dir / filename
    try:
        original = None if args.preset == "f1-rename" and not target.exists() else target.read_bytes()
        xml_parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True, insert_pis=True))
        root = ET.fromstring(original, parser=xml_parser) if original is not None else ET.Element("keymap")
        expected_tag = "config" if args.preset == "soft-gray" else "keymap"
        if root.tag != expected_tag:
            raise ValueError(f"Unexpected XML root {root.tag!r} in {target.name}.")

        before = xml_bytes(deepcopy(root), original or b"")
        if args.preset == "soft-gray":
            colours = root.find("colors")
            if colours is None:
                colours = ET.SubElement(root, "colors")
            merge_colours(colours, ET.parse(PRESETS / "soft-gray.xml").getroot())
        else:
            apply_f1(root)
        after = xml_bytes(root, original or b"")

        if before == after and original is not None:
            print(f"Already applied: {target}")
            return
        if args.apply:
            backup = write_with_backup(target, original, after)
            print(f"Updated: {target}")
            if backup:
                print(f"Backup: {backup}")
        else:
            print(f"Preview: {target}")
            for line in difflib.diff_bytes(difflib.unified_diff, before.splitlines(), after.splitlines()):
                print(line.decode("ascii", errors="backslashreplace"))
    except (OSError, ET.ParseError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
