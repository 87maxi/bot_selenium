from abc import ABC



class MetaData(ABC):

    __metadata= {}        
        
        

    def add_metadata(self, key, value):  
        self.__metadata[key]=value 
    
    
    def get_metadata(self, key):
        
        if not key in self.__metadata:
            return False
        return self.__metadata[key]
    
    def remove(self):
        self.__metadata.clear()
    
    def get_all_metadata(self):
        return self.__metadata