#!/usr/bin/env python3
import os
import subprocess
import sys

# Get the virtual environment site-packages directory
venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv")
venv_site_packages = os.path.join(venv_path, "lib", "python3.10", "site-packages")

if not os.path.exists(venv_site_packages):
    # Try alternative path structure
    venv_site_packages = os.path.join(venv_path, "lib", "site-packages")
    if not os.path.exists(venv_site_packages):
        print(f"Could not find site-packages directory in {venv_path}")
        sys.exit(1)

print(f"Using site-packages from: {venv_site_packages}")

spec_content = f"""# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Collect all packages from the virtual environment
site_packages_path = r'{venv_site_packages}'

# Create a list of all packages to include
packages = [
    'tkinterweb', 
    'tkinterdnd2', 
    'PIL', 
    'customtkinter', 
    'markdown', 
    'docx', 
    'openai',
    'pypdf',
    'python-docx',
    'docx2pdf'
]

# Initialize data collection
datas = [('assets', 'assets'), ('.env', '.'), ('icon.ico', '.')]
binaries = []
hiddenimports = [
    'PIL._tkinter_finder', 
    'TkinterWeb', 
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
    hooksconfig={{}},
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
    name='analysthub_bim_insights',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon=['icon.ico'],
)
"""

# Write the spec file
with open("simple.spec", "w") as f:
    f.write(spec_content)

# Run PyInstaller
print("Building application with PyInstaller...")
subprocess.run(["pyinstaller", "--clean", "simple.spec"])

print("Build completed. Check the 'dist' directory for the executable.")
