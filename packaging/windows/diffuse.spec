# PyInstaller specification for Windows 10/11 x64.

from pathlib import Path


root = Path(SPECPATH).parents[1]

a = Analysis(
    [str(root / 'packaging' / 'windows' / 'launcher.py')],
    pathex=[str(root / 'src')],
    binaries=[],
    datas=[
        (str(root / 'build' / 'windows' / 'diffuse.gresource'), '.'),
        (str(root / 'packaging' / 'windows' / 'diffuserc'), '.'),
        (str(root / 'data' / 'usr' / 'share' / 'diffuse' / 'syntax'), 'syntax'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={
        'gi': {
            'icons': ['Adwaita'],
            'themes': ['Adwaita'],
            'languages': ['en', 'ru'],
            'module-versions': {'Gtk': '3.0'},
        },
    },
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Diffuse',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=str(root / 'windows-installer' / 'diffuse.ico'),
    contents_directory='.',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name='Diffuse',
)
