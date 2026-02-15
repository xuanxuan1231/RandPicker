"""
Pre-build script for RandPicker.
Handles pre-packaging file processing including:
- Writing Windows platform version metadata files
- Cleaning build directories
"""

import os
import shutil
import sys
from pathlib import Path

# Setup paths
ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = ROOT / "build"
DIST_DIR = ROOT / "dist"

# Import VERSION directly to avoid full module dependencies
version_file = ROOT / "core" / "version_info.py"
VERSION = None
with open(version_file) as f:
    import re
    for line in f:
        # Match: VERSION = Version("x.y.z")
        match = re.search(r'VERSION\s*=\s*Version\s*\(\s*["\']([^"\']+)["\']\s*\)', line)
        if match:
            VERSION = match.group(1)
            break

if VERSION is None:
    VERSION = "0.0.0"

APP_NAME = "RandPicker"
APP_VERSION = VERSION


def _version_numbers() -> tuple[int, int, int, int]:
    """Extract version numbers from VERSION string."""
    try:
        # VERSION is already a string like "2.0.0"
        parts = [int(p) for p in VERSION.split('.') if p.isdigit()]
    except Exception:
        parts = [0, 0, 0, 0]

    while len(parts) < 4:
        parts.append(0)
    return tuple(parts[:4])


def write_win_version_file(path: Path) -> Path:
    """Write Windows version metadata file for PyInstaller."""
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
    print(f"Windows version file created at: {path}")
    return path


def write_unix_version_file(path: Path) -> Path:
    """
    Write Unix/Linux/Mac version metadata file.
    
    Creates a simple key-value format file:
        name=<APP_NAME>
        version=<APP_VERSION>
    
    This file is bundled with the application and can be read at runtime.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"name={APP_NAME}\nversion={APP_VERSION}\n"
    path.write_text(content, encoding="utf-8")
    print(f"Unix version file created at: {path}")
    return path


def clean_outputs():
    """Clean build and dist directories."""
    for path in (DIST_DIR, BUILD_DIR):
        if path.exists():
            print(f"Cleaning {path}...")
            shutil.rmtree(path)


def main():
    """Main pre-build process."""
    print("=" * 60)
    print("RandPicker Pre-Build Script")
    print("=" * 60)
    
    # Clean old build artifacts
    clean_outputs()
    
    # Create build directory
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    
    # Detect platform
    platform = sys.platform
    print(f"Platform: {platform}")
    print(f"App Version: {APP_VERSION}")
    
    # Create version files based on platform
    if platform.startswith("win"):
        print("\nCreating Windows version metadata...")
        write_win_version_file(BUILD_DIR / "version.txt")
    elif platform == "darwin":
        print("\nCreating macOS version metadata...")
        write_unix_version_file(BUILD_DIR / "mac_version.txt")
    elif platform.startswith("linux"):
        print("\nCreating Linux version metadata...")
        write_unix_version_file(BUILD_DIR / "linux_version.txt")
    
    print("\nPre-build process completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
