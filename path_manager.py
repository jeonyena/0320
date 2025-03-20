
from pathlib import Path
import maya.cmds as cmds
from file_parsing import FileParser

import os

class MayaPathManager:
    """FileParser 클래스로 분리된 정보를 이용하여 Maya 파일 및 폴더 경로 관리 클래스"""

    def __init__(self, pub_app_manager: 'PublishAppManager',path=None):
        self.app = pub_app_manager
        self.ui = pub_app_manager.ui  # UI 접근 가능

        # Maya 파일 경로 설정
        self.current_maya_path = path or cmds.file(q=True, sceneName=True)
        if not self.current_maya_path:
            raise ValueError("MayaPathManager를 생성할 때 file_path를 반드시 입력해야 합니다. 씬을 먼저 저장하세요.")


        """패턴에서 영어 대소문자 하나라도 틀려도 안됨 (spino와 Spino를 다르게 인식)"""
        """File Parser는 절대경로 기반이기 때문에 상대경로 사용된 파일 사용시 오류 예상"""
        # FileParser 모듈 인스턴스 생성
        self.current_maya_parser = FileParser(self.current_maya_path)
        self.current_parsed_data = self.current_maya_parser.data  # 딕셔너리 data
        self.pattern_key = self.current_maya_parser.matched_key   # Path 패턴 정보

        self.define_path_info()
        self.define_works_info() # UI Handeler에서 사용되는 setText Label에 사용되는 정보
        self.define_publish_path()
        self.define_confirm_path()
        self.define_cache_path()
        # self.define_image_seq_path()

    def key_error_gaurd(self):
        """None대신 ''으로, Key Error방지"""
        self.project = self.current_parsed_data.get("project")
        self.work_dir = self.current_parsed_data.get("work_dir")
        self.seq_name = self.current_parsed_data.get("seq_name")
        self.shot_num = self.current_parsed_data.get("shot_num")
        self.step = self.current_parsed_data.get("step")
        self.asset_name = self.current_parsed_data.get("asset_name")
        self.asset_type = self.current_parsed_data.get("asset_type")
        self.file_ver = self.current_parsed_data.get("version")
        self.ext = self.current_parsed_data.get("ext")

    def define_path_info(self):
        """
        File_Parser 클래스로 분리된 정보를 이용하여 경로정보 정의 
        (절대경로를 기반으로 했기에 상대경로 파일 사용시 오류발생)

        self.parsed_data = self.current_maya_parser.data
        [project], [work_dir], [seq_name], [shot_num], [step], [asset_name], [asset_type], [version], [ext]
        
        self.current_maya_path = cmds.file(q=True, sceneName=True) # (저장되어있는 상태)현재 켜져있는 Maya Scene경로 받기 # q는 query 
        """
        
        self.key_error_gaurd() # Key Error - None값 방지
        
        # # FileParser가 정상적으로 동작하는지 확인
        # print("Parsed Data:", self.current_parsed_data)
        # print("Pattern Key:", self.pattern_key)

        if "project" not in self.current_parsed_data:
            print('*'*50)
            print("파일명 다시 재확인")
            print('*'*50)
            print(self.current_maya_path)
            print('*'*50)
            raise KeyError("Oh My God")

        # self.parent_dir = Path(self.current_maya_path).parent # 폴더 위치한경로 (파일명.확장자 부분제외한 경로)
        
        
        try:
            self.parent_dir = Path(self.current_maya_path).parent  # 에러 발생 가능 부분
        except TypeError:
            print(" TypeError 발생: 경로가 None입니다. 파일을 저장하세요.")
            self.parent_dir = None
        
        
        
        
        self.project =  self.current_parsed_data["project"]
        self.work_dir =  self.current_parsed_data["work_dir"]
        self.ext =  self.current_parsed_data["ext"]                     #  mb
        self.file_ver =  self.current_parsed_data["version"]            #  v019
        self.ver_num =   int(self.file_ver[1:])                         #  19

    def define_works_info(self):
        """UI에 사용될 Work's info 정의"""
        if self.pattern_key == "maya_seq":
            self.works_info = f"{self.seq_name}_{self.shot_num}_{self.step}"
            self.file_name = f"{self.seq_name}_{self.shot_num}_{self.file_ver}.{self.ext}"
        
        elif self.pattern_key == "maya_asset":
            self.works_info = f"{self.asset_name}_{self.asset_type}"
            self.file_name = f"{self.asset_name}_{self.file_ver}.{self.ext}"

    def define_publish_path(self):
        """
        Publish 와 관련된 Path  
        PathManager에서는 
        comboBox확장자 currentText는 작동X
        """
        self.work_maya_path = self.current_maya_path
        # 확장자 제거된 파일 위치
        self.no_dot_ext_work_path = self.work_maya_path.replace(f".{self.ext}","")
        # print(f" define pub path No ext work path:{self.no_dot_ext_work_path}")
        
        # work -> pub 변경 (select ext 적용안됨)
        self.change_to_pub = self.work_maya_path.replace(self.work_dir, "pub")
        # print(f"define pub path change to pub:{self.change_to_pub}")
        
        # pub으로 바뀐 파일위치 경로
        self.pub_parent_dir = Path(self.change_to_pub).parent
        # print(f"define pub path pub parent dir:{self.pub_parent_dir}")
        
        # pub으로 바뀐 확장자 제거된 경로
        self.no_dot_ext_pub_path = self.change_to_pub.replace(f".{self.ext}","")
        # print(f"define pub path no ext pub path:{self.no_dot_ext_pub_path}")
        
    def define_cache_path(self): # 알렘빅 캐쉬 Data
        """
        cache경로로 abc Export
        파일명은 User가 선택한 object 네이밍
        work Path :  /nas/Batz_Maru/Jupiter/work/IndoRex_Character_Lookdev/scenes/IndoRex_v025.ma
        cache Path : /nas/Batz_maru/Jupiter/cache/IndoRex_Character_Lookdev/v001/IndoRex.abc
                                                        /{works_info}/{file_ver}/{user_select_object_name}.abc
        """
        
        self.change_to_cache = self.no_dot_ext_work_path.replace(self.work_dir,"cache")
        # /nas/Batz_maru/Jupiter/cache/IndoRex_Character_Lookdev/secens/IndoRex
        self.version_cache = self.change_to_cache.replace("scenes",f"{self.file_ver}")
        # /nas/Batz_maru/Jupiter/cache/IndoRex_Character_Lookdev/v001/IndoRex

        # 임시 abc경로
        self.cache_path = self.version_cache + ".abc"
        # /nas/Batz_maru/Jupiter/cache/IndoRex_Character_Lookdev/v001/IndoRex.abc
        
        # 위치한 폴더 경로
        self.cache_parent_dir = Path(self.cache_path).parent
        # /nas/Batz_maru/Jupiter/cache/IndoRex_Character_Lookdev/v001/

        self.cache_version_parent_dir = Path(self.cache_parent_dir).parent
        # print(f"캐쉬 버전 패런츠 : {self.cache_version_parent_dir}")
        # /nas/Batz_maru/Jupiter/cache/IndoRex_Character_Lookdev/

        # Cache Version 폴더 경로 안에 있는 파일 리스트
        # self.cache_files = os.listdir(self.cache_parent_dir)

    def define_thumbnail_path(self):    # sg_publishes_thumbnail
        """
        self.thumb_path가 쓰이는곳만 사용
        /nas/Batz_maru/Jupiter/work/Spino_Character_Model/scenes/Spino_v019.mb
        /nas/Batz_maru/Jupiter/thumbnail/Spino_Character_Model/Jupiter_Spino_Character_Model_thumb.jpg
        # /{project}_{asset_type}_{asset_name}_{step}_{version}_thumb.jpg
        """
        base_thumb_dir = f"/nas/Batz_maru/{self.project}/thumbnail"

        if self.pattern_key == "maya_seq":
            # 시퀀스 썸네일 이름설정
            self.seq_thumb_name =f"{self.project}_{self.seq_name}_{self.shot_num}_{self.step}_{self.file_ver}"
            self.seq_thumb_file = f"{self.seq_thumb_name}_thumb.jpg"
            # 시퀀스 썸네일 패스 설정
            self.seq_thumb_dir = f"{base_thumb_dir}/{self.seq_name}_{self.shot_num}_{self.step}/"
            self.thumb_path = os.path.join(self.seq_thumb_dir, self.seq_thumb_file)
            self.thumb_name = self.seq_thumb_name

        elif self.pattern_key == "maya_asset":
            # 에셋 썸네일 이름설정
            self.asset_thumb_name = f"{self.project}_{self.asset_type}_{self.asset_name}_{self.step}_{self.file_ver}"
            self.asset_thumb_file = f"{self.asset_thumb_name}_thumb.jpg"
            # 에셋 썸네일 패스 설정
            self.asset_thumb_dir = f"{base_thumb_dir}/{self.asset_type}_{self.asset_name}_{self.step}/"
            self.thumb_path = os.path.join(self.asset_thumb_dir, self.asset_thumb_file)
            self.thumb_name = self.asset_thumb_name

        self.thumb_dir = os.path.dirname(self.thumb_path)

    def define_confirm_path(self):   # playblast (컨펌받기위해 필요한 영상 경로 정의) / sg_version_thumbnail
        """
        self.confirm_path가 쓰이는곳만 사용
        """
        base_confirm_dir = f"/nas/Batz_maru/{self.project}/confirm"

        if self.pattern_key == "maya_seq":
            # 시퀀스 플레이블라스트

            self.confirm_file_name = f"{self.seq_name}_{self.shot_num}_{self.step}_{self.file_ver}"
            self.seq_confirm_mov_name = f"{self.confirm_file_name}.mov"
            self.seq_confirm_dir = f"{base_confirm_dir}/{self.seq_name}_{self.shot_num}_{self.step}/mov/"
            self.confirm_mov_path = self.seq_confirm_dir + self.seq_confirm_mov_name

        elif self.pattern_key == "maya_asset":
            # 에셋 플레이블라스트

            """
            mov 경로
            /nas/Batz_Maru/Jupiter/confirm/IndoRex_Character_Lookdev/mov/
            IndoRex_v025.mov

            이미지시퀀스
            /nas/Batz_Maru/Jupiter/confirm/IndRex_Character_Lookdev/image_seq_v025/
            IndoRex_v025.%04d.jpg [1~200]
            """

            self.confirm_file_name = f"{self.asset_name}_{self.file_ver}"
            self.asset_confirm_mov_name = f"{self.confirm_file_name}.mov"
            self.asset_confirm_dir = f"{base_confirm_dir}/{self.asset_name}_{self.asset_type}_{self.step}/mov/"
            self.confirm_mov_path = self.asset_confirm_dir + self.asset_confirm_mov_name



        # Confirm 경로
        self.confirm_mov_dir = str(Path(self.confirm_mov_path).parent)
        self.confirm_step_dir =  self.confirm_mov_dir.replace("mov","")
        self.confirm_img_seq_dir_name = f"image_seq_{self.file_ver}"
        self.confirm_img_seq_dir = self.confirm_step_dir + self.confirm_img_seq_dir_name
        self.confirm_img_seq_name = f"{self.confirm_img_seq_dir}/{self.confirm_file_name}"
        self.confirm_ffmpeg_jpg = f"{self.confirm_img_seq_name}.%04d.jpg"
