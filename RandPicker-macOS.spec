# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('src', 'src'),
        ('LICENSE', 'LICENSE'),
        ('lib', 'lib'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='RandPicker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=False,
    icon='assets/icon-dark.icns',
    contents_directory='.',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=[],
    name='RandPicker',
)

app = BUNDLE(
    coll,
    name='RandPicker.app',
    icon='assets/icon-dark.icns',
    bundle_identifier=None,
    info_plist = {
        'NSCameraUsageDescription': 'RandPicker needs access to the camera to perform face selection.'
    }
)
