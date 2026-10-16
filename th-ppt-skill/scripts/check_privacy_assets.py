#!/usr/bin/env python3
"""Fail when distributable PPT-skill files contain common secret or PNG metadata carriers."""

from __future__ import annotations

from pathlib import Path
import re
import struct
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = ROOT / "th-ppt-skill"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
FORBIDDEN_PNG_CHUNKS = {b"caBX", b"eXIf", b"iTXt", b"tEXt", b"zTXt"}
TEXT_FILE_SUFFIXES = {".md", ".yaml", ".yml", ".svg"}
SECRET_PATTERNS = (
    re.compile(r"(?i)\b(?:api[_-]?key|client[_-]?secret|private[_-]?key|password|passwd)\b\s*[:=]\s*[^\s<]{8,}"),
    re.compile(r"(?i)\bauthorization\s*:\s*bearer\s+[A-Za-z0-9._~+/-]{16,}"),
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
)


def png_chunks(path: Path):
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("not a PNG file")
    offset = len(PNG_SIGNATURE)
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError("truncated PNG chunk")
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        end = offset + length + 12
        if end > len(data):
            raise ValueError("truncated PNG payload")
        chunk_type = data[offset + 4 : offset + 8]
        payload = data[offset + 8 : offset + 8 + length]
        stored_crc = struct.unpack(">I", data[offset + 8 + length : end])[0]
        if (zlib.crc32(chunk_type + payload) & 0xFFFFFFFF) != stored_crc:
            raise ValueError(f"invalid PNG CRC in {chunk_type.decode('ascii', 'replace')}")
        yield chunk_type
        offset = end
        if chunk_type == b"IEND":
            if offset != len(data):
                raise ValueError("unexpected bytes after IEND")
            return
    raise ValueError("missing IEND chunk")


def main() -> int:
    failures: list[str] = []
    for path in sorted((SKILL_ROOT / "assets").rglob("*.png")):
        try:
            forbidden = sorted(
                chunk.decode("ascii", "replace")
                for chunk in png_chunks(path)
                if chunk in FORBIDDEN_PNG_CHUNKS
            )
        except ValueError as error:
            failures.append(f"{path.relative_to(ROOT)}: {error}")
            continue
        if forbidden:
            failures.append(f"{path.relative_to(ROOT)}: forbidden PNG metadata chunks: {', '.join(forbidden)}")

    for path in sorted(SKILL_ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_FILE_SUFFIXES:
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if any(pattern.search(line) for pattern in SECRET_PATTERNS):
                failures.append(f"{path.relative_to(ROOT)}:{line_number}: possible credential or email")

    if failures:
        print("Privacy asset check failed:", file=sys.stderr)
        print("\n".join(f"- {failure}" for failure in failures), file=sys.stderr)
        return 1
    print("Privacy asset check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
