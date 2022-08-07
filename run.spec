# -*- mode: python ; coding: utf-8 -*-

block_cipher = pyi_crypto.PyiBlockCipher(key='as2gaFgWE1weA2a')


a = Analysis(['run.py'],
             pathex=['/Users/Zy/PycharmProjects/ptbGui'],
             binaries=[('/System/Library/Frameworks/Tk.framework/Tk', 'tk'), ('/System/Library/Frameworks/Tcl.framework/Tcl', 'tcl')],
             datas=[('source', 'source'), ('yanglabMFuns', 'yanglabMFuns')],
             hiddenimports=['pkg_resources.py2_warn'],
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
          [],
          exclude_binaries=True,
          name='run',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='source/images/common/icon.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='run')
app = BUNDLE(coll,
             name='run.app',
             icon='./source/images/common/icon.icns',
             bundle_identifier=None)
