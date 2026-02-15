"""
Build script for RandPicker - DEPRECATED

This script is deprecated and has been replaced with modular scripts:
- scripts/pre_build.py - Pre-packaging file processing
- scripts/pyinstaller_args.py - Generate PyInstaller arguments
- scripts/post_build.py - Post-packaging file processing

For manual builds, run these in order:
1. python scripts/pre_build.py
2. pyinstaller $(python scripts/pyinstaller_args.py)
3. python scripts/post_build.py

Or use the GitHub Actions workflow instead.
"""

import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    """Legacy build process - runs the modular build scripts."""
    print("=" * 80)
    print("WARNING: This script is deprecated. Use the modular scripts instead.")
    print("=" * 80)
    print("\nRunning modular build process...\n")
    
    scripts_dir = ROOT / "scripts"
    
    # Step 1: Pre-build
    print("Step 1: Running pre-build processing...")
    result = subprocess.run([sys.executable, scripts_dir / "pre_build.py"], cwd=ROOT)
    if result.returncode != 0:
        print("Pre-build failed!")
        sys.exit(1)
    
    # Step 2: PyInstaller
    print("\nStep 2: Running PyInstaller...")
    args_result = subprocess.run(
        [sys.executable, scripts_dir / "pyinstaller_args.py"],
        cwd=ROOT,
        capture_output=True,
        text=True
    )
    if args_result.returncode != 0:
        print("Failed to generate PyInstaller arguments!")
        sys.exit(1)
    
    pyinstaller_args = args_result.stdout.strip().split('\n')
    result = subprocess.run(["pyinstaller"] + pyinstaller_args, cwd=ROOT)
    if result.returncode != 0:
        print("PyInstaller build failed!")
        sys.exit(1)
    
    # Step 3: Post-build
    print("\nStep 3: Running post-build processing...")
    result = subprocess.run([sys.executable, scripts_dir / "post_build.py"], cwd=ROOT)
    if result.returncode != 0:
        print("Post-build failed!")
        sys.exit(1)
    
    print("\n" + "=" * 80)
    print("Build completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()

