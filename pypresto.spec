# -*- mode: python -*-

block_cipher = None


a = Analysis(['pypresto.py'],
             pathex=['.'],
             binaries=[],
             datas=[('pypresto.png', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='pypresto',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='pypresto.png')
app = BUNDLE(exe,
             name='pypresto.app',
             icon='pypresto.icns',
             bundle_identifier=None,
             info_plist={
                'NSPrincipalClass': 'NSApplication'
             }
            )
