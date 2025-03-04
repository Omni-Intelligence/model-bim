# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None

# Use the current Python environment's site-packages instead of the Linux path
# This will properly reference the environment where PyInstaller is running
site_packages_path = os.path.join(sys.base_prefix, 'Lib', 'site-packages')

datas = []
binaries = []
hiddenimports = []

packages = [
    'PIL', 
    'tkinterweb', 
    'html5lib',
    'reportlab',
    'tkinterdnd2', 
    'customtkinter', 
    'markdown2', 
    'docx', 
    'openai',
    'xhtml2pdf',
]

for package in packages:
    try:
        pkg_datas, pkg_binaries, pkg_hiddenimports = collect_all(package)
        datas.extend(pkg_datas)
        binaries.extend(pkg_binaries)
        hiddenimports.extend(pkg_hiddenimports)
    except Exception as e:
        print(f"Could not collect package {package}: {e}")

tkinterweb_imports = collect_submodules('tkinterweb')
hiddenimports += tkinterweb_imports

data_paths = [
    ('.env', '.'), 
    ('icon.ico', '.'),
    ('assets', 'assets'),
]

a = Analysis(
    ['main.py'],
    pathex=[os.getcwd()],  # Use current working directory instead of hardcoded path
    binaries=binaries,
    datas=data_paths + datas,
    hiddenimports=[
        'PIL.Image', 'PIL._tkinter_finder', 'PIL._imagingtk', 'tkinterweb',  # Changed from TkinterWeb to tkinterweb
    ] + hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    a.zipfiles,
    [],
    name='model_bim_insights',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon=['icon.ico'],
)