import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"

sys.path.insert(0, str(ROOT))
from core.version_info import VERSION

APP_NAME = "RandPicker"
PKG_NAME = APP_NAME.lower()
APP_VERSION = str(VERSION)


def _resolve_platform() -> str:
    if sys.platform.startswith("win"):
        return "windows"
    if sys.platform == "darwin":
        return "mac"
    return "linux"


def _get_icon() -> Path | None:
    candidates = [
        ROOT / "assets" / "icon-dark.png",
        ROOT / "assets" / "icon-dark.jpg",
        ROOT / "assets" / "icon-dark.ico",
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def _remove_if_exists(path: Path) -> None:
    if path.exists():
        path.unlink()


def build_deb(dist_app_dir: Path) -> None:
    """构建 .deb 软件包，参考 build.py 的 Class-Widgets 风格"""
    print("Starting .deb package build (Class-Widgets style)...")
    deb_dir = BUILD_DIR / "deb"
    if deb_dir.exists():
        shutil.rmtree(deb_dir)

    opt_dir = deb_dir / "opt" / PKG_NAME
    bin_dir = deb_dir / "usr" / "bin"
    share_dir = deb_dir / "usr" / "share"
    apps_dir = share_dir / "applications"
    icons_dir = share_dir / "icons" / "hicolor" / "256x256" / "apps"
    debian_meta_dir = deb_dir / "DEBIAN"

    for d in [opt_dir, bin_dir, apps_dir, icons_dir, debian_meta_dir]:
        d.mkdir(parents=True, exist_ok=True)

    shutil.copytree(dist_app_dir, opt_dir, dirs_exist_ok=True)

    installed_size = 0
    for p in deb_dir.rglob("*"):
        if p.is_file():
            installed_size += p.stat().st_size
    installed_size_kb = installed_size // 1024

    control_content = f"""Package: {PKG_NAME}
Version: {APP_VERSION}
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Wenxuan Shen <bushigemen114@gmail.com>
Installed-Size: {installed_size_kb}
Depends: libglib2.0-0, libdbus-1-3, libxcb1, libx11-6
Description: {APP_NAME} random picker application.
 RandPicker is a simple and beautiful random picker application.
"""
    (debian_meta_dir / "control").write_text(control_content, encoding="utf-8")

    desktop_content = f"""[Desktop Entry]
Name={APP_NAME}
Exec=/usr/bin/{PKG_NAME}
Icon={PKG_NAME}
Type=Application
Categories=Utility;
Comment=A random picker application.
Terminal=false
"""
    (apps_dir / f"{PKG_NAME}.desktop").write_text(desktop_content, encoding="utf-8")

    icon_src = _get_icon()
    if icon_src:
        shutil.copy(icon_src, icons_dir / f"{PKG_NAME}{icon_src.suffix}")

    executable_link = bin_dir / PKG_NAME
    target_rel = Path(f"../../opt/{PKG_NAME}/{APP_NAME}")
    os.symlink(target_rel, executable_link)

    output_deb = DIST_DIR / f"{PKG_NAME}_{APP_VERSION}_amd64.deb"
    subprocess.run(["dpkg-deb", "--build", str(deb_dir), str(output_deb)], check=True)
    print(f".deb package built at {output_deb}")


def _post_build_windows() -> None:
    _remove_if_exists(ROOT / "version.txt")


def _post_build_linux() -> None:
    dist_app_dir = DIST_DIR / APP_NAME
    if not dist_app_dir.exists():
        raise FileNotFoundError(f"Missing dist app dir at {dist_app_dir}")
    build_deb(dist_app_dir)


def main() -> None:
    platform_key = _resolve_platform()
    if platform_key == "windows":
        _post_build_windows()
    elif platform_key == "linux":
        _post_build_linux()


if __name__ == "__main__":
    main()

