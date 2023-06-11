
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

class Cmd:
    
    load_app = None

    def __init__(self):
        self.load_app = self.list_app()
        
        load_project= self.__list_project(self.load_app)
        select_config, list_configs  = self.__list_configs( self.load_app, load_project)
        self.result= self.select_config(select_config, list_configs)


    def __files_configs (self, lp, lc):

        
        configs = self.__load_config(lp=lp, lc=lc)
        
        for file_name, config in configs:

            file_name= file_name.replace(".yml", "")

            yield file_name, config
    
    
    def list_app(self):
        lp= inquirer.select(message="Select:", choices=self.__load_dir()).execute()
        return lp

    
    def __list_project(self, load_app):
        lc = inquirer.select(message="Select:", choices=self.__load_project(load_app)).execute()
        return lc


    def __list_configs(self,load_project,  load_config):        
        configs = [ {file_name: config }  for file_name, config in  self.__files_configs(load_project, load_config)]
        config = [ list(key.keys())[0] for key in configs]
  
        select_config= inquirer.checkbox(message="Select:", choices=config).execute()         
        return select_config, configs

    def select_config(self,file, list_configs ):
        #TODO refactor 1
        print(file[0])
        result= [ i for i in  list_configs for f  in file if f in i  ]
        # TODO refactor 1
        return result
    
    def __load_config(self, lp=None, lc=None):

        # TODO refactor
        mypath=  os.getcwd()+os.sep+"configs"+os.sep+lp+os.sep+lc
        
        # r=root, d=directories, f = files

        def file_generator():
            
            for r, d, f in os.walk(mypath):
                
                for file in f:

                    if file.endswith(".yml"):
                    #onlyfiles.append( os.path.join(r, file))

                        yield file, os.path.join(r, file)

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

        config_files = [ (file, h )  for file, f in file_generator() for y in read_file_generator(f) for h  in load_stream(y) ]

        # TODO refactor

        return config_files

    def __load_dir(self):
        for r, d, f in os.walk(os.getcwd()+os.sep+"configs"):
            if d:
                return d

    def __load_project(self,project):
        base_dir = os.getcwd()+os.sep+"configs"


        for r, d, f in os.walk(base_dir+os.sep+project):

            if d:
                d.remove("include")
                return d
