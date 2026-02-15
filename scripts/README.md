# Build Scripts Documentation

This directory contains modular build scripts for RandPicker.

## Scripts Overview

### 1. pre_build.py
**Purpose:** Pre-packaging file processing
- Cleans old build artifacts (build/ and dist/ directories)
- Creates platform-specific version metadata files:
  - Windows: `build/version.txt` (PyInstaller version-file format)
  - macOS: `build/mac_version.txt`
  - Linux: `build/linux_version.txt`

**Usage:**
```bash
python scripts/pre_build.py
```

### 2. pyinstaller_args.py
**Purpose:** Generate PyInstaller command-line arguments
- Detects the current platform
- Generates appropriate PyInstaller arguments including:
  - Icon paths
  - Data file mappings (src, assets, lib)
  - Platform-specific options (--windowed, --onedir, etc.)
  - Version metadata files

**Usage:**
```bash
# Print PyInstaller arguments
python scripts/pyinstaller_args.py

# Use with PyInstaller (Unix/Linux/macOS)
pyinstaller $(python scripts/pyinstaller_args.py)

# Use with PyInstaller (Windows PowerShell)
$args = python scripts/pyinstaller_args.py
pyinstaller $args
```

### 3. post_build.py
**Purpose:** Post-packaging file processing
- **Linux only:** Builds .deb packages for Debian/Ubuntu
  - Creates proper directory structure (/opt, /usr/bin, /usr/share)
  - Generates DEBIAN/control file
  - Creates desktop entry (.desktop file)
  - Copies application icon
  - Creates symbolic link in /usr/bin
  - Builds the final .deb package using dpkg-deb

**Usage:**
```bash
python scripts/post_build.py
```

### 4. build.py (Legacy)
**Purpose:** Backwards-compatible wrapper
- Provides compatibility with the old build system
- Runs the three modular scripts in sequence
- **Deprecated:** Use the modular scripts or GitHub Actions workflow instead

**Usage:**
```bash
python scripts/build.py
```

## Build Workflow

### Manual Build (Recommended)
```bash
# 1. Pre-build processing
python scripts/pre_build.py

# 2. Build with PyInstaller
pyinstaller $(python scripts/pyinstaller_args.py)

# 3. Post-build processing
python scripts/post_build.py
```

### Legacy Build (Backwards Compatible)
```bash
python scripts/build.py
```

### GitHub Actions Workflow
The GitHub Actions workflow (`.github/workflows/build.yml`) automatically:
1. Runs `pre_build.py` to prepare build environment
2. Executes PyInstaller directly with arguments from `pyinstaller_args.py`
3. Runs `post_build.py` for platform-specific packaging
4. Creates platform-specific archives (ZIP for Windows, DMG for macOS, DEB for Linux)

## Platform-Specific Notes

### Windows
- Version metadata is embedded in the executable via `--version-file`
- Icon format: .ico
- Output: One-directory bundle with contents in current directory

### macOS
- Version metadata included as data file
- Icon format: .icns
- Output: .app bundle
- Supports both Intel (x64) and Apple Silicon (arm64)

### Linux (Debian)
- Version metadata included as data file
- Icon format: .png (preferred), .jpg (fallback)
- Output: One-directory bundle + .deb package
- .deb package follows Debian packaging standards

## Requirements

- Python 3.12+
- PyInstaller
- Platform-specific dependencies (see `.github/workflows/build.yml`)

## Version Management

All scripts read the version from `core/version_info.py`:
```python
VERSION = Version("2.0.0")
```

The version is automatically extracted without importing the full module to avoid dependency issues during build.
