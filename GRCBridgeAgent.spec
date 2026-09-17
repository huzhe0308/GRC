# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['bridge_agent.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['win32timezone', 'win32com', 'win32com.client', 'pythoncom', 'pywintypes', 'pywin32_system32', 'win32com.client.gencache'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GRCBridgeAgent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
