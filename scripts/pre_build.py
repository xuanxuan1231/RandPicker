import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.version_info import VERSION

APP_NAME = "RandPicker"
APP_VERSION = str(VERSION)

def _version_numbers() -> tuple[int, int, int, int]:
    try:
        if hasattr(VERSION, 'release'):
            parts = list(VERSION.release)
        else:
            parts = [int(p) for p in str(VERSION).split('.') if p.isdigit()]
    except Exception:
        parts = [0, 0, 0, 0]

    while len(parts) < 4:
        parts.append(0)
    return tuple(parts[:4])

def _write_win_version_file(path: Path) -> Path:
    nums = _version_numbers()
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"""VSVersionInfo(
    ffi=FixedFileInfo(
        filevers={nums},
        prodvers={nums},
        mask=0x3f,
        flags=0x0,
        OS=0x4,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo([
            StringTable(
                '040904B0',
                [
                    StringStruct('CompanyName', ''),
                    StringStruct('FileDescription', '{APP_NAME}'),
                    StringStruct('FileVersion', '{APP_VERSION}'),
                    StringStruct('InternalName', '{APP_NAME}'),
                    StringStruct('LegalCopyright', ''),
                    StringStruct('OriginalFilename', '{APP_NAME}.exe'),
                    StringStruct('ProductName', '{APP_NAME}'),
                    StringStruct('ProductVersion', '{APP_VERSION}')
                ]
            )
        ]),
        VarFileInfo([VarStruct('Translation', [1033, 1200])])
    ]
)
"""
    path.write_text(content, encoding="utf-8")
    return path

if __name__ == "__main__":
    if sys.platform == "win32":
        _write_win_version_file(ROOT / "version.txt")
