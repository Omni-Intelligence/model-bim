# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all

def collect_package(package_name):
    datas, binaries, hiddenimports = collect_all(package_name)
    return datas, binaries, hiddenimports

tkinterweb_datas, tkinterweb_binaries, tkinterweb_hiddenimports = collect_package('tkinterweb')
tkinterdnd_datas, tkinterdnd_binaries, tkinterdnd_hiddenimports = collect_package('tkinterdnd2')
xhtml2pdf_datas, xhtml2pdf_binaries, xhtml2pdf_hiddenimports = collect_package('xhtml2pdf')
markdown2_datas, markdown2_binaries, markdown2_hiddenimports = collect_package('markdown2')

binaries = [
    *tkinterweb_binaries,
    *tkinterdnd_binaries,
    *xhtml2pdf_binaries,
    *markdown2_binaries,
]

datas = [
    ('.env', '.'), 
    ('icon.ico', '.'), 
    ('assets', 'assets'),
    *tkinterweb_datas,
    *tkinterdnd_datas,
    *xhtml2pdf_datas,
    *markdown2_datas,
]

a = Analysis(
    ['main.py'],
    pathex=[os.getcwd()],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        'xhtml2pdf',
        'markdown2',
        'tkinterweb',
        'tkinterdnd2',
        'reportlab',
        'html5lib',
        'pypdf',
        'customtkinter',
        'PIL',
        'docx',
        'openai',
        'dotenv',
        *tkinterweb_hiddenimports,
        *tkinterdnd_hiddenimports,
        *xhtml2pdf_hiddenimports,
        *markdown2_hiddenimports,
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'IPython',
        'jupyter',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name='analysthub_bim_insights',
    debug=False, 
    strip=True,  
    upx=True,    
    upx_exclude=['vcruntime140.dll'],  
    runtime_tmpdir=None,
    console=True, 
    icon='icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=['vcruntime140.dll'],
    name='analysthub_bim_insights'
)