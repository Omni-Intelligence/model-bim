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
project_dir = os.getcwd()  # Use current directory in GitHub Actions
site_packages = site.getsitepackages()[0]  # Use first site-packages directory

print(f"Project directory: {project_dir}")
print(f"Site packages: {site_packages}")

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
    'python-dotenv'
]

# Initialize data files list
datas = []

# Handle assets directory safely
assets_dir = os.path.join(project_dir, 'assets')
os.makedirs(assets_dir, exist_ok=True)
datas.append((assets_dir, 'assets'))

# Create empty .env if needed
env_path = os.path.join(project_dir, '.env')
if not os.path.exists(env_path):
    with open(env_path, 'w') as f:
        f.write('# Placeholder .env created during build\n')
datas.append((env_path, '.'))

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

# Initialize binaries list
binaries = []

# Special package handling for problematic packages
for pkg_name in ['xhtml2pdf', 'markdown2', 'reportlab', 'html5lib']:
    for path in sys.path + site.getsitepackages():
        pkg_path = os.path.join(path, pkg_name)
        if os.path.exists(pkg_path) and os.path.isdir(pkg_path):
            print(f"Adding package directory: {pkg_path} -> {pkg_name}")
            if pkg_name in ['xhtml2pdf', 'markdown2']:
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

# Create placeholder main.py if it doesn't exist
main_path = os.path.join(project_dir, 'main.py')
if not os.path.exists(main_path):
    with open(main_path, 'w') as f:
        f.write('# Placeholder main.py created during build\n')

# Analyze the application
a = Analysis(
    [main_path],
    pathex=[project_dir, site_packages],
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

# Create the executable
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
    console=True,  # Always show console in CI
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