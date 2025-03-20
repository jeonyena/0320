
"""마야 Shelf를 활용해 Artist가 현재작업중인 파일을 버전업해서 저장해주는 Code"""
"""마우스 중앙휠 클릭으로 상단 쉘프로 드래그하면 버튼 생김"""

import maya.cmds as cmds
import os
import re
# 현재있는 경로가 저장되었다면 버전업하는 코드 (ma이면 ma)(mb이면 mb)

# 현재 파일의 저장된 경로 가져오기
saved_path = cmds.file(q=True, sceneName=True)

# 파일이 저장되지 않은 경우 예외 처리
if not saved_path:
    cmds.warning("현재 씬이 저장되지 않았습니다. 먼저 저장 후 실행하세요.")
    raise RuntimeError("현재 씬이 저장되지 않았습니다.")


file_name = os.path.basename(saved_path)           # "spino_v019.mb"
file_base, file_ext = os.path.splitext(file_name)  # ("spino_v019", ".mb")
file_ext = file_ext[1:]                            # ".mb" → "mb"

match = re.search(r'_(v\d{3})\.', file_name)
file_ver = match.group(1)  # "v019" 추출

ver_num = int(file_ver[1:])                         # Result: 19 #

# 버전 증가 및 포맷 맞추기
ver_num_up = f"v{ver_num+1:03d}"  # Result: v020 #

new_save_file_path = saved_path.replace(file_ver, ver_num_up)
# Result: C:/Jupiter/work/Spino_Character_Modeling/scenes/Spino_v020.mb # 
# mb파일 그대로 저장하기

cmds.file(rename = new_save_file_path)
if file_ext == "mb":
    cmds.file(save=True, type="mayaBinary") # mb
elif file_ext == "ma":
    cmds.file(save=True, type="mayaAscii") # ma