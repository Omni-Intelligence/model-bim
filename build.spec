# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import site
from PyInstaller.utils.hooks import collect_all

# For debugging
print(f"Building from directory: {os.getcwd()}")

# Block cipher setup
block_cipher = None

# Define important paths
project_dir = r'/var/www/html/python/analysthub'
site_packages_path = r'/var/www/html/python/analysthub/.venv/lib/python3.10/site-packages'

# List packages to include
packages = [
    'tkinterweb', 
    'tkinterdnd2', 
    'PIL', 
    'customtkinter', 
    'markdown2',
    'docx',       
    'openai',
    'xhtml2pdf',
    'reportlab',
    'html5lib',
    'pypdf',
    'dotenv'
]

# Handle assets directory
datas = []
assets_dir = os.path.join(project_dir, 'assets')
if os.path.exists(assets_dir):
    print(f"Including assets directory: {assets_dir}")
    datas.append((assets_dir, 'assets'))
else:
    print(f"Warning: Assets directory not found at {assets_dir}")
    # Create empty assets directory if it doesn't exist
    os.makedirs(assets_dir, exist_ok=True)
    datas.append((assets_dir, 'assets'))

# Add .env file if it exists
env_path = os.path.join(project_dir, '.env')
if os.path.exists(env_path):
    datas.append((env_path, '.'))
    print(f"Including .env file: {env_path}")
else:
    print(f"Warning: .env file not found at {env_path}")

# Hidden imports that might be missed
hiddenimports = [
    'PIL._tkinter_finder',
    'TkinterWeb',
    'html5lib',
    'reportlab',
    'xhtml2pdf.w3c',
    'html5lib.treebuilders.etree',
    'pypdf',
    'numpy',
    'json',
    're',
    'urllib',
    'urllib3',
    'http.client',
    'email.message',
    'markdown2',
    'io',
]

# Add important modules directly
binaries = []

# Special package handling for problematic packages
for pkg_name in ['xhtml2pdf', 'markdown2', 'reportlab', 'html5lib']:
    for path in sys.path + site.getsitepackages():
        pkg_path = os.path.join(path, pkg_name)
        if os.path.exists(pkg_path) and os.path.isdir(pkg_path):
            print(f"Adding package directory: {pkg_path} -> {pkg_name}")
            if pkg_name in ['xhtml2pdf', 'markdown2']:  # Critical packages
                datas.append((pkg_path, pkg_name))
            break

# Collect all package data
for package in packages:
    try:
        pkg_datas, pkg_binaries, pkg_hiddenimports = collect_all(package)
        datas.extend(pkg_datas)
        binaries.extend(pkg_binaries)
        hiddenimports.extend(pkg_hiddenimports)
        print(f"Collected data for package: {package}")
    except Exception as e:
        print(f"Warning: Could not collect data for {package}: {e}")

# Analyze the application
a = Analysis(
    [os.path.join(project_dir, 'main.py')],
    pathex=[project_dir, site_packages_path],
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

# Create the PYZ archive
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create the main executable in directory mode (more reliable)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='analysthub_bim_insights',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Console for debugging on non-Windows
    icon=None,
)

# Create the distribution directory
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='analysthub_bim_insights',
)
