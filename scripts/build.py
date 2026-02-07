import os
import shutil
from pathlib import Path
import sys

import PyInstaller.__main__

ROOT = Path(__file__).resolve().parent.parent
MAIN_FILE = ROOT / "app.py"
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"
sys.path.insert(0, str(ROOT))
from core.version_info import VERSION
APP_NAME = "RandPicker"
APP_VERSION = str(VERSION)

DATA_MAPPINGS = [
    ("src", "src"),
    ("assets", "assets"),
    ("lib", "lib")
]


def _clean_outputs():
    for path in (DIST_DIR, BUILD_DIR):
        if path.exists():
            shutil.rmtree(path)


def _add_data_args():
    for rel_path, target in DATA_MAPPINGS:
        src = ROOT / rel_path
        if src.exists():
            yield f"--add-data={src}{os.pathsep}{target}"


def _get_icon(platform_key: str) -> Path | None:
    candidates = {
        "windows": [ROOT / "assets" / "icon-dark.ico", ROOT / "assets" / "icon-dark.png", ROOT / "assets" / "icon-dark.jpg"],
        "mac": [ROOT / "assets" / "icon-dark.icns", ROOT / "assets" / "icon-dark.png", ROOT / "assets" / "icon-dark.jpg"],
        "linux": [ROOT / "assets" / "icon-dark.jpg", ROOT / "assets" / "icon-dark.png", ROOT / "assets" / "icon-dark.ico"],
    }
    for path in candidates.get(platform_key, []):
        if path.exists():
            return path
    return None


def _resolve_platform(key: str | None = None) -> str:
    if key:
        key = key.lower()
        if key.startswith("win"):
            return "windows"
        if key in ("mac", "darwin", "osx"):
            return "mac"
    if sys.platform.startswith("win"):
        return "windows"
    if sys.platform == "darwin":
        return "mac"
    return sys.platform


def _platform_args(platform_key: str) -> list[str]:
    args: list[str] = []
    icon = _get_icon(platform_key)
    if icon:
        args.append(f"--icon={icon}")

    if platform_key == "windows":
        args.extend([
            "--onedir",
            "--windowed",
            "--contents-directory=.",
        ])
    elif platform_key == "mac":
        args.extend([
            "--onedir",
            "--windowed",
            f"--osx-bundle-identifier=com.randpicker.{APP_NAME.lower()}",
        ])
    elif platform_key.startswith("linux"):
        args.extend([
            "--onedir",
            "--windowed",
        ])
    return args


def _version_numbers() -> tuple[int, int, int, int]:
    parts = list(VERSION.release)
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


def _write_unix_version_file(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"name={APP_NAME}\nversion={APP_VERSION}\n"
    path.write_text(content, encoding="utf-8")
    return path


def build(platform_key: str, name: str = APP_NAME):
    if not MAIN_FILE.exists():
        raise FileNotFoundError("Missing app.py entry point")

    args = [
        str(MAIN_FILE),
        "--noconfirm",
        "--clean",
        f"--distpath={DIST_DIR}",
        f"--workpath={BUILD_DIR}",
        f"--name={name}",
    ]
    args = [a for a in args if a]

    if platform_key == "windows":
        version_file = _write_win_version_file(BUILD_DIR / "version.txt")
        args.append(f"--version-file={version_file}")
    elif platform_key == "mac":
        meta_file = _write_unix_version_file(BUILD_DIR / "mac_version.txt")
        args.append(f"--add-data={meta_file}{os.pathsep}.")
    elif platform_key.startswith("linux"):
        meta_file = _write_unix_version_file(BUILD_DIR / "linux_version.txt")
        args.append(f"--add-data={meta_file}{os.pathsep}.")

    args.extend(_platform_args(platform_key))
    args.extend(_add_data_args())
    PyInstaller.__main__.run(args)


if __name__ == "__main__":
    # Always clean before building
    _clean_outputs()
    platform_key = _resolve_platform()
    build(platform_key=platform_key, name=APP_NAME)
