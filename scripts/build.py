import os
import shutil
from pathlib import Path
import sys
import subprocess

import PyInstaller.__main__

ROOT = Path(__file__).resolve().parent.parent
MAIN_FILE = ROOT / "app.py"
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"
sys.path.insert(0, str(ROOT))
from core.version_info import VERSION

APP_NAME = "RandPicker"
PKG_NAME = APP_NAME.lower()
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
            yield f"{src}{os.pathsep}{target}"


def _get_icon(platform_key: str) -> Path | None:
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
    return "linux"


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
    elif platform_key == "linux":
        args.extend([
            "--onedir",
            "--windowed",
        ])
    return args


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


def _write_unix_version_file(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"name={APP_NAME}\\nversion={APP_VERSION}\\n"
    path.write_text(content, encoding="utf-8")
    return path


def build_deb(dist_app_dir: Path):
    """构建 .deb 软件包，参考 Class-Widgets 标准"""
    print("Starting .deb package build (Class-Widgets style)...")
    pkg_name = PKG_NAME
    deb_dir = BUILD_DIR / "deb"
    if deb_dir.exists():
        shutil.rmtree(deb_dir)

    # 1. 创建目录结构
    opt_dir = deb_dir / "opt" / pkg_name
    bin_dir = deb_dir / "usr" / "bin"
    share_dir = deb_dir / "usr" / "share"
    apps_dir = share_dir / "applications"
    icons_dir = share_dir / "icons" / "hicolor" / "256x256" / "apps"
    debian_meta_dir = deb_dir / "DEBIAN"

    for d in [opt_dir, bin_dir, apps_dir, icons_dir, debian_meta_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # 2. 拷贝构建产物
    shutil.copytree(dist_app_dir, opt_dir, dirs_exist_ok=True)

    # 3. 计算 Installed-Size (单位 KB)
    installed_size = 0
    for p in deb_dir.rglob('*'):
        if p.is_file():
            installed_size += p.stat().size
    installed_size_kb = installed_size // 1024

    # 4. 创建 DEBIAN/control
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

    # 5. 创建桌面快捷方式
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

    # 6. 拷贝图标
    icon_src = _get_icon("linux")
    if icon_src:
        shutil.copy(icon_src, icons_dir / f"{pkg_name}{icon_src.suffix}")

    # 7. 创建 /usr/bin 软链接
    executable_link = bin_dir / pkg_name
    target_rel = Path(f"../../opt/{pkg_name}/{APP_NAME}")
    os.symlink(target_rel, executable_link)

    # 8. 执行打包
    output_deb = DIST_DIR / f"{pkg_name}_{APP_VERSION}_amd64.deb"
    subprocess.run(["dpkg-deb", "--build", str(deb_dir), str(output_deb)], check=True)
    print(f".deb package built at {output_deb}")


def build(platform_key: str, name: str = APP_NAME):
    if not MAIN_FILE.exists():
        raise FileNotFoundError(f"Missing app.py entry point at {MAIN_FILE}")

    args = [
        str(MAIN_FILE),
        "--noconfirm",
        "--clean",
        f"--distpath={DIST_DIR}",
        f"--workpath={BUILD_DIR}",
        f"--name={name}",
    ]

    if platform_key == "windows":
        version_file = _write_win_version_file(BUILD_DIR / "version.txt")
        args.append(f"--version-file={version_file}")
    elif platform_key == "mac":
        meta_file = _write_unix_version_file(BUILD_DIR / "mac_version.txt")
        args.append(f"--add-data={meta_file}{os.pathsep}.")
    elif platform_key == "linux":
        meta_file = _write_unix_version_file(BUILD_DIR / "linux_version.txt")
        args.append(f"--add-data={meta_file}{os.pathsep}.")

    args.extend(_platform_args(platform_key))
    for data_arg in _add_data_args():
        args.append(f"--add-data={data_arg}")

    print(f"Running PyInstaller with args: {args}")
    PyInstaller.__main__.run(args)

    if platform_key == "linux":
        build_deb(DIST_DIR / name)


if __name__ == "__main__":
    _clean_outputs()
    platform_key = _resolve_platform()
    print(f"Detected platform: {platform_key}")
    build(platform_key=platform_key, name=APP_NAME)
