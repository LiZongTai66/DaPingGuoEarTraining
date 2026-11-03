from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import shutil
ROOT=Path(__file__).resolve().parent
files=['使用说明.md','piano_game_complete.v','original_gowin.v',
       'rhythm_game_core.v','01_game_load.txt','02_start_release.txt',
       '03_tm0_timer.txt','04_back_release.txt','05_game_unload.txt',
       'chart.json','screen_tests.txt','rtl_simulation.txt',
       'piano_game_complete.v.diagnostics.txt','original_gowin.v.diagnostics.txt',
       'tb_game.sv','tb_integration.sv','check_screen.py']
with ZipFile(ROOT/'音游模块.zip','w',ZIP_DEFLATED) as out:
    for file in files: out.write(ROOT/file, f'game_module/{file}')
shutil.copyfile(ROOT/'音游模块.zip', ROOT/'音游模块_50ms.zip')
shutil.copyfile(ROOT/'音游模块.zip', ROOT/'音游模块_50ms_无新增文本.zip')
print(f'Packaged {len(files)} files, {(ROOT/"音游模块.zip").stat().st_size} bytes')
try:
    print('Original HMI SHA256: '+hashlib.sha256((ROOT.parent/'piano.HMI').read_bytes()).hexdigest())
except PermissionError:
    print('HMI is open in the editor; package creation does not need to read it.')
