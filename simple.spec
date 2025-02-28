# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Collect all packages from the virtual environment
site_packages_path = r'/var/www/html/python/analysthub/.venv/lib/python3.10/site-packages'

# Create a list of all packages to include
packages = [
    'tkinterweb', 
    'tkinterdnd2', 
    'PIL', 
    'customtkinter', 
    'markdown', 
    'docx', 
    'weasyprint', 
    'openai',
    'PyQt6'
]

# Initialize data collection
datas = [('assets', 'assets'), ('.env', '.'), ('icon.ico', '.'), (os.path.join(site_packages_path, 'PyQt6', 'Qt6', 'plugins'), 'PyQt6/Qt6/plugins')]
binaries = []
hiddenimports = [
    'PIL._tkinter_finder', 
    'TkinterWeb', 
    'PyQt6', 
    'PyQt6.QtWidgets',
    'PyQt6.QtWidgets.QApplication',
    'PyQt6.QtWidgets.QFileDialog',
    'PyQt6.QtCore'
    'PyQt6.QtGui',
    'PyQt6.sip',
]

# Collect all data for each package
for package in packages:
    pkg_datas, pkg_binaries, pkg_hiddenimports = collect_all(package)
    datas.extend(pkg_datas)
    binaries.extend(pkg_binaries)
    hiddenimports.extend(pkg_hiddenimports)

a = Analysis(
    ['main.py'],
    pathex=[site_packages_path],  # Add site-packages to path
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='analysthum_bim_insights',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to True for debugging
    icon=['icon.ico'],
)
