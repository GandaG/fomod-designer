# -*- mode: python -*-

block_cipher = None
import os
import validator.validate

a = Analysis(['pyinstaller-bootstrap.py'],
             pathex=[os.getcwd()],
             binaries=None,
             datas=[('../resources', 'resources'),
                    (validator.validate.SCHEMA_FILE_PATH, 'resources'),
                    ('../setup.cfg', '.'),],
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
          name='FOMOD Designer',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='resources/file_icon.ico')
