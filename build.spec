# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import importlib
import shutil
from PyInstaller.utils.hooks import collect_all, collect_submodules, collect_data_files
with open('hook_packages.py', 'w') as f:
    f.write("""
import sys
import os

# Add package directories to path at runtime
package_dirs = ['xhtml2pdf', 'markdown2', 'tkinterweb', 'tkinterdnd2']
for pkg in package_dirs:
    pkg_path = os.path.join(sys._MEIPASS, pkg)
    if os.path.exists(pkg_path) and pkg_path not in sys.path:
        sys.path.insert(0, pkg_path)
        print(f"Added {pkg_path} to path")
""")

def get_package_path(package_name):
    try:
        package = importlib.import_module(package_name)
        return os.path.dirname(package.__file__)
    except ImportError:
        print(f"Warning: Cannot import {package_name}")
        return None

def collect_package(package_name):
    try:
        datas, binaries, hiddenimports = collect_all(package_name)
        pkg_path = get_package_path(package_name)
        if pkg_path:
            print(f"Package {package_name} found at {pkg_path}")
            datas.append((pkg_path, package_name))
        return datas, binaries, hiddenimports
    except Exception as e:
        print(f"Warning: Error collecting package {package_name}: {e}")
        return [], [], []

def bundle_package(package_name):
    src_path = get_package_path(package_name)
    if not src_path:
        return None
    
    # Create a local copy for bundling
    dst_path = os.path.join(os.getcwd(), f'_bundled_{package_name}')
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)
    
    shutil.copytree(src_path, dst_path)
    print(f"Bundled {package_name} from {src_path} to {dst_path}")
    return dst_path

xhtml2pdf_bundle = bundle_package('xhtml2pdf')
markdown2_bundle = bundle_package('markdown2')

tkinterweb_datas, tkinterweb_binaries, tkinterweb_hiddenimports = collect_package('tkinterweb')
tkinterdnd_datas, tkinterdnd_binaries, tkinterdnd_hiddenimports = collect_package('tkinterdnd2')
xhtml2pdf_datas, xhtml2pdf_binaries, xhtml2pdf_hiddenimports = collect_package('xhtml2pdf')
markdown2_datas, markdown2_binaries, markdown2_hiddenimports = collect_package('markdown2')

tkdnd_path = os.path.join(os.path.dirname(importlib.import_module('tkinterdnd2').__file__), 'tkdnd')
tkhtml_path = os.path.join(os.path.dirname(importlib.import_module('tkinterweb').__file__), 'tkhtml')

binaries = [
    *tkinterweb_binaries,
    *tkinterdnd_binaries,
    *xhtml2pdf_binaries,
    *markdown2_binaries,
]

if os.path.exists(tkdnd_path):
    binaries.append((tkdnd_path, 'tkdnd'))
if os.path.exists(tkhtml_path):
    binaries.append((tkhtml_path, 'tkhtml'))

datas = [
    ('.env', '.'), 
    ('icon.ico', '.'), 
    ('assets', 'assets')
]    

if xhtml2pdf_bundle:
    datas.append((xhtml2pdf_bundle, 'xhtml2pdf'))
if markdown2_bundle:
    datas.append((markdown2_bundle, 'markdown2'))

# Add collected data
datas.extend([
    *tkinterweb_datas,
    *tkinterdnd_datas,
    *xhtml2pdf_datas,
    *markdown2_datas,
])

a = Analysis(
    ['main.py'],
    pathex=[os.getcwd()],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        'xhtml2pdf', 'xhtml2pdf.w3c', 'xhtml2pdf.pisa', 'xhtml2pdf.context',
        'xhtml2pdf.default', 'xhtml2pdf.parser', 'xhtml2pdf.util', 'xhtml2pdf.tags',
        'markdown2',
        'tkinterweb',
        'tkinterweb.htmlwidgets',
        'tkinterweb.bindings',
        'tkinterweb.widgets',
        'tkinterdnd2',
        'tkinterdnd2.TkinterDnD',
        'reportlab',
        'reportlab.pdfbase',
        'reportlab.pdfgen',
        'reportlab.platypus',
        'html5lib',
        'html5lib.treebuilders.etree',
        'pypdf',
        'customtkinter',
        'PIL._tkinter_finder',
        'PIL',
        'docx',
        'openai',
        'dotenv',
        'json',
        're',
        'urllib',
        'urllib3',
        'http.client',
        'email.message',
        'io',
        *tkinterweb_hiddenimports,
        *tkinterdnd_hiddenimports,
        *xhtml2pdf_hiddenimports,
        *markdown2_hiddenimports,
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['hook_packages.py'],
    excludes=[],
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name='analysthub_bim_insights',
    debug=True,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True,
    icon='icon.ico'
)