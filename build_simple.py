#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import shutil
import platform
import site

# Ensure we're running from the project root
project_root = os.path.abspath(os.path.dirname(__file__))
os.chdir(project_root)
print(f"Working directory set to: {project_root}")

# Detect environment
is_github_action = os.environ.get("GITHUB_ACTIONS") == "true"
is_windows = platform.system() == "Windows"

if is_github_action:
    print("Running in GitHub Actions environment")

# Find site-packages
venv_path = os.path.join(project_root, ".venv")
python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"

# Try multiple possible paths for site-packages
potential_paths = [
    os.path.join(venv_path, "lib", python_version, "site-packages"),
    os.path.join(venv_path, "lib", "site-packages"),
    os.path.join(venv_path, "Lib", "site-packages"),  # Windows path
]

# Add system site-packages
potential_paths.extend(site.getsitepackages())

venv_site_packages = None
for path in potential_paths:
    if os.path.exists(path):
        venv_site_packages = path
        break

if not venv_site_packages:
    print(f"Could not find site-packages directory")
    sys.exit(1)

print(f"Using site-packages from: {venv_site_packages}")

# Create the spec file content
spec_content = f"""# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import site
from PyInstaller.utils.hooks import collect_all

# For debugging
print(f"Building from directory: {{os.getcwd()}}")

# Block cipher setup
block_cipher = None

# Define important paths
project_dir = r'{project_root}'
site_packages_path = r'{venv_site_packages}'

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
    print(f"Including assets directory: {{assets_dir}}")
    datas.append((assets_dir, 'assets'))
else:
    print(f"Warning: Assets directory not found at {{assets_dir}}")
    # Create empty assets directory if it doesn't exist
    os.makedirs(assets_dir, exist_ok=True)
    datas.append((assets_dir, 'assets'))

# Add .env file if it exists
env_path = os.path.join(project_dir, '.env')
if os.path.exists(env_path):
    datas.append((env_path, '.'))
    print(f"Including .env file: {{env_path}}")
else:
    print(f"Warning: .env file not found at {{env_path}}")

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
            print(f"Adding package directory: {{pkg_path}} -> {{pkg_name}}")
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
        print(f"Collected data for package: {{package}}")
    except Exception as e:
        print(f"Warning: Could not collect data for {{package}}: {{e}}")

# Analyze the application
a = Analysis(
    [os.path.join(project_dir, 'main.py')],
    pathex=[project_dir, site_packages_path],
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
    console={not is_windows},  # Console for debugging on non-Windows
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
"""

# Write spec file
spec_path = os.path.join(project_root, "build.spec")
with open(spec_path, "w") as f:
    f.write(spec_content)
print(f"Created spec file at: {spec_path}")

# Clear previous build artifacts
dist_path = os.path.join(project_root, "dist")
build_path = os.path.join(project_root, "build")

for path in [dist_path, build_path]:
    if os.path.exists(path):
        print(f"Clearing previous build directory: {path}")
        shutil.rmtree(path)

# Run PyInstaller directly (not as a module)
print("Building application with PyInstaller...")
result = subprocess.run(
    ["pyinstaller", "--clean", spec_path],
    capture_output=True,
    text=True,
)

# Print output
print("\n--- PyInstaller Output ---")
print(result.stdout)
if result.stderr:
    print("\n--- PyInstaller Errors ---")
    print(result.stderr)

if result.returncode != 0:
    print("Build failed!")
    sys.exit(1)

# Create convenience scripts for running
executable_dir = os.path.join(dist_path, "analysthub_bim_insights")
if not os.path.exists(executable_dir):
    print(f"Error: Expected build directory not found at {executable_dir}")
    sys.exit(1)

if is_windows:
    with open(os.path.join(project_root, "run_app.bat"), "w") as f:
        f.write("@echo off\n")
        f.write("cd %~dp0\n")
        f.write("dist\\analysthub_bim_insights\\analysthub_bim_insights.exe\n")
    print("Created run_app.bat for Windows")
else:
    with open(os.path.join(project_root, "run_app.sh"), "w") as f:
        f.write("#!/bin/bash\n\n")
        f.write('cd "$(dirname "$0")"\n\n')
        f.write("chmod +x ./dist/analysthub_bim_insights/analysthub_bim_insights\n")
        f.write("./dist/analysthub_bim_insights/analysthub_bim_insights\n")

    os.chmod(os.path.join(project_root, "run_app.sh"), 0o755)

    # Ensure the executable has proper permissions
    executable_path = os.path.join(executable_dir, "analysthub_bim_insights")
    if os.path.exists(executable_path):
        os.chmod(executable_path, 0o755)
        print(f"Set execute permissions for {executable_path}")
    else:
        print(f"Warning: Could not find executable at {executable_path}")

    print("Created run_app.sh for Unix/Linux/Mac")

print("\nBuild completed successfully.")
print(
    "IMPORTANT: This builds a DIRECTORY-MODE executable that must be distributed as a directory."
)
print("To run the application:")

if is_windows:
    print("  - Run 'run_app.bat'")
    print(
        "  - Or navigate to dist\\analysthub_bim_insights and run analysthub_bim_insights.exe"
    )
else:
    print("  - Run './run_app.sh'")
    print(
        "  - Or navigate to dist/analysthub_bim_insights and run ./analysthub_bim_insights"
    )

print(
    "\nFor GitHub Actions or automated builds, the entire 'dist/analysthub_bim_insights' directory"
)
print("should be packaged as a zip/tar archive for distribution.")
