# -*- mode: python -*-

block_cipher = None


a = Analysis(['Automatic_off_sprd.py'],
             pathex=['E:\\VsProjects\\Automatic_off_sprd\\Automatic_off_sprd'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Automatic_off_sprd',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
