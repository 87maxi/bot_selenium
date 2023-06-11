
from InquirerPy import inquirer
from pprint import pprint
import os
import yaml



class Loader(yaml.SafeLoader):

    def __init__(self, stream):

        self._root = os.path.split(stream.name)[0]

        super(Loader, self).__init__(stream)

    def include(self, node):

        filename = os.path.join(self._root, self.construct_scalar(node))

        with open(filename, 'r',encoding="utf-8") as f:
            return yaml.load(f, Loader)

Loader.add_constructor('!include', Loader.include)



class Cmd2:
    
    load_app = None
    base_dir = os.getcwd()+os.sep+"configs"

    def __init__(self):
        self.load_app = self.list_app()
        files_list=  self.__load_project(self.load_app)

        files_list_path =[ os.path.join(self.base_dir, a+'.yml')  for a in files_list]

        self.result=  self.__read_configs_files(files_list_path)


    
    def __load_dir(self):
        for r, d, f in os.walk(self.base_dir):
            if d:
                return d
    
    
    def list_app(self):
        lp= inquirer.select(message="Select:", choices=self.__load_dir()).execute()
        return lp

    
    def __load_project(self,project):
            
        self.base_dir = self.base_dir+os.sep+project

        direc =[]
        
        # load files configs
        for r, d, f in os.walk(self.base_dir):
            if d:
                direc.append(d)

        direc[0].remove('include')
        
        res = inquirer.select(message="Select:", choices=direc[0]).execute()
        
        # load file configs

        self.base_dir= self.base_dir+os.sep+res

        files=None
        
        for r,d,f in os.walk(self.base_dir):

            files = [ i.replace(".yml", "") for i in f ]   
            
        
        list_configs_files= inquirer.checkbox(message="Select:", choices=files).execute()

        return list_configs_files

    
    def __read_configs_files(self, file_list ):

        def read_file_generator(files):

            with  open(files, 'r',encoding="utf-8") as  stream:
                stream= yaml.load(stream, Loader)
                yield stream
        
        def load_stream(stream):
            def base_test(i):
                for k,v in i.items():
                    if "loader" not in k:
                        if k =="test":
                            yield v
            di ={}
            di["test"]=[]
            
            if "loader" in stream:

                for i in stream["loader"]:
                    if "test" in i:
                          di["test"] += [ a for a in  base_test(i)][0]

                    if "url" in i:
                        di["url"] = i["url"]
                    if "env" in i:
                        di["env"] = i["env"]
                    
                    if "implicitly_wait" in i:
                        di["implicitly_wait"] = i["implicitly_wait"]

            di["test"] += stream["test"]


            yield di


        return [(file, i)  for file in file_list  for  f in read_file_generator(file) for i in load_stream(f)  ] 