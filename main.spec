# -*- mode: python ; coding: utf-8 -*-

import os
import sys

from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None

site_packages_path = r'/var/www/html/python/analysthub/.venv/lib/python3.10/site-packages'

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
    pathex=[site_packages_path],
    binaries=binaries,
    datas=data_paths + datas,
    hiddenimports=[
        'PIL.Image', 'PIL._tkinter_finder', 'PIL._imagingtk', 'TkinterWeb',
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
    console=True,
    icon=['icon.ico'],
)