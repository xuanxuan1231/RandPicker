"""
Post-build script for RandPicker.
Handles post-packaging file processing including:
- Building .deb packages for Debian/Ubuntu
- Additional packaging tasks
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Setup paths
ROOT = Path(__file__).resolve().parent.parent
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
PKG_NAME = APP_NAME.lower()
APP_VERSION = VERSION


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


def build_deb(dist_app_dir: Path):
    """Build .deb package for Debian/Ubuntu (Class-Widgets style)."""
    print("\n" + "=" * 60)
    print("Building .deb package...")
    print("=" * 60)
    
    pkg_name = PKG_NAME
    deb_dir = BUILD_DIR / "deb"
    if deb_dir.exists():
        shutil.rmtree(deb_dir)

    # 1. Create directory structure
    opt_dir = deb_dir / "opt" / pkg_name
    bin_dir = deb_dir / "usr" / "bin"
    share_dir = deb_dir / "usr" / "share"
    apps_dir = share_dir / "applications"
    icons_dir = share_dir / "icons" / "hicolor" / "256x256" / "apps"
    debian_meta_dir = deb_dir / "DEBIAN"

    for d in [opt_dir, bin_dir, apps_dir, icons_dir, debian_meta_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # 2. Copy build artifacts
    print(f"Copying build artifacts from {dist_app_dir} to {opt_dir}...")
    shutil.copytree(dist_app_dir, opt_dir, dirs_exist_ok=True)

    # 3. Calculate Installed-Size (in KB)
    installed_size = 0
    for p in deb_dir.rglob('*'):
        if p.is_file():
            installed_size += p.stat().st_size
    installed_size_kb = installed_size // 1024
    print(f"Calculated installed size: {installed_size_kb} KB")

    # 4. Create DEBIAN/control
    control_content = f"""Package: {pkg_name}
Version: {APP_VERSION}
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Manus App <manus-app@manus.im>
Installed-Size: {installed_size_kb}
Depends: libglib2.0-0, libdbus-1-3, libxcb1, libx11-6
Description: {APP_NAME} random picker application.
 RandPicker is a simple and beautiful random picker application.
"""
    (debian_meta_dir / "control").write_text(control_content, encoding="utf-8")
    print("Created DEBIAN/control file")

    # 5. Create desktop entry
    desktop_content = f"""[Desktop Entry]
Name={APP_NAME}
Exec=/usr/bin/{pkg_name}
Icon={pkg_name}
Type=Application
Categories=Utility;
Comment=A random picker application.
Terminal=false
"""
    (apps_dir / f"{pkg_name}.desktop").write_text(desktop_content, encoding="utf-8")
    print("Created desktop entry file")

    # 6. Copy icon
    icon_src = get_icon("linux")
    if icon_src:
        shutil.copy(icon_src, icons_dir / f"{pkg_name}{icon_src.suffix}")
        print(f"Copied icon: {icon_src.name}")

    # 7. Create /usr/bin symlink
    executable_link = bin_dir / pkg_name
    target_rel = Path(f"../../opt/{pkg_name}/{APP_NAME}")
    os.symlink(target_rel, executable_link)
    print(f"Created symlink: {executable_link} -> {target_rel}")

    # 8. Build the package
    output_deb = DIST_DIR / f"{pkg_name}_{APP_VERSION}_amd64.deb"
    print(f"\nBuilding .deb package: {output_deb}")
    subprocess.run(["dpkg-deb", "--build", str(deb_dir), str(output_deb)], check=True)
    print(f"✓ .deb package built successfully at {output_deb}")
    print("=" * 60)


def main():
    """Main post-build process."""
    print("=" * 60)
    print("RandPicker Post-Build Script")
    print("=" * 60)
    
    # Detect platform
    platform = sys.platform
    print(f"Platform: {platform}")
    print(f"App Version: {APP_VERSION}")
    
    # Check if dist directory exists
    if not DIST_DIR.exists():
        print(f"Error: Dist directory not found at {DIST_DIR}")
        sys.exit(1)
    
    # For Linux, build .deb package
    if platform.startswith("linux"):
        dist_app_dir = DIST_DIR / APP_NAME
        if not dist_app_dir.exists():
            print(f"Error: App directory not found at {dist_app_dir}")
            sys.exit(1)
        
        build_deb(dist_app_dir)
    else:
        print(f"\nNo post-build tasks for platform: {platform}")
    
    print("\nPost-build process completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
