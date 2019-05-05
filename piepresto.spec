# -*- mode: python -*-

block_cipher = None


a = Analysis(['piepresto.py'],
             pathex=['.'],
             binaries=[],
             datas=[('piepresto.png', '.')],
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
          name='piepresto',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='piepresto.png')
app = BUNDLE(exe,
             name='piepresto.app',
             icon='piepresto.icns',
             bundle_identifier=None,
             info_plist={
                'NSPrincipalClass': 'NSApplication'
             }
            )
