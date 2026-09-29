# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['local_client.py'],
    pathex=[
        '.',
        'demo_app',
    ],
    binaries=[],
    datas=[
        ('demo_app/static', 'demo_app/static'),
        ('demo_app/auth.py', 'demo_app'),
        ('demo_app/server_unified.py', 'demo_app'),
        ('demo_app/bridge_manager.py', 'demo_app'),
        ('demo_app/ws_server.py', 'demo_app'),
        ('scripts', 'scripts'),
        ('wiki', 'wiki'),
        ('contacts.json', '.'),
        ('config.yaml', '.'),
        ('.jira_config', '.'),
    ],
    hiddenimports=[
        'win32timezone', 'win32com', 'win32com.client', 'pythoncom', 'pywintypes',
        'pywin32_system32', 'win32com.client.gencache',
        'aiohttp', 'aiohttp.web', 'openpyxl',
        'webview', 'webview.platforms.winforms',
        'clr_loader', 'pythonnet',
        'auth', 'bridge_manager', 'ws_server',
        'scripts.run_daily_report', 'scripts.assessment_flow',
        'scripts.download_psv_manual', 'scripts.download_pvs_attachments',
        'scripts.parse_pvs_to_wiki', 'scripts.sync_pvs_wiki',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'scipy', 'pandas', 'tkinter', 'unittest', 'test'],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GRCAgent',
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
    icon=None,
)
