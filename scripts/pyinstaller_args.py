"""
Generate PyInstaller arguments for building RandPicker.
This script outputs PyInstaller command-line arguments to stdout,
which can be used by the build workflow.
"""

import os
import sys
from pathlib import Path

# Setup paths
ROOT = Path(__file__).resolve().parent.parent
MAIN_FILE = ROOT / "app.py"
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"

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

DATA_MAPPINGS = [
    ("src", "src"),
    ("assets", "assets"),
    ("lib", "lib")
]


def get_icon(platform_key: str) -> Path | None:
    """Get icon path for specified platform."""
    candidates = {
        "windows": [ROOT / "assets" / "icon-dark.ico", ROOT / "assets" / "icon-dark.png",
                    ROOT / "assets" / "icon-dark.jpg"],
        "mac": [ROOT / "assets" / "icon-dark.icns", ROOT / "assets" / "icon-dark.png",
                ROOT / "assets" / "icon-dark.jpg"],
        "linux": [ROOT / "assets" / "icon-dark.png", ROOT / "assets" / "icon-dark.jpg",
                  ROOT / "assets" / "icon-dark.ico"],
    }
    for path in candidates.get(platform_key, []):
        if path.exists():
            return path
    return None


def resolve_platform(key: str | None = None) -> str:
    """Resolve platform key from argument or system platform."""
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
    return "linux"


def add_data_args():
    """Generate --add-data arguments for PyInstaller."""
    for rel_path, target in DATA_MAPPINGS:
        src = ROOT / rel_path
        if src.exists():
            yield f"--add-data={src}{os.pathsep}{target}"


def platform_args(platform_key: str) -> list[str]:
    """Generate platform-specific PyInstaller arguments."""
    args: list[str] = []
    icon = get_icon(platform_key)
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
    elif platform_key == "linux":
        args.extend([
            "--onedir",
            "--windowed",
        ])
    return args


def generate_args(platform_key: str | None = None) -> list[str]:
    """Generate complete PyInstaller arguments."""
    if not MAIN_FILE.exists():
        raise FileNotFoundError(f"Missing app.py entry point at {MAIN_FILE}")

    platform_key = resolve_platform(platform_key)
    
    args = [
        str(MAIN_FILE),
        "--noconfirm",
        "--clean",
        f"--distpath={DIST_DIR}",
        f"--workpath={BUILD_DIR}",
        f"--name={APP_NAME}",
    ]

    # Add version file for Windows
    if platform_key == "windows":
        version_file = BUILD_DIR / "version.txt"
        if version_file.exists():
            args.append(f"--version-file={version_file}")
    # Add version metadata for Unix-like systems
    elif platform_key == "mac":
        meta_file = BUILD_DIR / "mac_version.txt"
        if meta_file.exists():
            args.append(f"--add-data={meta_file}{os.pathsep}.")
    elif platform_key == "linux":
        meta_file = BUILD_DIR / "linux_version.txt"
        if meta_file.exists():
            args.append(f"--add-data={meta_file}{os.pathsep}.")

    # Add platform-specific arguments
    args.extend(platform_args(platform_key))
    
    # Add data mappings
    for data_arg in add_data_args():
        args.append(data_arg)

    return args


def main():
    """Generate and print PyInstaller arguments."""
    platform = sys.argv[1] if len(sys.argv) > 1 else None
    args = generate_args(platform)
    
    # Print each argument on a separate line for easy parsing
    for arg in args:
        print(arg)


if __name__ == "__main__":
    main()
