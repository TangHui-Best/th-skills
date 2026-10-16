#!/usr/bin/env python3
"""Remove nonessential PNG metadata while preserving raster chunks byte-for-byte."""

from __future__ import annotations

import argparse
from pathlib import Path
import struct
import zlib

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
METADATA_CHUNKS = {b"caBX", b"eXIf", b"iTXt", b"tEXt", b"zTXt"}


def chunks(data: bytes):
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("not a PNG file")
    offset = len(PNG_SIGNATURE)
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError("truncated PNG chunk")
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        end = offset + 12 + length
        if end > len(data):
            raise ValueError("truncated PNG payload")
        chunk_type = data[offset + 4 : offset + 8]
        payload = data[offset + 8 : offset + 8 + length]
        expected_crc = struct.unpack(">I", data[offset + 8 + length : end])[0]
        actual_crc = zlib.crc32(chunk_type + payload) & 0xFFFFFFFF
        if actual_crc != expected_crc:
            raise ValueError(f"invalid PNG CRC in {chunk_type.decode('ascii', 'replace')}")
        yield chunk_type, payload
        offset = end
        if chunk_type == b"IEND":
            if offset != len(data):
                raise ValueError("unexpected bytes after IEND")
            return
    raise ValueError("missing IEND chunk")


def sanitize(path: Path) -> list[str]:
    retained = bytearray(PNG_SIGNATURE)
    removed: list[str] = []
    for chunk_type, payload in chunks(path.read_bytes()):
        if chunk_type in METADATA_CHUNKS:
            removed.append(chunk_type.decode("ascii"))
            continue
        retained.extend(struct.pack(">I", len(payload)))
        retained.extend(chunk_type)
        retained.extend(payload)
        retained.extend(struct.pack(">I", zlib.crc32(chunk_type + payload) & 0xFFFFFFFF))
    path.write_bytes(retained)
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    for path in args.files:
        removed = sanitize(path)
        print(f"{path}: removed {', '.join(removed) if removed else 'no metadata chunks'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
