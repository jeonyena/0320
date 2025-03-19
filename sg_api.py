from shotgun_api3 import Shotgun
import re
import file_parsing
import pub
import json
from singleton_sg import Singleton_SG



class MyTask:
      def __init__(self, user_id, project):
            """ShotGrid 태스크 데이터를 로드하고 폴더 경로를 생성하는 클래스"""           

            init_sg = Singleton_SG()
            self.sg = init_sg.sg
            self.user_id = user_id

            self.project_id = self.get_project_id(project)
            self.tasks = self.get_tasks()
            self.entities = self.get_entities(self.tasks)
            self.folders = self.create_folders(self.tasks)
            self.path_list = self.create_paths(project)

            self.task_data = self.pass_data(self.tasks)

            self.display_folders()

      def get_project_id(self, project):
        """ShotGrid에서 프로젝트 ID를 조회하는 함수"""

        filters = [
            ['users', 'is', {'type': "HumanUser", 'id': self.user_id}],
            ['name', 'is', project]
        ]
        project_data = self.sg.find_one("Project", filters, ['id', 'name'])

        if not project_data:
            raise ValueError(f" {project}  없어여")

        return project_data['id']

      def get_tasks(self):
        """유저의 태스크 조회하는 함수"""

        filters = [
            ['task_assignees', 'is', {'type': 'HumanUser', 'id': self.user_id}],
            ['project', 'is', {'type': 'Project', 'id': self.project_id}]
        ]
        fields = ['start_date', 'due_date', 'entity',
                   'content', 'step', 'sg_description', 'duration']

        tasks = self.sg.find("Task", filters, fields)
        print(f"tasks in get tasks : {tasks}")
        
        if not tasks:
            raise ValueError(" 태스크 없어여")
        
        return tasks

      def get_entity_fields(self):
        """엔티티 타입별 필드 매핑하는 함수"""
        
        return {
            'Asset': ['id', 'code', 'sg_asset_type'],
            'Shot': ['id', 'code']
        }

      def get_entities(self,tasks):
        """태스크에서 엔티티 정보 조회하는 함수"""

        entity_types = {task['entity']['type'] for task in tasks}
        entity_fields = self.get_entity_fields()

        entities = {}
        for entity_type in entity_types:
            entity_names = {
                task['entity']['name']
                for task in tasks if task['entity']['type'] == entity_type
            }
            if not entity_names:
                continue

            filters = [
                ['project', 'is', {'type': 'Project', 'id': self.project_id}],
                ['code', 'in', list(entity_names)]
            ]
            entity_list = self.sg.find(entity_type, filters, entity_fields[entity_type])

            for entity in entity_list:
                entities[entity['code']] = entity  

        return entities

      def create_folders(self,tasks):
        """태스크와 엔티티 정보를 조합해 폴더명 생성하는 함수"""

        folders = set()

        for task in tasks:
            entity_name = task['entity']['name']
            step_name = task['step']['name']
            entity_type = task['entity']['type']

            if entity_type == 'Shot':
                folders.add(f"{entity_name}_{step_name}")
            else:
                entity = self.entities.get(entity_name)
                if entity:
                    folders.add(f"{entity_name}_{entity['sg_asset_type']}_{step_name}")

        return list(folders)

      def create_paths(self, project):
        """폴더명들을 기반으로 경로 생성"""
            
        return [f"/nas/Batz_Maru/{project}/work/{folder}" for folder in self.folders]

      def display_folders(self):
            """폴더 리스트를 보내는 함수"""

            print(f"path list: {self.path_list}")
            return self.path_list


      def pass_data(self, task):
            """나에게 할당된 태스크의 정보들을 보여주는 함수"""

            for task_name in self.tasks:
                  if task == task_name:
                        f"task start : {task['start_date']}"
            return
                  # days = int(task['duration'] / 60 / 8)    
                  # for entity in entities:

                  #       pub_data =  {
                  #             'sg': self.sg,
                  #             'user_id': self.user_id,
                  #             'task_data' : {'type': 'Task', 
                  #                         'start_date': task['start_date'], 
                  #                         'due_date' : task['due_date'],
                  #                         'duration' : f"{days} Days",
                  #                         'type' : entity['id']}
                  #                   }

                  # print(f" published data : {pub_data}")
                  # return pub_data

if __name__ == "__main__":
    MyTask(user_id=133, project='Jupiter')




class SG_Publish:
      """받은 경로를 샷그리드에 퍼블리쉬하는 클래스
      로더할 때 가진 데이터 기반으로 진행"""

      def __init__(self, pub_dict):

            init_sg = Singleton_SG()
            self.sg = init_sg.sg
            # import sys
            # sys.path.append("/nas/Batz_Maru/pingu/nana/sh1n/0314")
           
            # self.path = "/nas/Batz_Maru/Jupiter/work/Ep1_0010_Layout/scenes/Ep1_0010_v001.ma"  #마야에서 실행할 땐 주석하세이
            # self.parsed_data = self.parsing_path(self.path)
            # print(f"current path in sg_api : {self.path}")
            
            # self.get_id()

            # self.set_data(self.description)
            # self.pub_to_sg()
            # self.create_version()
            # self.update_version()

      def search_value(self):

            """파일의 길이에 따라서 반복돌게 하기
            딕셔너리 value에 따라서 'copy' / 'path' / version / pub files 바뀌도록 하기"""















      def parsing_path(self,path):
            """경로를 파싱하여 필요한 정보 가져오기"""
            print("def parsing path")

            # parser = 
            parser = file_parsing.FileParser(path)
            self.parsed = parser.data

            self.key = parser.matched_key
            f_project = self.parsed.get('project')
            f_work_dir = self.parsed.get('work_dir')
            f_type_info = []
            f_step = self.parsed.get('step')
            
            if self.key in ['maya_seq', 'seq']: 
                  f_type_info = f"{self.parsed.get('seq_name')}_{self.parsed.get('shot_num')}"
                  self.type = 'seq'

            else:
                  f_type_info = self.parsed.get('asset_name')
                  self.type = 'asset'
            
            print(f"type info : {f_type_info}")

            self.data = {
                  'project' : f_project, 
                  'work_dir' : f_work_dir, 
                  'type_info' : f_type_info, 
                  'step' : f_step,
                  }
            
            print(f"parsed file data : {self.data}")

      def get_id(self):
            """파싱된 정보를 가지고 shotgrid 에서 id를 가져오는 함수"""

            json_file_path = '/nas/Batz_Maru/pingu/nana/yenyaong/user_info.json'
            with open(json_file_path, 'r', encoding='utf-8') as file:
                  user_info = json.load(file)
            self.user_id = user_info.get('id')
            print(f" user id : {self.user_id}")

            self.project = self.sg.find_one("Project" , [['name' , 'is' , self.data['project']]] , ['id'])

            if 'seq_name' in self.parsed:
                  self.type = self.sg.find_one("Shot", 
                        [['project', 'is', {'type': 'Project', 'id': self.project['id']}],  
                        ['code', 'is', self.data['type_info']]],  
                        ['id']
                  )
                  self.entity_type = 'Shot'
            else:
                  self.type = self.sg.find_one("Asset", 
                        [['project', 'is', {'type': 'Project', 'id': self.project['id']}], 
                        ['code', 'is', self.data['type_info']]],  
                        ['id']
                  )
                  self.entity_type = 'Asset'

            self.task = self.sg.find_one("Task",
                                  [['project' , 'is' ,{'type' : 'Project' ,'id' :self.project['id']}],
                                   ['entity', 'is', {'type' : self.entity_type, 'id' : self.type['id']}],
                                   ['content','is', self.data['step']]],
                                    ['id','start_date','due_date','duration'])


            print(f"user_id : {self.user_id} project_id : {self.project['id']} task : {self.task} type : {self.type['id']}  entity : {self.entity_type}")



      def set_data(self,description):
            """샷그리드에 생성하기 전에 데이터를 만드는 작업을 하는 함수"""
            # description = "T^T"
            self.publish_data = {  
                  'project': {'type': 'Project', 'name': self.data['project'], 'id' : self.project['id']},   
                  'code': self.path,
                  'task': {'type': 'Task', 'id': self.task['id']},
                  'entity' : {'type' : self.entity_type, 'name' :self.data['type_info'], 'id' : self.type['id']},
                  'path': {'local_path': self.path},
                  'description' : description        
                  }
            
            print(f"Set data: {self.publish_data}")

      def pub_to_sg(self):
            """샷그리드에 데이터를 만드는 함수"""
            self.result = self.sg.create("PublishedFile", self.publish_data) 
            print(f"Published File Created: {self.result}")
      
      def create_version(self):
            """퍼블리쉬 된 파일을 버전업하는 함수"""

            prj_id = self.project['id']
            print(f" project id : {prj_id}")

            pub_file = self.sg.find("PublishedFile" , 
                                    [['project','is',{'type' :'Project','id' : prj_id}],
                                     ['code','is',self.publish_data['code']]],['id'])

            # ver_count = len(pub_file)

            # if pub_file:
            #       current_ver = ver_count + 1

            version_data = {
                  'project' : self.publish_data['project'],
                  # 'code' : f"{self.path}_v{current_ver :03d}",
                  'code' : f"{self.path}",
                  'entity' : {'type' : self.publish_data['entity']['type'], 'id': self.publish_data['entity']['id']},
                  'published_files' : [{'type' : 'PublishedFile', 'id' : self.result['id']}]
            }
            print(f" version data : {version_data}")
            self.version_up = self.sg.create("Version", version_data) 

      def update_version(self):
            """version create하면서 update 해주는 클래스"""
            version_id = self.version_up['id']
            
            change_workdir = self.path.replace(self.path.split('/')[4],"confirm")
            change_workspace = change_workdir.replace(change_workdir.split('/')[-2],"mov")
            change_ext = change_workspace.replace(change_workspace.split('/')[-1].split('.')[-1],'mov')
            print(f" change ext : {change_ext}")
            # if os.isdir
            update_ver = self.sg.update("Version", version_id, {"sg_uploaded_movie" : change_ext})

            print(f"mov 추가됏서여")
            """/nas/Batz_Maru/Jupiter/confirm/IndoRex_Character_Lookdev/mov/IndoRex_v025.mov"""

      def send_data(self):
            """ ui에 필요한 정보를 넘겨주는 함수"""
            days = int(self.task['duration'] / 60 / 8)
            ui_data = {
            'start_date' : self.task['start_date'],
            'due_date' : self.task['start_date'],
            'duration' : f"{days} Days"
            }

            return ui_data