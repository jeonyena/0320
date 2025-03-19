"""
from importlib import reload
import sys

sys.path.append("/nas/Batz_Maru/pingu/nana/03_20/kec/yenyaong")
import loader_3011_v1
reload(loader_3011_v1)
w = loader_3011_v1.MainCtrl()
# w.show()
"""

try:
    from PySide6.QtWidgets import QMainWindow, QApplication, QMenu
    from PySide6.QtWidgets import QVBoxLayout, QGridLayout, QTreeWidget, QTableWidgetItem
    from PySide6.QtWidgets import QHBoxLayout, QLabel, QComboBox, QTreeWidgetItem
    from PySide6.QtWidgets import QPushButton, QWidget, QHeaderView, QListWidgetItem
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtGui import QPixmap, QCursor
    from PySide6.QtCore import Qt, QFile, QSize, QObject
    from PySide6.QtGui import QIcon, QColor, QFontMetrics 
    from PySide6.QtGui import QStandardItemModel, QStandardItem
    import shutil
except:
    from PySide2.QtWidgets import QMainWindow, QApplication, QMenu
    from PySide2.QtWidgets import QVBoxLayout, QGridLayout, QTreeWidget, QTableWidgetItem
    from PySide2.QtWidgets import QHBoxLayout, QLabel, QComboBox, QTreeWidgetItem
    from PySide2.QtWidgets import QPushButton, QWidget, QHeaderView, QListWidgetItem
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtGui import QPixmap, QCursor
    from PySide2.QtCore import Qt, QFile, QSize, QObject
    from PySide2.QtGui import QIcon, QColor, QFontMetrics 
    from PySide2.QtGui import QStandardItemModel, QStandardItem
    import maya.cmds as cmds
    import shutil

import os
import json

from shotgun_api3 import Shotgun
import sg_api

class MainCtrl(QMainWindow):
    def __init__(self):
        super().__init__()
        self.root_path = "/nas/Batz_Maru"

        json_path = "/nas/Batz_Maru/pingu/nana/merge/user_info.json"
        with open(json_path,'r', encoding='utf-8') as f:
            user_info = json.load(f)
            user_id = user_info['id']

        project_name = "Jupiter"    
        self.path_manager = sg_api.MyTask(user_id, project=project_name)
        folders = self.path_manager.display_folders()

        self.load_ui()
        self.center_window()

        self.UISetup = UISetup(self.ui)
        self.UtilityMgr = UtilityMgr(self.ui, self.ui.treeWidget)
        self.TreeMgr = TreeMgr(self.ui.treeWidget, self.ui.treeWidget_task, folders, self.root_path, self.UtilityMgr, self.ui)
        self.TableMgr = TableMgr(self.ui, self.ui.treeWidget, self.ui.treeWidget_task, self.ui.tableWidget, self.ui.label_path, folders, self.root_path)
        self.MayaMgr = MayaMgr(self.TableMgr)
        self.ButtonMgr = ButtonMgr(self.ui, self.TableMgr, self.TreeMgr, self.root_path, self.UISetup, self.MayaMgr)  
        self.ShotGridMgr = ShotGridMgr(self.path_manager)
        self.SubUISetup = SubUISetup(self.ui, self.TableMgr, self.ui.label_path, self.path_manager, self.ShotGridMgr)

        self.ui.installEventFilter(self)

    def center_window(self):
        """UI를 화면 중앙에 배치하는 함수"""
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        ui_geometry = self.ui.frameGeometry()
        center_point = screen_geometry.center()

        ui_geometry.moveCenter(center_point)
        self.ui.move(ui_geometry.topLeft())

    def eventFilter(self, obj, event):
        """창 크기 변경 시 TableMgr의 resize_window 실행"""
        if obj == self.ui and event.type() == event.Resize:
            self.TableMgr.resize_window()
        return super().eventFilter(obj, event)

    def load_ui(self):
        ui_file_path = "/nas/Batz_Maru/pingu/nana/03_14/kec/kec_loaderUI_0313.ui"
        ui_file = QFile(ui_file_path)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        self.ui.show()
        ui_file.close()

class ShotGridMgr:
    def __init__(self, path_manager):
        self.path_manager = path_manager
        self.current_task = None
        self.task_dict = {}
        # self.set_task_name()

    # def set_task_name(self):
    #     # self.task_name = task_name
    #     # print(f"current task : {self.task_name}")
    #     ep, shotnum, step = self.task_name.split('_')
    #     print(ep)
    #     print(shotnum)
    #     print(step)

    
    # def set_task_name(self, task_name):
    #     self.current_task = task_name
    #     print (f"확인용으로 자르게{self.current_task}")

    #     parts = self.current_task.split("_")
    #     self.extracted_value_0 = parts[0]
    #     self.extracted_value_1 = parts[1]  # 두 번째 값(인덱스 1) 추출
    #     self.extracted_value_2 = parts[2]
    #     print (f"가운데수뽑기{self.extracted_value_0}")
    #     print (f"가운데수뽑기{self.extracted_value_1}")
    #     print (f"가운데수뽑기{self.extracted_value_2}")
    #     self.load_tasks()

    def set_task_name(self, task_name):
        self.current_task = task_name
        parts = self.current_task.split("_")
        self.extracted_value_1 = parts[1]
        print (f"확인용으로 자르게{self.extracted_value_1}")
        
        self.load_tasks()

    def load_tasks(self):
        tasks = self.path_manager.get_tasks()

        task_dict = {}
        for task in tasks:
            entity_name = task["entity"]["name"]
            step_name = task["step"]["name"]
            entity_type = task["entity"]["type"]
            # entity = self.entities.get(entity_name)
            task_name = f"{entity_name}_{step_name}" if entity_type == "Shot" else f"{entity_name}_{task['content']}_{step_name}"
            # task_name = f"{entity_name}_{entity['sg_asset_type']}_{step_name}" if entity_type == "Shot" else f"{entity_name}_{task['content']}_{step_name}"
            # task_name = f"{self.extracted_value_0}_{self.extracted_value_1}_{self.extracted_value_2}" if entity_type == "Shot" else f"{entity_name}_{task['content']}_{step_name}"

            task_dict[task_name] = {
                "start_date": task["start_date"],
                "due_date": task["due_date"],
                "duration": task["duration"],
                "entity_type": entity_type,
                "description": task.get("sg_description", "N/A"),
            }

        self.task_dict = task_dict  # 저장해서 이후 검색 가능
        self.pull_task_info(self.current_task)
        print(f"테스크 분류 결과: {self.task_dict}")

    def pull_task_info(self, current_task):
        matched_task = self.task_dict.get(current_task)
        if matched_task:
            return [
                f"Sta_Date : {matched_task['start_date']}",
                f"Due_Date : {matched_task['due_date']}",
                f"Duration : {matched_task['duration']} days",
                f"Description : {matched_task['description']}",
            ]
        return []

class MayaMgr:
    def __init__(self, table_mgr):
        self.table_mgr = table_mgr

        self.table_mgr.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_mgr.tableWidget.customContextMenuRequested.connect(self.show_menu)
    
    def show_menu(self, position):

        # 테이블위젯 좌표값
        item = self.table_mgr.tableWidget.itemAt(position)
        self.selected_item = item.text()
        
        menu = QMenu()

        open_action = menu.addAction("Open")
        import_action = menu.addAction("Import")
        reference_action = menu.addAction("Reference")

        # QAction이 실행되었을 때 실행할 함수 연결
        open_action.triggered.connect(self.maya_open)
        import_action.triggered.connect(self.maya_import)
        reference_action.triggered.connect(self.maya_reference)

        menu.exec_(self.table_mgr.tableWidget.viewport().mapToGlobal(position))

    def maya_open(self):
        file_path = os.path.join(self.table_mgr.current_folder, self.selected_item)

        if os.path.exists(file_path):
            file_extension = os.path.splitext(file_path)[-1].lower()
            file_type = "mayaAscii" if file_extension == ".ma" else "mayaBinary"

            print(f"✅ Import 실행: {file_path}")
            cmds.file(file_path, open=True, force=True, type=file_type, ignoreVersion=True, options="v=0;")


    def maya_import(self):
        file_path = os.path.join(self.table_mgr.current_folder, self.selected_item)

        if os.path.exists(file_path):
            file_extension = os.path.splitext(file_path)[-1].lower()
            file_type = "mayaAscii" if file_extension == ".ma" else "mayaBinary"

            print(f"✅ Import 실행: {file_path}")
            cmds.file(file_path, i=True, type=file_type, ignoreVersion=True, ra=True, mergeNamespacesOnClash=False, options="v=0;", pr=True, importFrameRate=True)

    def maya_reference(self):
        file_path = os.path.join(self.table_mgr.current_folder, self.selected_item)

        if not os.path.exists(file_path):
            print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
            return

        file_extension = os.path.splitext(file_path)[-1].lower()
        file_type = "mayaAscii" if file_extension == ".ma" else "mayaBinary"

        # 고유한 네임스페이스 생성 (중복 로딩 가능)
        namespace = os.path.splitext(self.selected_item)[0]  # 파일명 기반 네임스페이스

        # Maya Reference 실행 (강제 로드 가능)
        print(f"🔗 Reference 실행: {file_path}")
        cmds.file(file_path, reference=True, type=file_type, ignoreVersion=True, mergeNamespacesOnClash=False, options="v=0;", pr=True, namespace=namespace, force=True)

    # def maya_reference(self):
    #     file_path = os.path.join(self.table_mgr.current_folder, self.selected_item)

    #     if not os.path.exists(file_path):
    #         print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
    #         return

    #     file_extension = os.path.splitext(file_path)[-1].lower()
    #     file_type = "mayaAscii" if file_extension == ".ma" else "mayaBinary"

    #     # 🔥 Maya Reference 실행 (중복 체크 제거)
    #     print(f"🔗 Reference 실행: {file_path}")
    #     cmds.file(file_path, reference=True, type=file_type, ignoreVersion=True, mergeNamespacesOnClash=False, options="v=0;", pr=True)

class SubUISetup:
    def __init__(self, ui, table_mgr, label_path, path_manager, shotgrid_mgr):
        self.ui = ui
        self.table_mgr = table_mgr
        self.label_path = label_path 
        self.path_manager = path_manager
        self.shotgrid_mgr = shotgrid_mgr

        #self.show_sub()

        self.ui.treeWidget.itemClicked.connect(self.listWidget_info)
        self.ui.tableWidget.cellClicked.connect(self.tableWidget_info)
        self.ui.treeWidget_task.itemClicked.connect(self.listWidget_task_info)

    def tableWidget_info(self, row, column):
        sub_list_info = []

        # 파일명 가져오기
        item = self.ui.tableWidget.item(row, column)
        file_name = item.text().strip()
        sub_list_info.append(f"Name : {file_name}")

        # 경로 가져오기
        path_name = self.label_path.text().strip()
        project_name = path_name.split("/")[3]  
        sub_list_info.append(f"Project : {project_name}")  

        # 샷그리드에서 name에 맞는 날짜 가져오기
        file_name


        self.listWidget_sub(sub_list_info)

    def listWidget_task_info(self, item):
        
        sub_list_info = []
        
        file_name = item.text(0)

        sub_list_info.append(f"Name : {file_name}")
        self.shotgrid_mgr.set_task_name(file_name)
        result = self.shotgrid_mgr.pull_task_info(file_name)
        sub_list_info.extend(result)

        # result = self.shotgrid_mgr.pull_task_info()
        print (f"샷건자료넘어옴?{result}")


        # self.path_manager.pass_data(file_name, self.path_manager.entities)

        # sta_date = 
        # due_date = 
        # duration =
        # description = 
        
        # sub_list_info = []
        # sub_list_info.append(f"Name : {file_name}")
        # sub_list_info.append(f"Sta_Date : {sta_date}")
        # sub_list_info.append(f"Due_Date : {due_date}")
        # sub_list_info.append(f"Duration : {duration} days")
        # sub_list_info.append(f"Description : {description}")

        self.listWidget_sub(sub_list_info)

        # sub_list_info.append(f"Name : {file_name}")
        # sub_list_info.append(f"Sta_Date : {sta_date}")
        # sub_list_info.append(f"Due_Date : {due_date}")
        # sub_list_info.append(f"Duration : {duration}")
        # sub_list_info.append(f"Description : {description}")

        self.listWidget_sub(sub_list_info)


    def listWidget_info(self, item):
        
        sub_list_info = []
        
        file_name = item.text(0)
        sub_list_info.append(f"Name : {file_name}")
        self.listWidget_sub(sub_list_info)

    def shotgrid_info(self, item):
            
        sub_list_info = []

        # 파일 이름 추가
        file_name = item.text(0).strip()
        sub_list_info.append(f" Name : {file_name}")

        # 프로젝트 정보 추가
        project_name =  self.shotgrid_mgr.get_project_name()
        if project_name:
            sub_list_info.append(f" Project : {project_name}")

        # 샷 시작 날짜 추가
        shot_start_date = self.shotgrid_mgr.get_shot_start_date()
        if shot_start_date:
            sub_list_info.append(f" Start Date : {shot_start_date}")

        # 샷 마감 날짜 추가
        shot_due_date = self.shotgrid_mgr.get_shot_due_date()
        if shot_due_date:
            sub_list_info.append(f" Due Date : {shot_due_date}")

        # 샷 소요 기간 추가
        shot_duration = self.shotgrid_mgr.get_shot_duration()
        if shot_duration:
            sub_list_info.append(f" Duration : {shot_duration}")

        #  리스트 위젯 업데이트
        self.listWidget_sub(sub_list_info)
        
    # def listWidget_sub(self, list_info):
    #     self.ui.listWidget_sub.clear()
    #     self.ui.listWidget_sub.addItems(list_info) 
    def listWidget_sub(self, list_info):
        self.ui.listWidget_sub.clear()
        
        for info in list_info:
            item = QListWidgetItem(info)  # 각 항목을 QListWidgetItem으로 생성
            item.setToolTip(info)  # 툴팁 추가 (전체 내용 볼 수 있음)
            item.setWhatsThis(info)  # 추가 정보 저장 가능
            self.ui.listWidget_sub.addItem(item)
        
        self.ui.listWidget_sub.setWordWrap(True)  # 자동 줄 바꿈 활성화


    def show_sub(self):
        self.label_sub()


    def label_sub(self):
        sub_im = "/nas/Batz_Maru/pingu/imim/batzz.png"
        pixmap = QPixmap(sub_im)
        pixmap = pixmap.scaled(200, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation) 

        self.ui.label_sub.setPixmap(pixmap)  # QLabel에 이미지 설정
        self.ui.label_sub.setFixedSize(200, 180)  # QLabel 크기 고정
            


    def tableWidget_sub(self):
        pass

class TreeMgr:
    def __init__(self, tree_widget, tree_Widget_task, folders, root_path, utility_mgr, ui):

        self.tree_widget = tree_widget
        self.tree_Widget_task = tree_Widget_task
        self.folders = folders
        self.root_path = root_path
        self.utility_mgr = utility_mgr 
        self.ui = ui

        self.show_file()

    def show_file(self):
        self.tree_widget.setHeaderLabels(["Batz_Maru"])
        self.tree_Widget_task.setHeaderLabels(["Task"])

        folder_structure = self.get_folder(self.root_path)
        folder_structure_task = self.get_task()

        self.populate_tree(folder_structure, self.tree_widget)
        self.populate_tree(folder_structure_task, self.tree_Widget_task)

    def get_folder(self, path=None):

        if path is None:
            path = self.root_path
        
        folder_dict = {}
        
        if os.path.isdir(path):
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    folder_dict[item] = self.get_folder(full_path)
                    
        return folder_dict
    
    def get_task(self, task_paths=None):
        folder_dict_task = {}

        if task_paths is None:
            task_paths = self.folders

        for task_path in task_paths:  # task 폴더 하나씩 확인
            if os.path.isdir(task_path):  # 폴더인지 확인
                sub_folders = []  # 하위 폴더를 저장할 리스트

                # 현재 task 폴더 내 모든 항목 검사
                for item in os.listdir(task_path):
                    full_path = os.path.join(task_path, item)  # 전체 경로 생성

                    if os.path.isdir(full_path):  # 폴더인지 확인
                        sub_folders.append(full_path)  # 리스트에 추가

                # 현재 task 폴더를 키로 추가하고, 하위 폴더를 저장
                folder_name = os.path.basename(task_path)  # 폴더명만 추출
                folder_dict_task[folder_name] = {}  # 트리에는 폴더명만 표시

                for sub_folder in sub_folders:
                    sub_folder_name = os.path.basename(sub_folder)  # 하위 폴더명만 추출
                    folder_dict_task[folder_name][sub_folder_name] = {}  # 트리에는 이름만 표시

        return folder_dict_task

    def populate_tree(self, folder_dict, parent_item):
        """ 주어진 폴더 딕셔너리를 QTreeWidget에 추가하는 함수 """

        for folder, sub_folders in folder_dict.items():
            child_item = QTreeWidgetItem(parent_item)
            child_item.setText(0, folder)

            # 하위 폴더가 있으면 재귀적으로 추가
            self.populate_tree(sub_folders, child_item)

class ButtonMgr:
    def __init__(self, ui, tablemgr, tree_mgr, root_path, ui_setup, maya_mgr):
        self.ui = ui
        self.table_mgr = tablemgr
        self.tree_mgr = tree_mgr
        self.root_path = root_path 
        self.ui_setup = ui_setup 
        self.maya_mgr = maya_mgr


        self.history = []  # 클릭한 트리 항목 저장
        self.current_index = -1  # 현재 선택한 히스토리 위치

        self.ui.pushButton_home.clicked.connect(self.go_home)
        self.ui.pushButton_back.clicked.connect(self.go_back)
        self.ui.pushButton_front.clicked.connect(self.go_front)

        # 항목 클릭 시 경로 저장
        self.ui.treeWidget.itemClicked.connect(self.click_history)
        self.ui.comboBox_task.currentIndexChanged.connect(self.new_combo) 

        # self.ui.pushButton_luck.clicked.connect(self.view_list)
        self.ui.pushButton_list_menu.clicked.connect(self.view_list)
        self.ui.pushButton_icon_menu.clicked.connect(self.view_icon)
        
        # listView_button 우클릭
        self.ui.listView_button.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.listView_button.customContextMenuRequested.connect(self.show_menu)

    
    def show_menu(self, position):
        item = self.table_mgr.tableWidget.itemAt(position)
        
        if item is None:
            print("❌ 선택된 항목이 없음!")
            return

        self.selected_item = item.text()
        print(f"✅ 선택된 파일: {self.selected_item}")  # 디버깅용 출력

        menu = QMenu()
        open_action = menu.addAction("Open")
        open_action.triggered.connect(self.maya_open)

        menu.exec_(self.table_mgr.tableWidget.viewport().mapToGlobal(position))



    # def maya_open(self):
    #     file_path = os.path.join(self.table_mgr.current_folder, self.selected_item)

    #     if os.path.exists(file_path):
    #         file_extension = os.path.splitext(file_path)[-1].lower()
    #         file_type = "mayaAscii" if file_extension == ".ma" else "mayaBinary"

    #         print(f"✅ Import 실행: {file_path}")
    #         cmds.file(file_path, open=True, force=True, type=file_type, ignoreVersion=True, options="v=0;")


        # 테이블위젯 좌표값
        # item = self.table_mgr.tableWidget.itemAt(position)
        # self.selected_item = item.text()
        
        # menu = QMenu()

        # open_action = menu.addAction("Open")
        # import_action = menu.addAction("Import")
        # reference_action = menu.addAction("Reference")

        # # QAction이 실행되었을 때 실행할 함수 연결
        # open_action.triggered.connect(self.maya_open)
        # import_action.triggered.connect(self.maya_import)
        # reference_action.triggered.connect(self.maya_reference)

        # menu.exec_(self.table_mgr.tableWidget.viewport().mapToGlobal(position))
        
    

    def view_icon(self):
        """아이콘 뷰 활성화"""
        self.ui.listView_button.hide()  # 리스트뷰 숨기기
        self.ui.tableWidget.show()  # 테이블 위젯 표시

    def view_list(self):
        """리스트 뷰 활성화"""
        current_item = self.ui.treeWidget.currentItem()
        task_item = self.ui.treeWidget_task.currentItem()

        if not current_item and not task_item:
            print("폴더가 선택되지 않았음")
            return

        # treeWidget에서 선택된 경우
        if current_item:
            self.current_folder = self.table_mgr.get_full_path(current_item)
        # treeWidget_task에서 선택된 경우
        elif task_item:
            self.current_folder = self.table_mgr.get_task_path(task_item)

        if not os.path.exists(self.current_folder):
            print(f"경로가 존재하지 않음: {self.current_folder}")
            return

        # 리스트뷰 활성화
        self.ui.tableWidget.hide()
        self.ui.listView_button.show()

        # 테이블과 동일한 크기 적용
        self.ui.listView_button.setGeometry(self.ui.tableWidget.geometry())

        # 모델 설정
        model = QStandardItemModel()
        self.ui.listView_button.setModel(model)

        for file in os.listdir(self.current_folder):
            model.appendRow(QStandardItem(file))


        

    def new_combo(self):
        self.ui.treeWidget_task.clear()
        project_name = self.ui.comboBox_task.currentText()

        self.path_manager = sg_api.MyTask(user_id=133, project=project_name)
        folders = self.path_manager.display_folders()
        self.update_task_tree(folders)

    def update_task_tree(self, folders):
        """Task 트리를 새로운 값으로 업데이트"""
        task_data = self.tree_mgr.get_task(folders)  # 기존 TreeMgr 활용
        self.tree_mgr.populate_tree(task_data, self.ui.treeWidget_task) 


    def click_history(self, item):
        """트리에서 선택한 항목 기록"""
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]  # 앞으로 가기 기록 삭제

        self.history.append(item)  # 새 아이템 저장
        self.current_index += 1  # 현재 인덱스 업데이트

        # label_path
        full_path = self.table_mgr.get_full_path(item)
        self.ui.label_path.setText(full_path)

    def go_back(self):
        """뒤로 가기 버튼 동작 - 이전 트리 항목 선택"""
        if self.current_index > 0:
            self.current_index -= 1
            item = self.history[self.current_index]  # 이전 항목 가져오기

            # tableWidget 먼저 초기화
            self.ui.tableWidget.clearContents()
            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.setColumnCount(0)

            self.ui.treeWidget.setCurrentItem(item)  # 이전 항목 선택
            self.ui.treeWidget.scrollToItem(item)  # 스크롤 이동
            print(f" 뒤로 가기: {item.text(0)}")

            folder_path = self.table_mgr.get_full_path(item)

            if os.path.isdir(folder_path):  # 폴더인지 확인
                print(f"테이블 업데이트: {folder_path}")
                self.table_mgr.display_files(os.listdir(folder_path), folder_path)  # 테이블 갱신
            else:
                print(f"폴더가 존재하지 않습니다: {folder_path}")

    def go_front(self):
        """앞으로 가기 버튼 동작"""
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            item = self.history[self.current_index]  # 다음 항목 가져오기

            # tableWidget 먼저 초기화
            self.ui.tableWidget.clearContents()
            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.setColumnCount(0)

            self.ui.treeWidget.setCurrentItem(item)  # 다시 선택
            self.ui.treeWidget.scrollToItem(item)  # 스크롤 이동

            folder_path = self.table_mgr.get_full_path(item) 

            if os.path.isdir(folder_path):  # 폴더인지 확인
                print(f"테이블 업데이트: {folder_path}")
                self.table_mgr.display_files(os.listdir(folder_path), folder_path)  # 테이블 갱신
            else:
                print(f"폴더가 존재하지 않습니다: {folder_path}")


    def go_home(self):
        """홈 버튼 클릭 시 초기화"""
        self.history = []  # 히스토리 리셋
        self.current_index = -1
        
        self.ui.treeWidget.clearSelection()  # 트리 선택 해제
        self.ui.treeWidget_task.clearSelection()
        self.ui.tableWidget.clear()
        self.tree_mgr.show_file(self.root_path) 
        
        folder_path = self.root_path 
        # 추가: tableWidget 초기화
        if os.path.isdir(folder_path):
            self.ui.tableWidget.clearContents()
            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.setColumnCount(0)
            self.table_mgr.display_files(os.listdir(folder_path), folder_path)
        
        self.ui.treeWidget.itemClicked.connect(self.click_history)

        print(" 홈으로 이동")
        
class UtilityMgr:
    """트리 위젯 버튼 구현 클래스"""
    def __init__(self,  ui, tree_widget):
        self.ui = ui
        self.tree_widget = tree_widget
        self.root_path = "/nas/Batz_Maru"

        # ComboBox_task_pro
        self.ui.comboBox_task.addItems(self.get_projects())
        self.ui.comboBox_task.currentIndexChanged.connect(self.print_selected_project) 

        # Enter 키 입력시 실행
        self.ui.lineEdit.returnPressed.connect(self.run_search)

        # tableWidget/슬라이더 - 스타일 및 기능 추가
        
        self.ui.horizontalSlider.valueChanged.connect(self.update_asset_icons)

        # tableWidget/슬라이더 - 기본값 설정
        self.ui.horizontalSlider.setValue(50)
        
    def print_selected_project(self):
        selected_project = self.ui.comboBox_task.currentText()
        print(f"선택된 프로젝트: {selected_project}")


    def get_projects(self):
        project = []
        for name in os.listdir(self.root_path):
            project_path = f"{self.root_path}/{name}" # 경로 만들기
            if not os.path.isdir(project_path): # 디렉토리가 아니면 패스
                continue
            project.append(name)
        return project

        

    # 검색 실행 함수
    def run_search(self): 
        """ 검색 실행 함수 - 트리 위젯에서 검색 """
        keyword = self.ui.lineEdit.text().strip() 

        if not keyword:  
            print("검색어를 입력하세요.")
            return

        found = self.find_and_select_in_tree(keyword)
        
        if not found:
            print(f"'{keyword}'에 해당하는 폴더 또는 파일을 찾을 수 없습니다.")
        else:
            print(f"'{keyword}' 검색 결과를 강조 표시합니다.")

    def find_and_select_in_tree(self, keyword):
        """ 트리에서 키워드와 일치하는 항목을 찾아 선택 """

        def search_items(item):
            """ 재귀적으로 트리를 탐색하면서 키워드 검색 """
            for i in range(item.childCount()):
                child = item.child(i) 
                
                if keyword.lower() in child.text(0).lower():  
                    self.tree_widget.setCurrentItem(child)  
                    self.tree_widget.scrollToItem(child)  
                    return True  # 검색 성공
                
                # 자식 항목이 있는 경우 하위 폴더도 검색
                if search_items(child):
                    item.setExpanded(True) # 부모 폴더를 자동으로 펼쳐서 보이게 함
                    return True  # 검색 성공
        
            return False  # 검색어가 포함된 항목을 찾지 못한 경우
        
        # 최상위 폴더(Batz_Maru)부터 검색 시작
        for i in range(self.tree_widget.topLevelItemCount()):
            top_item = self.tree_widget.topLevelItem(i)  # 최상위 폴더 가져오기
            if search_items(top_item):
                return True  # 검색 성공
        
        return False  # 검색 실패

    # 슬라이더 값 변경 시 아이콘과 테이블 셀 크기를 업데이트
    def update_asset_icons(self):
        zoom_value = self.ui.horizontalSlider.value()
        icon_size = 50 + (zoom_value / 100) * 50  # 기본 50px ~ 최대 100px 크기 조절

        row_count = self.ui.tableWidget.rowCount()
        col_count = self.ui.tableWidget.columnCount()

        for row in range(row_count):
            for col in range(col_count):
                widget = self.ui.tableWidget.cellWidget(row, col)
                if widget:
                    layout = widget.layout()
                    if layout and layout.count() > 1:
                        image_label = layout.itemAt(0).widget()
                        if isinstance(image_label, QLabel):
                            thumb_path = "/nas/Batz_Maru/pingu/imim/batzz_1.png"
                            pixmap = QPixmap(thumb_path).scaled(
                                int(icon_size), int(icon_size),
                                Qt.KeepAspectRatio, Qt.SmoothTransformation
                            )
                            image_label.setPixmap(pixmap)
                            image_label.setScaledContents(True)
                            image_label.setFixedSize(int(icon_size), int(icon_size))

        # 테이블 셀 크기 업데이트 (아이콘이 잘리지 않도록 조정)
        self.ui.tableWidget.verticalHeader().setDefaultSectionSize(int(icon_size) + 30)  
        self.ui.tableWidget.horizontalHeader().setDefaultSectionSize(int(icon_size) + 30)

        # 테이블 UI 업데이트 적용
        self.ui.tableWidget.update()
        self.ui.tableWidget.viewport().update()
        # 현재 선택한 폴더의 파일 목록을 다시 표시하고 아이콘 크기 반영
        
    def refresh_table(self):
        current_item = self.ui.treeWidget.currentItem()
        if current_item:
            folder_path = self.asset_manager.get_full_path(current_item)
            if os.path.isdir(folder_path):
                self.asset_manager.display_files(os.listdir(folder_path))
                self.update_asset_icons()  # 아이콘 크기 즉시 업데이트

class TableMgr:
    def __init__(self, ui, tree_widget, treeWidget_task, table_widget, label_path, folders, root_path):
        self.ui = ui
        self.treeWidget = tree_widget
        self.treeWidget_task = treeWidget_task
        self.tableWidget = table_widget
        self.root_path = root_path
        self.label_path = label_path
        self.folders = folders
        
        self.treeWidget.itemClicked.connect(self.get_asset)
        self.treeWidget_task.itemClicked.connect(self.get_task_assets)
        self.tableWidget.cellDoubleClicked.connect(self.open_item)

        

    def get_asset(self, item):
        """선택한 폴더의 파일 목록을 테이블에 표시"""
        folder_path = self.get_full_path(item)  # 전체 경로 가져오기
        self.display_files(os.listdir(folder_path), folder_path)
        
        # 분리 예정
        self.label_path.setText(folder_path)

    def get_task_assets(self, item):
        task_path = self.get_task_path(item)
        self.display_files(os.listdir(task_path), task_path)
        
        # 분리 예정
        self.label_path.setText(task_path)

    def get_full_path(self, item):
        """ full 트리에서 경로 추출"""

        path_list = []

        while item:
            path_list.insert(0, item.text(0))  # 부모 경로부터 추가
            item = item.parent()

        full_path = os.path.join(self.root_path, *path_list)
        
        return full_path

    def get_task_path(self, task_item):
        """ task 트리에서 경로 추출 """
        
        # task 트리 선택 항목 경로화 예) "Ep1_0010_Layout/sourceimages"
        task_list = []

        while task_item:
            if isinstance(task_item, QTreeWidgetItem):
                task_list.insert(0, task_item.text(0))  # ✅ QTreeWidgetItem은 text(0) 사용
                task_item = task_item.parent()
            
            elif isinstance(task_item, QTableWidgetItem):
                task_list.insert(0, task_item.text())  # ✅ QTableWidgetItem은 text() 사용
                break  # ✅ QTableWidgetItem은 부모가 없으므로 루프 종료
            
            else:
                print(f"⚠️ 알 수 없는 아이템 타입: {type(task_item)}")  # 디버깅용
                break

        # while task_item:
        #     task_list.insert(0, task_item.text(0))  # 부모 → 자식 순서로 리스트에 저장
        #     task_item = task_item.parent()
        
        relative_path = os.path.join(*task_list)
        print(f"클릭 경로: {relative_path}")

        # self.folders에서 최상위 경로 찾기
        base_path = None
        for folder in self.folders:
            if relative_path.startswith(os.path.basename(folder)):  # 폴더명이 포함된 최상위 경로 찾기
                base_path = folder
                break
        if base_path is None:
            print(f"❌ 오류: '{relative_path}'의 최상위 경로를 찾을 수 없음!")
            return relative_path  # 최악의 경우 상대 경로라도 반환
        
        # 최종 경로 생성 예) /nas/Batz_Maru/Jupiter/work/Ep1_0010_Layout/
        full_path = os.path.join(base_path, relative_path.replace(os.path.basename(base_path), "").lstrip("/"))
        return full_path
    #
    #
    #

    def resize_window(self):
        new_width = self.ui.width()
        new_height = self.ui.height()

        self.ui.tableWidget.setGeometry(280, 110, new_width - 300, new_height - 200)
        
        self.ui.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # ✅ 세로 스크롤 항상 표시

        # 🔥 현재 폴더 유지하면서 파일 재배치
        if hasattr(self, "current_folder") and self.current_folder:
            self.display_files(os.listdir(self.current_folder), self.current_folder)

    #
    #
    #


    def display_files(self, file_list, folder_path):
        """테이블 위젯에 파일 목록을 표시"""
        self.tableWidget.clearContents()  # 기존 파일 목록 초기화
        self.current_folder = folder_path

        column_width = 100  # 한 개 아이템(셀)의 너비
        table_width = self.tableWidget.width() # 테이블 위젯 전체 너비를 가져옴
        
        column_count = max(0, table_width // column_width)  # 최소 1개의 컬럼 유지 + 열이 나온다
        row_count = (len(file_list) + column_count - 1) // column_count  # 행 개수 자동 계산

        print(f"테이블 업데이트: {table_width}px → {column_count}열, {row_count}행")

        self.tableWidget.setColumnCount(column_count)
        self.tableWidget.setRowCount(row_count)

         # 가로 스크롤 제거
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 가로 스크롤 없앰
        
 

        for index, file in enumerate(file_list):
            row = index // column_count  # 행 계산
            col = index % column_count   # 열 계산
            self.make_asset_table(row, col, file, folder_path)  # 행과 열을 정확히 배치

    def make_asset_table(self, row, col, file, folder_path):
        """테이블에 개별 애셋(파일)을 추가"""
        widget = QWidget()
        layout = QVBoxLayout()

        image_label = QLabel() # 이미지 라벨
        text_label = QLabel()  # 텍스트 라벨 (파일 이름 표시)

        # 폴더 또는 파일인지 확인하여 thumb_path 결정
        full_path = os.path.join(folder_path, file)  # 파일의 전체 경로 생성
        if os.path.isdir(full_path):
            thumb_path = "/nas/Batz_Maru/pingu/imim/batzz.png"
        else:
            thumb_path = "/nas/Batz_Maru/pingu/imim/batzz_mamb.png"

        pixmap = QPixmap(thumb_path).scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)

        # # 이름 넘길시 ...
        fm = QFontMetrics(text_label.font())
        max_width = 90 # 최대가로 실어
        max_lines = 2 # 최대 2줄
        elided_text = fm.elidedText(file, Qt.ElideRight, max_width)  # 길면 "..." 처리
        text_label.setText(elided_text)  # 줄인 텍스트 적용

        layout.addWidget(image_label)
        layout.addWidget(text_label)
        widget.setLayout(layout)

        file_item = QTableWidgetItem(file)
        file_item.setForeground(QColor(255, 255, 255, 0))  # A(알파) 값 0 → 완전 투명
        self.tableWidget.setItem(row, col, file_item)

        self.tableWidget.setCellWidget(row, col, widget)  # 테이블에 추가

        # 테이블 스타일 설정 
        self.tableWidget.setShowGrid(False) # 표 선 숨기기
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100) # 세로 간격
        self.tableWidget.verticalHeader().setDefaultSectionSize(120) # 가로 간격
        self.tableWidget.verticalHeader().setMinimumSectionSize(30)

    def open_item(self, row, column):
        """더블 클릭 시 폴더 내부로 이동 또는 파일 실행"""
        item = self.tableWidget.item(row, column)
        if item is None:
            print("⚠ 오류: 선택한 셀이 비어 있음!")
            return

        file_name = item.text().strip()
        full_path = os.path.join(self.current_folder, file_name)  # ✅ 현재 폴더 기준으로 경로 생성

        print(f" 현재 폴더: {self.current_folder}")
        print(f" 선택한 파일/폴더: '{file_name}'")
        print(f" 최종 경로: {full_path}")

        if os.path.isdir(full_path):
            # print(f"폴더 안으로 이동: {full_path}")
            self.current_folder = full_path  # 현재 폴더 업데이트
            self.display_files(os.listdir(full_path), full_path)  # ✅ 내부 폴더 파일 목록 표시

            # label_path
            self.sync_tree_with_table(full_path)  # 트리 위치 동기화 추가
            # self.label_path.setText(full_path)
        

        else:
            print(f"파일 실행: {full_path}")
            self.open_maya_file(row, column)

    def sync_tree_with_table(self, folder_path):
        """테이블에서 폴더를 열면 트리도 해당 위치로 이동"""
        def find_item_by_path(item, target_path):
            """트리에서 특정 경로를 가진 아이템을 찾는 재귀 함수"""
            if self.get_full_path(item) == target_path:
                return item
            
            for i in range(item.childCount()):
                found_item = find_item_by_path(item.child(i), target_path)
                if found_item:
                    return found_item
            return None

        # 트리의 최상위부터 탐색
        for i in range(self.treeWidget.topLevelItemCount()):
            root_item = self.treeWidget.topLevelItem(i)
            target_item = find_item_by_path(root_item, folder_path)
            if target_item:
                self.treeWidget.setCurrentItem(target_item)  # 트리 위치 이동
                target_item.setExpanded(True)  # 폴더 자동 확장
                break

    def open_maya_file(self, row, column):
        """더블 클릭한 테이블의 파일을 Maya에서 실행"""
        print("더블 클릭 감지됨!")

        item = self.tableWidget.item(row, column)  # QTableWidgetItem을 가져옴
        if item is None:
            print("선택한 셀이 비어 있음! 파일이 존재하지 않음.")
            print(f"현재 테이블 행 수: {self.tableWidget.rowCount()}")
            print(f"현재 테이블 열 수: {self.tableWidget.columnCount()}")
            return

        file_name = item.text()  # 파일명을 가져옴
        folder_item = self.find_file_path_in_tree(file_name)  # 트리에서 해당 파일이 포함된 폴더 찾기

        if folder_item is None:
            print(f"트리에서 파일 {file_name} 이(가) 포함된 폴더를 찾을 수 없음.")
            return

        file_folder = self.get_full_path(folder_item)  # 해당 파일의 폴더 경로 가져오기
        file_path = os.path.join(file_folder, file_name)

        print(f"최종 파일 경로: {file_path}")

        if os.path.exists(file_path):  # 파일이 실제 존재하는지 확인
            if file_name.endswith((".ma", ".mb", ".fbx", ".obj")):  # 추가 확장자 지원
                print(f"Maya 파일 실행: {file_path}")

                if cmds.file(file_path, q=True, exists=True):
                    cmds.file(new=True, force=True)  # 새로운 씬 열기
                    cmds.file(file_path, open=True, force=True)  # 마야 파일 실행
                    print(f"{file_path} 실행 완료!")
                else:
                    print(f" 파일을 찾을 수 없습니다: {file_path}")
            else:
                print(f" 이 파일은 마야 파일이 아닙니다: {file_name}")
        else:
            print(f" 실제 파일이 존재하지 않음: {file_path}")

    def find_file_path_in_tree(self, file_name):
        """트리에서 해당 파일이 포함된 폴더를 찾아 반환"""
        def search_tree(item):
            for i in range(item.childCount()):
                child = item.child(i)
                folder_path = self.get_full_path(child)

                # 해당 폴더에 파일이 있는지 검사
                if os.path.exists(os.path.join(folder_path, file_name)):
                    return child

                # 재귀적으로 하위 폴더 탐색
                found_item = search_tree(child)
                if found_item:
                    return found_item

            return None

        # 최상위 폴더부터 탐색 시작
        for i in range(self.treeWidget.topLevelItemCount()):
            top_item = self.treeWidget.topLevelItem(i)
            found_item = search_tree(top_item)
            if found_item:
                return found_item

        return None  # 해당 파일이 포함된 폴더를 찾을 수 없음

class UISetup(QObject):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.button_images = self.get_button_images()
        self.button_mapping = self.get_button_mapping()
        self.setup_button_styles()
        self.resize_window()
        self.set_background()
        self.apply_styles()
        self.image_path()

        self.ui.installEventFilter(self)

    def image_path(self):
        task_image = "/nas/Batz_Maru/pingu/imim/batzz_open.png"
        pixmap = QPixmap(task_image).scaled(200, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ui.pushButton_luck.setIcon(QIcon(pixmap))
        self.ui.pushButton_luck.setIconSize(QSize(200, 180))
        self.ui.pushButton_luck.setFixedSize(200, 180)


    def eventFilter(self, obj, event):
        """창 크기 변경 감지"""
        if obj == self.ui and event.type() == event.Resize:         
            self.resize_window()
        return super().eventFilter(obj, event)

    def resize_window(self):
        """창 크기에 맞춰 tableWidget 크기 조정"""
        margin = 20  # 여백 설정
        window_width = self.ui.width()
        window_height = self.ui.height()
        tab_width = self.ui.tabWidget.width() + 10
        new_width = self.ui.width()
        new_height = self.ui.height() # 상단 UI를 고려하여 조정

        self.ui.pushButton_icon_menu.setGeometry(new_width - 310, 60, 40, 40)
        self.ui.pushButton_list_menu.setGeometry(new_width - 260, 60, 40, 40)
        self.ui.tableWidget.setGeometry(280, 110, new_width - 500, new_height - 200)
        self.ui.lineEdit.setGeometry(10, new_height - 115, 261, 28)
        self.ui.tabWidget.setGeometry(10, 110, 261, new_height - 230)
        self.ui.treeWidget.setGeometry(0, 0, 257, new_height - 267)
        self.ui.treeWidget_task.setGeometry(0, 0, 261, new_height - 230)
        self.ui.horizontalSlider.setGeometry(new_width -465, new_height - 72 , 240, 16)
        self.ui.pushButton_luck.setGeometry(new_width - 210, 10, 200, 180)
        self.ui.listWidget_sub.setGeometry(new_width - 210, 200, 200, new_height - 290)
  
    def set_background(self):
        """전체 UI의 배경을 설정"""
        self.ui.setStyleSheet("QMainWindow { background-color: black; }")

    # 버튼 스타일 적용 함수
    def setup_button_styles(self):
        """버튼 스타일 설정"""
        for button, key in self.button_mapping.items():
            normal_img, clicked_img = self.button_images[key]
            button.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background: transparent;
                    background-image: url({normal_img});
                    background-repeat: no-repeat;
                    background-position: center;
                    transition: filter 0.2s ease-in-out;
                }}
                QPushButton:hover {{
                    filter: brightness(80%);
                }}
                QPushButton:pressed {{
                    background-image: url({clicked_img});
                }}
            """)

    def get_button_images(self):
        """버튼에 사용될 이미지 경로 반환"""
        base_path = "/nas/Batz_Maru/pingu/imim"
        return {
            "home": (f"{base_path}/white/home.png", f"{base_path}/yellow/home_1.png"),
            "back": (f"{base_path}/white/ctrlz.png", f"{base_path}/yellow/ctrlz_1.png"),
            "front": (f"{base_path}/white/ctrlshiftz.png", f"{base_path}/yellow/ctrlshiftz_1.png"),
            "list_menu": (f"{base_path}/white/menu.png", f"{base_path}/yellow/menu_1.png"),
            "icon_menu": (f"{base_path}/white/icon_menu.png", f"{base_path}/yellow/icon_menu_1.png"),
            }

    def get_button_mapping(self):
        """버튼과 이미지 키 매핑"""
        return {
            self.ui.pushButton_home: "home",
            self.ui.pushButton_back: "back",
            self.ui.pushButton_front: "front",
            self.ui.pushButton_list_menu: "list_menu",
            self.ui.pushButton_icon_menu: "icon_menu",
        }

    def apply_styles(self):
        """UI 스타일을 설정하는 함수"""

        self.ui.listView_button.setStyleSheet("""
            QListView {
                background-color: #FFF8DC; /* 크림색 배경 */
                border: 2px solid #fdcb01; /* 배츠마루 테마 노랑 테두리 */
                color: #555555;
                font: 14px "Comic Sans MS";
                selection-background-color: #faefc1; /* 선택된 항목 배경 */
                padding: 5px;
            }
            QListView::item {
                padding: 5px;
            }
            QListView::item:selected {
                background-color: #faefc1;
                color: #000000;
                font-weight: bold;
            }
        """)

        self.ui.lineEdit.setStyleSheet("""
            QLineEdit {
                border: 0px solid #FFF8DC;
                border-radius: 10px;
                padding: 5px;
                font-size: 16px;
                background-color: #feeca4;
                color: #333333;
            }
            QLineEdit:focus {
                border: 2px solid #fdcb01;
                background-color: #FFF8DC;
            }
        """)

        self.ui.pushButton_luck.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)

        self.ui.treeWidget.setStyleSheet("""
        QTreeWidget {
            background-color: #FFF8DC; /* 크림색 배경 */
            border: 2px solid #fdcb01; /* 배츠마루 느낌의 노랑 테두리 */
            border-radius: 0px;
            color: #555555;
            font: 14px "Comic Sans MS"; /* 귀여운 느낌의 폰트 */
        }

        /* 헤더 스타일 */
        QHeaderView::section {
            background-color: #feeca4; /* 배츠마루 테마 연한 노랑 */
            color: #222222;
            font: bold 16px "Comic Sans MS"; /* 심플한 귀여운 느낌 */
            padding: 8px;
            border-radius: 8px;
            text-align: center;
        }

        /* 트리 아이템 스타일 */
        QTreeWidget::item {
            height: 32px;
            padding: 6px;
            border-radius: 2px;
        }

        QTreeWidget::item:selected {
            background-color: #faefc1; /* 부드러운 연노랑 */
            color: #222222;
        }

        QTreeWidget::item:hover {
            background-color: #faefc1;
        }

        /* 세련된 스크롤바 스타일 */
        QScrollBar:vertical, QScrollBar:horizontal {
            border: none;
            background: transparent;
            width: 5px;
            height: 5px;
        }

        QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
            background: #fdcb01; /* 부드러운 노랑 */
            border-radius: 5px;
            min-height: 20px;
            min-width: 20px;
        }

        QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
            background: #fea500; /* 마우스 올리면 살짝 더 진한 노랑 */
        }

        QScrollBar::handle:vertical:pressed, QScrollBar::handle:horizontal:pressed {
            background: #ff9800; /* 클릭하면 더 오렌지빛 */
        }

        QScrollBar::add-line, QScrollBar::sub-line {
            background: none;
            border: none;
        }
        """)

        self.ui.tableWidget.setStyleSheet("""
            QTableWidget {
                background-color: #FFF8DC; /* 크림색 배경 */
                border: 2px solid #fdcb01; /* 배츠마루 테마 노랑 테두리 */
                border-radius: 0px;
                
                font: 17px "Comic Sans MS"; /* 귀여운 느낌의 폰트 */
              
      
                font: 10px "Comic Sans MS";
            }
            QHeaderView::section {
                background-color: #feeca4;
                font: bold 16px "Comic Sans MS";
            }
            QTableWidget::item:selected {
                background-color: #faefc1;
                color: rgba(0, 0, 0, 0);  /* 의문의 글자 색: 투명 */
                font-weight: bold;  /* 글자를 굵게 */
            }
            QHeaderView::section {
                background-color: #feeca4; /* 연한 노랑 */
                color: #555555;
                font: bold 16px "Comic Sans MS"; /* 심플한 귀여운 폰트 */
                padding: 8px;
                border-radius: 8px;
                text-align: center;
            
            }
        """)

        self.ui.treeWidget_task.setStyleSheet("""
               /* 전체 배경 및 기본 폰트 설정 */
        QTreeWidget {
            background-color: #FFF8DC; /* 크림색 배경 */
            border: 2px solid #fdcb01; /* 배츠마루 느낌의 노랑 테두리 */
            border-radius: 0px;
            color: #555555;
            font: 14px "Comic Sans MS"; /* 귀여운 느낌의 폰트 */
        }

        /* 헤더 스타일 */
        QHeaderView::section {
            background-color: #feeca4; /* 배츠마루 테마 연한 노랑 */
            color: #222222;
            font: bold 16px "Comic Sans MS"; /* 심플한 귀여운 느낌 */
            padding: 8px;
            border-radius: 8px;
            text-align: center;
        }

        /* 트리 아이템 스타일 */
        QTreeWidget::item {
            height: 32px;
            padding: 6px;
            border-radius: 6px;
        }

        QTreeWidget::item:selected {
            background-color: #faefc1; /* 부드러운 연노랑 */
            color: #222222;
        }

        QTreeWidget::item:hover {
            background-color: #faefc1;
        }

        /* 세련된 스크롤바 스타일 */
        QScrollBar:vertical, QScrollBar:horizontal {
            border: none;
            background: transparent;
            width: 5px;
            height: 5px;
        }

        QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
            background: #fdcb01; /* 부드러운 노랑 */
            border-radius: 5px;
            min-height: 20px;
            min-width: 20px;
        }

        QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
            background: #fea500; /* 마우스 올리면 살짝 더 진한 노랑 */
        }

        QScrollBar::handle:vertical:pressed, QScrollBar::handle:horizontal:pressed {
            background: #ff9800; /* 클릭하면 더 오렌지빛 */
        }

        QScrollBar::add-line, QScrollBar::sub-line {
            background: none;
            border: none;
        }
        """)
        self.ui.comboBox_task.setStyleSheet("""
        QComboBox {
            background-color: #FFF8DC; /* 크림색 배경 */
            border: 2px solid #fdcb01; /* 노란 테두리 */
            border-radius: 5px;
            padding: 5px;
            color: #111111;
            font: 14px "Comic Sans MS";
        }
        QComboBox:hover {
            background-color: #faefc1; /* 호버 시 밝은 노랑 */
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox QAbstractItemView {
            background-color: #feeca4; /* 드롭다운 배경 */
            selection-background-color: #faefc1; /* 선택된 항목 배경 */
            border: 1px solid #fdcb01;
        }
    """)

        self.ui.tabWidget.setStyleSheet("""
        QTabWidget::pane {
            border: 2px solid #fdcb01; /* 노란색 테두리 */
            background-color: #FFF8DC; /* 크림색 배경 */
            border-radius: 3px;
        }
        QTabBar::tab {
            background: #feeca4; /* 연한 노랑 */
            border: 1px solid #fdcb01;
            border-top-left-radius: 13px;
            border-top-right-radius: 5px;
            padding: 10px;
            color: #555555;
            font: bold 11px "Comic Sans MS";
        }
        QTabBar::tab:selected {
            background: #faefc1; /* 선택된 탭 강조 */
            color: #222222;
            font-weight: bold;
        }
        QTabBar::tab:hover {
            background: #fce6a4; /* 호버 효과 */
        }
    """)
        self.ui.listWidget_sub.setStyleSheet("""
            QListWidget {
                background-color: #FFF8DC; /* 크림색 배경 */
                border: 2px solid #fdcb01; /* 배츠마루 테마 노랑 테두리 */
                border-radius: 0px;
                color: #555555;
                font: 14px "Comic Sans MS"; /* 귀여운 느낌의 폰트 */
                gridline-color: #fdcb01; /* 테이블 그리드라인 색상 */
      
                font: 14px "Comic Sans MS";
            }
            QHeaderView::section {
                background-color: #feeca4;
                font: bold 16px "Comic Sans MS";
            }
            QTableWidget::item:selected {
                background-color: #faefc1;
                color: rgba(0, 0, 0, 0);  /* 의문의 글자 색: 투명 */
                font-weight: bold;  /* 글자를 굵게 */
            }
            QHeaderView::section {
                background-color: #feeca4; /* 연한 노랑 */
                color: #222222;
                font: bold 16px "Comic Sans MS"; /* 심플한 귀여운 폰트 */
                padding: 8px;
                border-radius: 8px;
                text-align: center;
            
            }
            /* 개별 아이템 스타일 */
            QListWidget::item {
                color: #333333; /* 기본 아이템 글자색 */
                font: 14px "Comic Sans MS";
                padding: 6px;
            }

            QListWidget::item:selected {
                background-color: #faefc1; /* 부드러운 연노랑 */
                color: #000000; /* 선택된 아이템 글자색 */
                font-weight: bold;
            }

            QListWidget::item:hover {
                background-color: #faefc1;
                color: #222222; /* 마우스 오버 시 글자색 */
            }
        """)
        self.ui.horizontalSlider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                border: 2px solid white; /* 하양 테두리 */
                background: white; /* 하양 배경 */
                height: 2px; /* 트랙 높이 조정 */
                border-radius: 1px;
                padding: 0px; /* 여백 제거 */
            }}
            QSlider::handle:horizontal {{
                background: url(/nas/Batz_Maru/pingu/imim/slider_1.png); /* 핸들 이미지 적용 */
                background-repeat: no-repeat;
                background-position: center;
                width: 30px;  /* 핸들 크기 조정 */
                height: 30px;
                margin: -14px 0; /* 트랙 중앙에 정렬 */
                border: 2px solid transparent; /* 테두리를 투명하게 설정 */
                background-color: transparent; /* 배경색 투명 */
            }}
            QSlider::handle:horizontal:hover {{
                background: url(/nas/Batz_Maru/pingu/imim/slider_1.png); /* 동일한 이미지 유지 */
                background-repeat: no-repeat;
                background-position: center;
                width: 30px;
                height: 30px;
                margin: -14px 0;
                border: 2px solid transparent;
                background-color: transparent;
            }}
            QSlider::sub-page:horizontal {{
                background: yellow; /* 진행된 부분(노랑색) */
                border-radius: 1px;
                padding: 0px; /* 진행된 부분의 여백 제거 */
            }}
        """)

if __name__=="__main__":
    app = QApplication()  
    w = MainCtrl()
    app.exec() 