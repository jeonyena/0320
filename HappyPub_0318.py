"""
from importlib import reload
import sys

sys.path.append("/nas/Batz_Maru/pingu/nana/merge")


import HappyPub_0318
reload(HappyPub_0318)
w = HappyPub_0318.PublishAppManager()
"""

try:
    from PySide6.QtWidgets import QMainWindow, QApplication, QMenu, QMessageBox
    from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QTreeWidget, QDialog
    from PySide6.QtWidgets import QWidget, QComboBox, QLabel, QLineEdit, QPushButton, QTreeWidgetItem
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import Qt, QFile, QRect, QRect, QTimer, QSize
    from PySide6.QtGui import QPainter, QPixmap, QIcon, QCursor, QMovie
except:
    from PySide2.QtWidgets import QMainWindow, QApplication, QMenu, QMessageBox
    from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QTreeWidget, QDialog
    from PySide2.QtWidgets import QWidget, QComboBox, QLabel, QLineEdit, QPushButton, QTreeWidgetItem
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import Qt, QFile, QRect, QRect, QTimer, QSize
    from PySide2.QtGui import QPainter, QPixmap, QIcon, QCursor, QMovie
    import maya.cmds as cmds
    import shutil

import os
import re
import json
# import time
from shotgun_api3 import Shotgun
from pathlib import Path

from file_parsing import FileParser

import subprocess

from path_manager import MayaPathManager



import sys
sys.path.append("/nas/Batz_Maru/pingu/nana/yenyaong")

import sg_api


# from sg_api_test_2 import SG_Publish


class PublishAppManager(QMainWindow):
    """Publish와 UI 관련된 class 관리"""
    def __init__(self):
        super().__init__()
        # self.root_path = "/nas/Batz_Maru"

        self.load_ui()

        # PathManager : Path들 정의
        self.maya_path_manager = MayaPathManager(self)

        # PlayblastHandler : Playblast 관련 스크린샷, 영상
        self.playblast_handler = PlayBlastHandler(self)

        # MayaFileManager : Maya Publish 파일저장, 내보내기
        self.maya_file_manager = MayaFileManager(self)

        # UIManager : UI 기능 모음
        self.ui_manager = UIManager(self)
        
    def receive_pub_data(self, pub_data):
            """
            MayaFileManager에서 생성한 딕셔너리 데이터를 받아서 저장 후 샷그리드에 업로드
            """

            print(f" 디버깅: receive_pub_data에서 받은 pub_data = {pub_data}")

            if not isinstance(pub_data, dict):
                raise ValueError(" Error: receive_pub_data에서 받은 pub_data가 딕셔너리가 아닙니다.")

            if "pub_files" not in pub_data:
                raise KeyError(" Error: receive_pub_data에서 받은 pub_data에 'pub_files' 키가 없습니다.")


            self.pub_data = pub_data
            print("MayaFileManager에서 전달받은 데이터:", self.pub_data)
            p = sg_api.SGPublisher(self.pub_data) 
            S = p.get_dict(self.pub_data)
            print("SG 전송완료")

    def load_ui(self):
        ui_file_path = "/nas/Batz_Maru/pingu/nana/merge/Happypub_0318.ui"
        ui_file = QFile(ui_file_path)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        self.ui.show()
        ui_file.close()



class UIManager:
    """UI 이벤트 및 연결을 관리하는 클래스"""

    def __init__(self, pub_app_manager):
        self.app = pub_app_manager
        self.ui = pub_app_manager.ui  
        
        # AppManager에서 받아오는 class 인스턴스
        self.maya_path_manager = pub_app_manager.maya_path_manager
        self.maya_file_manager = pub_app_manager.maya_file_manager
        self.playblast_handler = pub_app_manager.playblast_handler
        
        self.click_connect()
        self.label_set_text()
        self.combobox_ui()

        self.apply_styles()  # 스타일 적용
        self.load_images()   # 이미지 적용
        self.setup_ui()
    
    def setup_ui(self):
        """UI 요소 스타일 및 이벤트 설정"""
        self.apply_styles_text()
        self.setup_events()



    def click_connect(self):
        """clicked.connect() 모음"""
        self.ui.pushButton_publish.clicked.connect(self.maya_file_manager.to_publish)
        self.ui.pushButton_screen.clicked.connect(self.playblast_handler.screen_shot)
        self.ui.pushButton_playblast.clicked.connect(self.playblast_handler.run_playblast)

    def label_set_text(self):
        """label setText() 모음"""
        self.ui.label_works_info.setText(self.maya_path_manager.works_info)
        self.ui.label_step.setText(self.maya_path_manager.step)
        self.ui.label_pub_path.setText(self.maya_path_manager.no_dot_ext_pub_path)

    def combobox_ui(self):
        """ComboBox 관련 메서드"""
        self.combo_ext = self.ui.comboBox_ext
        self.ext_list = [".ma", ".mb"]
        self.combo_ext.addItems(self.ext_list)

        """현재 파일의 확장자를 디폴트로 ComboBox에 나오도록 설정"""
        for combo_item in self.ext_list:
            if self.maya_path_manager.ext == combo_item:
                self.combo_ext.setCurrentText(combo_item)
                break

    def apply_styles(self):

        """UI 스타일을 설정하는 함수"""

        button_style_2 = """
            QPushButton {
                border: 2px solid #fdcb01;
                border-radius: 10px;
                padding: 8px;
                font: bold 18px "Comic Sans MS";
                background-color: #FFF8DC;
                color: #333333;
            }
            QPushButton:hover {
                background-color: #feeca4;
                border: 2px solid #feeca4;
            }
            QPushButton:pressed {
                background-color: #fdd835;
                border: 2px solid #fbc02d;
            }
        """

        label_style_logo = """
            QLabel {
                font-family: "Comic Sans MS", cursive, sans-serif;
                font-size: 50px;
                color: #white;
            }
        """
        
        label_style_1 = """
            QLabel {
                font-family: "Comic Sans MS", cursive, sans-serif;
                font-size: 20px;
                font-weight: bold;
                color: #fdcb01;
            }
        """

        label_style_2 = """
            QLabel {
                font-family: "Comic Sans MS", cursive, sans-serif;
                font-size: 22px;
                color: #fdcb01;
            }
        """

        label_style_3 = """
            QLabel {
                font-family: "Comic Sans MS", cursive, sans-serif;
                font-size: 18px;
                color: #FFF8DC;
            }
        """
        combo_box_style = """
            QComboBox {
                border: 2px solid #fdcb01;
                border-radius: 8px;
                padding: 5px;
                background-color: #feeca4;
                color: #111111;
                font: 19px "Comic Sans MS";
            }
            QComboBox:hover {
                background-color: #faefc1;
            }
            QComboBox::drop-down {
                border: none;
                background: #fdcb01;
                border-radius: 4px;
            }
            QComboBox QAbstractItemView {
                background: #FFF8DC;
                border: 2px solid #fdcb01;
                color: #555555;
                selection-background-color: #faefc1;
            }
        """        

        line_style = """
            QFrame {
                background: qlineargradient(
                    spread: pad, 
                    x1: 0, y1: 0, 
                    x2: 1, y2: 0, 
                    stop: 0 #ff9800, 
                    stop: 1 #FFF8DC
                ); /* 부드러운 그라디언트 효과 */
                border-radius: 2px; /* 둥근 테두리 */
            }

            QFrame:horizontal {
                min-height: 1px;
                max-height: 1px; /* 강제로 높이를 1px로 고정 */
            }

            QFrame:vertical {
                min-width: 1px;
                max-width: 1px; /* 강제로 폭을 1px로 고정 (세로선) */
            }
        """

        text_edit_style = """
            QTextEdit {
                border: 2px solid #fdcb01;
                border-radius: 10px;
                padding: 5px;
                font: bold 16px "Comic Sans MS";
                background-color: #FFF8DC;
                color: #333333;
            }
            QTextEdit:focus {
                border: 2px solid #FFF8DC;
                background-color: #feeca4;
            }
        """


        # 스타일 적용 (각 UI 요소에 설정 적용)       
        self.ui.pushButton_publish.setStyleSheet(button_style_2)
        self.ui.pushButton_playblast.setStyleSheet(button_style_2)
        
        self.ui.label_logo.setStyleSheet(label_style_logo) 

        self.ui.label_text_1.setStyleSheet(label_style_1)
        self.ui.label_text_2.setStyleSheet(label_style_1)
        self.ui.label_text_3.setStyleSheet(label_style_1)

        self.ui.label_text_4.setStyleSheet(label_style_2)
        self.ui.label_text_5.setStyleSheet(label_style_2)

        self.ui.label_works_info.setStyleSheet(label_style_3)
        self.ui.label_step.setStyleSheet(label_style_3)
        self.ui.label_pub_path.setStyleSheet(label_style_3) 

        self.ui.comboBox_ext.setStyleSheet(combo_box_style) 
        
        self.ui.line_horizontal_1.setStyleSheet(line_style)
        self.ui.line_horizontal_2.setStyleSheet(line_style)
        self.ui.line_horizontal_3.setStyleSheet(line_style)
        self.ui.line_horizontal_4.setStyleSheet(line_style)

        self.ui.line_vertical_1.setStyleSheet(line_style)
        self.ui.line_vertical_2.setStyleSheet(line_style)
        self.ui.line_vertical_3.setStyleSheet(line_style)
        self.ui.line_vertical_4.setStyleSheet(line_style)

#######################################################################

    def apply_styles_text(self):
        """텍스트 UI 스타일을 설정하는 함수"""

        # 버튼 스타일
        button_style_1 = """
            QPushButton {
                border: 2px solid #fdcb01;
                border-radius: 10px;
                padding: 8px;
                font: bold 18px "Comic Sans MS";
                background-color: #FFF8DC;
                color: #333333;
            }
            QPushButton:hover {
                background-color: #feeca4;
                border: 2px solid #feeca4;
            }
            QPushButton:pressed {
                background-color: #fdd835;
                border: 2px solid #fbc02d;
            }
        """

        # QTextEdit 스타일 (기존 스타일 유지)
        text_edit_style = """
            QTextEdit {
                border: 2px solid #fdcb01;
                border-radius: 10px;
                padding: 5px;
                font: bold 16px "Comic Sans MS";
                background-color: #FFF8DC;
                color: gray;
            }
            QTextEdit:focus {
                border: 2px solid #FFF8DC;
                background-color: #feeca4;
                color: black;
            }
        """

        self.ui.pushButton_screen.setStyleSheet(button_style_1)        
        self.ui.textEdit_description.setStyleSheet(text_edit_style)

        # 기본 텍스트 설정
        self.ui.pushButton_screen.setText("Click me")
        self.ui.textEdit_description.setPlainText("텍스트 입력")

    def setup_events(self):
        """버튼 및 텍스트 이벤트 설정"""
        self.ui.pushButton_screen.clicked.connect(self.clear_button_text)
        self.ui.textEdit_description.textChanged.connect(self.clear_text_hint)
        self.ui.textEdit_description.focusOutEvent = self.restore_text_hint

    def clear_button_text(self):
        """버튼을 클릭하면 텍스트 제거 및 아이콘 초기화"""
        self.ui.pushButton_screen.setText("")  # 버튼 텍스트 제거
        self.ui.pushButton_screen.setIcon(self.playblast_handler.change_button)  # 아이콘 제거
        self.ui.pushButton_screen.setIcon(Qicon())  # 아이콘 제거


    def clear_text_hint(self):
        """사용자가 텍스트 입력 시 힌트 자동 제거"""
        if self.ui.textEdit_description.toPlainText() == "텍스트 입력":
            self.ui.textEdit_description.clear()  # 기본값 제거
            self.ui.textEdit_description.setStyleSheet("""
                QTextEdit {
                    border: 2px solid #fdcb01;
                    border-radius: 10px;
                    padding: 5px;
                    font: bold 16px "Comic Sans MS";
                    background-color: #FFF8DC;
                    color: black;
                }
            """)

    def restore_text_hint(self, event):
        """텍스트 필드가 포커스를 잃으면 힌트 복원"""
        if not self.ui.textEdit_description.toPlainText().strip():
            self.ui.textEdit_description.setPlainText("텍스트 입력")
            self.ui.textEdit_description.setStyleSheet("""
                QTextEdit {
                    border: 2px solid #fdcb01;
                    border-radius: 10px;
                    padding: 5px;
                    font: bold 16px "Comic Sans MS";
                    background-color: #FFF8DC;
                    color: gray;
                }
            """)


    def load_images(self):
        """QLabel에 이미지 로드 및 크기 조절 (비율 유지 + 고화질 변환)"""

        self.im_01 = QPixmap("/nas/Batz_Maru/pingu/imim/publish/logo.png")
        self.im_02 = QPixmap("/nas/Batz_Maru/pingu/imim/publish/leave_work.png")
        self.im_03 = QPixmap("/nas/Batz_Maru/pingu/imim/publish/publish_right.png")

        # QLabel 크기 가져오기
        size_1 = self.ui.label_image_1.size()
        size_2 = self.ui.label_image_2.size()
        size_3 = self.ui.label_image_3.size()

        # 이미지 크기 조정 (비율 유지 + 고화질 변환)
        self.ui.label_image_1.setPixmap(self.im_01.scaled(size_1, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.ui.label_image_2.setPixmap(self.im_02.scaled(size_2, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.ui.label_image_3.setPixmap(self.im_03.scaled(size_3, Qt.KeepAspectRatio, Qt.SmoothTransformation))





class MayaFileManager(MayaPathManager):
    """Maya 씬을 관리하고 저장 및 내보내기 기능을 제공하는 클래스"""
    """절대경로를 기반으로 했기에 상대경로 사용시 오류발생"""

    def __init__(self, pub_app_manager):
        super().__init__(pub_app_manager)
        self.pub_app_manager = pub_app_manager
        self.pub_app_ui = pub_app_manager.ui
        self.pub_app_result = {}


    def to_publish(self):
        """
        Publish 버튼을 누르면 발동하는 메서드
        현재 파일 저장후 pub 파일로 복사
        """
        print("to publish 함수 실행")

        # User가 선택한 확장자 [ma, mb]
        self.selected_ext = self.ui.comboBox_ext.currentText()
        print(f" selected ext : {self.selected_ext}")
        # work 경로에 있는 파일
        self.work_output_path = self.no_dot_ext_work_path + self.selected_ext
        print(f" work output path :{self.work_output_path}")

        """User가 선택한 확장자로 work경로에서 저장후"""
        cmds.file(rename = self.work_output_path)
        if self.selected_ext == ".ma":
            cmds.file(save=True, type = 'mayaAscii')
        elif self.selected_ext == ".mb":
            cmds.file(save=True, type = 'mayaBinary')

        if not os.path.exists(self.work_output_path):
            print("그딴 파일 없어요")
            return
        
        # pub경로에 생성되는 파일
        self.pub_file_path = self.no_dot_ext_pub_path + self.selected_ext
        print(f"pub file_path : {self.pub_file_path}")

        """Pub경로로 복사"""
        self.pub_parent_dir = os.path.dirname(self.pub_file_path)

        print("파일 복사중~~~~~~~~~")
        shutil.copy(self.work_output_path, self.pub_file_path) # 파일 복사

        print(f"파일 복사 완료: {self.pub_file_path}")


        print("exrpot pub abc 실행")
        self.export_pub_abc()

    def export_pub_abc(self):
        """
        cache경로로 abc Export
        파일명은 User가 선택한 object 네이밍

        cache Path : /nas/Batz_maru/Jupiter/cache/char_spino_animation/v001/spino.abc
                                                        /{works_info}/{file_ver}/{user_select_object_name}
        """
        # 경로가 존재하지 않으면 생성
        if not os.path.exists(self.cache_parent_dir):
            print(f"경로가 존재하지 않음. 자동 생성 중: {self.cache_parent_dir}")
            os.makedirs(self.cache_parent_dir)
            print(f"경로 생성 완료 : {self.cache_parent_dir}")

        # Alembic 캐시 리스트 초기화
        self.pub_cache_list = []

        # 기존 Alembic 파일 리스트 가져오기
        try:
            self.cache_files = os.listdir(self.cache_parent_dir)
        except FileNotFoundError as e:
            print(f"폴더를 찾을 수 없음: {e}")
            self.cache_files = []  # 폴더가 없어서 리스트를 가져올 수 없으면 빈 리스트 반환

        # 기존 Alembic 파일들을 pub_cache_list에 추가
        for cache_file in self.cache_files:
            if cache_file.endswith(".abc"):
                self.pub_cache_list.append(os.path.join(self.cache_parent_dir, cache_file))

        # 선택된 오브젝트 가져오기
        self.user_selection = cmds.ls(selection=True)[0]

        if not self.user_selection:
            cmds.warning("선택된 오브젝트가 없습니다.")
            return

        # 선택된 첫 번째 오브젝트 기준으로 파일명 설정
        object_name = self.user_selection
        object_name = object_name.replace("|", "_")  # 네임스페이스 충돌 방지
        object_name = object_name.replace(":", "_")  # 네임스페이스 충돌 방지

        # Abc 경로
        self.abc_file = os.path.join(self.cache_parent_dir, f"{object_name}.abc")


        start_frame = int(cmds.playbackOptions(q=True,min=True))
        end_frame = int(cmds.playbackOptions(q=True,max=True))

        #알렘빅 캐쉬 옵션 설정
        cmd = f"-frameRange {start_frame} {end_frame} "
        cmd += "-uvWrite "
        cmd += "-worldSpace "
        cmd += "-renderableOnly "

        #추가한 커스텀 어트리뷰트 이름 추가
        cmd += "-attr assettype "

        #오브젝트 추가 부분
        cmd += f"-root {self.user_selection} "

        #파일 저장 경로
        cmd += f"-file {self.abc_file}"
        cmds.AbcExport(jobArg=cmd)

        print("Cache경로에 Alembic Cache파일이 생성이 완료되었습니다.")
        print(f"{self.abc_file}")

        import time
        # 파일이 실제로 생성될 때까지 대기
        wait_time = 5
        while not os.path.exists(self.abc_file) and wait_time < 10:  # 최대 10초 대기
            time.sleep(0.5)
            wait_time += 0.5

        # 파일이 정상적으로 생성되었는지 확인 후 리스트에 추가
        if os.path.exists(self.abc_file):
            self.pub_cache_list.append(self.abc_file)
            print("Cache경로에 Alembic Cache파일이 생성이 완료되었습니다.")
            print(f"{self.abc_file}")
        else:
            print(f" Alembic 파일이 정상적으로 생성되지 않았습니다: {self.abc_file}")
            return  # 파일이 생성되지 않았다면 이후 로직을 실행하지 않음



        # 선택해제
        cmds.select(clear=True)

        self.make_pub_data_dic()
        # PublishAppManager에 전달

    def make_pub_data_dic(self):
        print(" make_pub_data_dic 실행됨")

        # 기존 데이터를 유지하면서 pub_cache_list 업데이트

        if not hasattr(self, 'pub_cache_list'):
            self.pub_cache_list = []

        for cache_file in self.cache_files:
            if cache_file.endswith(".abc"):
                self.cache_file_name = cache_file
                self.full_cache_path = os.path.join(self.cache_parent_dir, self.cache_file_name)
                self.pub_cache_list.append(self.full_cache_path)

        # # Shot Grid로 보내기 위한 디스크립션
        # self.user_comment_des = self.pub_app_ui.textEdit_description.toPlainText().strip()

        # # PlayblastHandler에서 thumb_path 가져오기
        # if hasattr(self.pub_app_manager.playblast_handler, 'thumb_path'):
        #     self.thumb_path = self.pub_app_manager.playblast_handler.thumb_path
        # else:
        #     self.thumb_path = None  # 썸네일이 없을 경우 None 처리

        # # PlayblastHandler에서  confirm_mov_path 가져오기
        # if hasattr(self.pub_app_manager.playblast_handler, 'confirm_mov_path'):
        #     self.confirm_mov_path = self.pub_app_manager.playblast_handler.confirm_mov_path
        # else:
        #     self.confirm_mov_path= None  # 썸네일이 없을 경우 None 처리

        # # Publish하면서 나온 Data들의 딕셔너리 생성
        # self.pub_app_result = {}

        # Shot Grid로 보낼 description 가져오기
        self.user_comment_des = self.pub_app_ui.textEdit_description.toPlainText().strip()

        # PlayblastHandler에서 썸네일 경로 가져오기
        self.thumb_path = getattr(self.pub_app_manager.playblast_handler, 'thumb_path', None)
        self.confirm_mov_path = getattr(self.pub_app_manager.playblast_handler, 'confirm_mov_path', None)

        # #  필수 데이터가 None일 경우 기본값 추가
        # if self.pub_cache_list is None:
        #     self.pub_cache_list = []
        # if self.pub_file_path is None:
        #     self.pub_file_path = "Unknown_Maya_File.ma"
        # if self.confirm_mov_path is None:
        #     self.confirm_mov_path = "Unknown_Mov_File.mov"
        # if self.thumb_path is None:
        #     self.thumb_path = "Unknown_Thumbnail.jpg"


        # Pub Info
        self.pub_app_result["pub_info"] = {
                            'version': self.file_ver,
                            'description' : self.user_comment_des
                            }
        # Pub Files
        self.pub_app_result["pub_files"] = {
                            "Confirm_mov" : self.confirm_mov_path,      # SG Versions  엔티티
                            "pub_maya" : self.pub_file_path,            # SG Publishes 엔티티
                            "Thumbnail_jpg" : self.thumb_path,          # SG Publishes 엔티티
                            "Cache_abc_list" : self.pub_cache_list      # SG Publishes 엔티티 # cache 파일 리스트
                                }

        print(f"생성된 pub_data: {self.pub_app_result}")

        self.pub_app_manager.receive_pub_data(self.pub_app_result)




class PlayBlastHandler(MayaPathManager):
    """
    Playblast 관련 기능들 class
    
    Directory : EXT
    스크린샷
    thumbnail : jpg,
    
    플레이블라스트 (영상) 
    confirm : mov
    """

    def __init__(self, pub_app_manager):
            super().__init__(pub_app_manager)
            self.ui = pub_app_manager.ui

    def screen_shot(self):
        # 썸네일 path 정의
        self.define_thumbnail_path()

        cmds.playblast(
            format="image",
            filename=self.thumb_path,        # 절대경로 (파일확장자까지)
            frame=cmds.currentTime(q=True),  # 현재 프레임 캡처
            viewer=False,                    # 뷰어 자동 실행 X
            clearCache=True,                 # 이전 버퍼 삭제
            showOrnaments=False,             # HUD 정보 제거
            forceOverwrite=True,             # 기존 파일 덮어쓰기 허용
            percent=100,                     # 100% 해상도
            compression="jpg",               # jpg 형식으로 저장
            widthHeight=(1920, 1080),        # 이미지 해상도 설정
            framePadding=0                   # 자동으로 0000 붙는 것 방지
        )

        # Jupiter_Character_Spino_Model_v019_thumb.jpg.0.jpg 로저장되는 이슈

        # 파일명 변경
        saved_file = self.thumb_path + ".0.jpg"  # Maya가 저장한 파일명
        if os.path.exists(saved_file):
            os.rename(saved_file, self.thumb_path)

        # 만약 썸네일 로딩이 오래걸리면 풀기
        # wait_time = 0
        # while not os.path.exists(self.thumb_path) and wait_time < 1:
        #     time.sleep(0.1)
        #     wait_time += 0.1

        print(f"스크린샷 저장: {self.thumb_path}")
        self.change_button()


    def change_button(self):
        """스크린샷이 저장된 후 버튼의 아이콘을 변경"""

        # 썸네일 path 정의
        self.define_thumbnail_path()

        if not os.path.exists(self.thumb_path):
            print(f"이미지 파일이 존재하지 않습니다: {self.thumb_path}")
            return

        pixmap = QPixmap(self.thumb_path)

        if pixmap.isNull():
            print(f"QPixmap이 이미지를 로드하지 못했습니다: {self.thumb_path}")
            return
        

        self.ui.pushButton_screen.setIcon(QIcon())
        icon = QIcon(pixmap)
        self.ui.pushButton_screen.setIcon(icon)
        self.ui.pushButton_screen.setIconSize(self.ui.pushButton_screen.size())
        print(f"버튼 이미지 변경 완료!")
    
    def run_playblast(self):
        """
        시퀀스 : 렌더세팅에 맞춰 렌더
        Asset : 턴테이블
        """

        # Confirm Playblast 저장 경로가 존재하지 않면 생성
        if not os.path.exists(self.confirm_mov_dir):
            os.makedirs(self.confirm_mov_dir)
            print(f"Confirm mov 폴더 생성: {self.confirm_mov_dir}")

        if not os.path.exists(self.confirm_img_seq_dir):
            os.makedirs(self.confirm_img_seq_dir)
            print(f"Confirm 이미지 시퀀스 폴더 생성: {self.confirm_img_seq_dir}")

        if self.pattern_key == "maya_seq":
            # self.seq_mov_playblast()
            print("Seq 팀: 렌더 설정을 이용한 플레이블라스트 실행")
            self.seq_mov_playblast()
        
        elif self.pattern_key == "maya_asset":
            print("Asset 팀: 턴테이블 플레이블라스트 실행")
            self.asset_turn_table()
            
        else:
            print("Playblast Error (step 매칭): 파일명, 경로를 재확인 해주세요")
            return

    def seq_mov_playblast(self):
        """Seq 팀 : 렌더 설정 기반 mov 플레이블라스트"""
        
        camera = self.get_selected_camera()
        if not camera:
            return
        
        # # Render Settings 확인
        # is_jpg = self.get_camera_render_settings(camera)

        width = cmds.getAttr("defaultResolution.width")
        height = cmds.getAttr("defaultResolution.height")
        print(f"Render Resolution: {width} x {height}")

        cmds.playblast(
            format="image",
            filename=self.confirm_img_seq_name,
            sequenceTime=False,
            clearCache=True,
            viewer=False,
            showOrnaments=False,
            offScreen=True,
            fp=4,
            percent=100,
            quality=100,
            compression="jpg", # if is_jpg else "png",  # JPG 또는 PNG 설정
            widthHeight=(width, height)
        )

        print(f"Seq팀 Playblast 저장 : {self.confirm_img_seq_name}")
        self.ffmpeg_convert_to_mov()


    def get_selected_camera(self):
        """현재 선택된 카메라 가져오기"""
        self.selected_camera = cmds.ls(selection=True, type="transform")
        if not self.selected_camera:
            cmds.warning("카메라를 선택해주세요.")
            return None
        
        # 선택된 오브젝트 중에서 카메라 찾기
        for obj in self.selected_camera:
            shapes = cmds.listRelatives(obj, shapes=True, type="camera")
            if shapes:
                return obj  # 변환 노드를 반환
        
        cmds.warning("선택된 오브젝트가 카메라가 아닙니다.")
        return None


    def get_camera_render_settings(self, selected_camera):
        """해당 카메라의 Render Settings에서 포맷을 확인"""
        render_globals = "defaultRenderGlobals"
        
        # 현재 렌더 포맷 확인 (기본 렌더 설정에서 가져옴)
        render_format = cmds.getAttr(f"{render_globals}.imageFormat")  # 8: JPG, 32: EXR, 51: PNG 등
        
        # 렌더 설정이 JPG라면 True 반환
        return render_format == 8  



    def asset_turn_table(self):
        """Asset 팀 : 턴테이블"""

        self.create_turntable_animation()

        cmds.playblast(
            format="image",
            filename=self.confirm_img_seq_name,
            sequenceTime=False,
            clearCache=True,
            viewer=False,
            showOrnaments=False,
            fp=4,
            percent=100,
            compression="jpg",
            forceOverwrite=True
        )

        self.ffmpeg_convert_to_mov()

        self.undo_original(steps=7) # Undo (Ctrl + Z) 7번

    def undo_original(self, steps=int):
        """지정된 횟수만큼 Undo 실행 (기본 7회)"""
        for _ in range(steps):
            cmds.undo()


    def create_turntable_animation(self, duration=200):
        """현재 뷰포트에 있는 오브젝트를 턴테이블 회전 애니메이션 추가 """

        cmds.playbackOptions(min=1, max=200, animationStartTime=1, animationEndTime=200)

        visible_objects = cmds.ls(visible=True, transforms=True)
        # if not visible_objects:
        #     print("현재 뷰포트에 보이는 오브젝트가 없습니다.")
        #     return

        turntable_grp = "Turntable_Group"
        
        if cmds.objExists(turntable_grp):
            # 그룹 내부의 모든 오브젝트 찾기
            children = cmds.listRelatives(turntable_grp, children=True, fullPath=True) or []
            
            if children:
                cmds.parent(children, world=True) #(Unparent)

            cmds.delete(turntable_grp)
            print(f"기존 그룹 삭제 완료: {turntable_grp}")

        # 새로운 턴테이블 그룹 생성
        cmds.group(visible_objects, name=turntable_grp)
        print(f"새로운 그룹 생성 완료: {turntable_grp}")

        start_frame = cmds.playbackOptions(q=True, min=True)
        end_frame = start_frame + duration

        cmds.setKeyframe(turntable_grp, attribute="rotateY", t=start_frame, v=0)
        cmds.setKeyframe(turntable_grp, attribute="rotateY", t=end_frame, v=360)

        cmds.select(turntable_grp)
        cmds.keyTangent(turntable_grp, attribute="rotateY", inTangentType="linear", outTangentType="linear")

        cmds.select(clear=True) # 선택해제
        print(f" 턴테이블 애니메이션 생성 완료 ({duration} 프레임 동안 360도 회전)")

    def ffmpeg_convert_to_mov(self):
        """
        이미지 시퀀스를 MOV 파일로 변환하는 메서드.
        - self.confirm_ffmpeg_jpg (ffmpeg에서 사용 가능한 %04d 형식) 활용
        - 변환된 MOV 파일은 self.confirm_mov_path에 저장됨
        - ffmpeg 실행 후 RV로 MOV 파일 자동 재생 가능
        """

        # 이미지 시퀀스가 저장된 폴더 생성 (존재하지 않으면)
        if not os.path.exists(self.confirm_img_seq_dir):
            os.makedirs(self.confirm_img_seq_dir)
            print(f"이미지 시퀀스 폴더 생성: {self.confirm_img_seq_dir}")


        # ffmpeg 명령어 생성
        ffmpeg_cmd = [
            "ffmpeg",
            "-framerate", "24",  # 기본 프레임 레이트 (필요 시 변경)
            "-i", self.confirm_ffmpeg_jpg,  # %04d 형식의 이미지 시퀀스
            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",  # 해상도를 자동으로 2의 배수로 변환
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-y",  # 기존 파일 덮어쓰기
            self.confirm_mov_path  # 최종 MOV 파일 경로
        ]



        try:
            print(f"🔹 ffmpeg 변환 시작: {self.confirm_mov_path}")
            result = subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True)
            print(f"✅ ffmpeg 변환 완료: {self.confirm_mov_path}")
            print("📜 FFmpeg 출력 로그:")
            print(result.stdout)

        except subprocess.CalledProcessError as e:
            print(f"❌ ffmpeg 변환 실패: {e}")
            print("🔍 FFmpeg 에러 로그:")
            print(e.stderr)
            return
        # 변환된 MOV 파일을 RV로 재생할지 여부 확인 후 실행
        self.play_playblast()

    def play_playblast(self):
        """RV로 mov 재생"""

        os.environ["PATH"] += os.pathsep + "/usr/local/bin"

        if not os.path.exists(self.confirm_mov_path):
            print(f"변환된 MOV 파일을 찾을 수 없습니다: {self.confirm_mov_path}")
            return

        rv_path = "rv"  # 환경변수를 추가했으므로 rv 명령어만 실행 가능

        try:
            print(f"RV 실행: {rv_path} {self.confirm_mov_path}")
            subprocess.Popen([rv_path, "-play", self.confirm_mov_path])
            # subprocess.run([rv_path, self.confirm_mov_path], check=True)
        except Exception as e:
            print(f"RV 실행 실패: {e}")





if __name__=="__main__":
    app = QApplication()
    w = PublishAppManager()
    app.exec_()