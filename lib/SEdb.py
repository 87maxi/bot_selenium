from pprint import pprint
from .MetaData import MetaData
import sqlite3
import json
import os

class SEdb(MetaData):

    def __init__(self) -> None:
        self.cursor= sqlite3.connect("test.db")
        self.__create()
        self.__load_sql()


    def load_data(self):
        data = {
            "title" : self.get_metadata("title"),
            "url": self.get_metadata("url"),
            "fingerprint_db":self.get_metadata("fingerprint_db"),
            "parameters": json.dumps(self.get_metadata("parameters")),
            "function": self.get_metadata("function"),
            "form_id" : self.get_metadata("form_id"),
            "type": self.get_metadata("type")
        }

        #pprint(data)

        self.cursor.execute("""insert into selenium(title,url,fingerprint_db, parameters, function, form_id, type) values
                            ( :title, :url, :fingerprint_db, :parameters, :function, :form_id , :type )""", data)
        self.cursor.commit()
    
    def get_parameters(self):
        self.cursor.row_factory = sqlite3.Row
        a = self.cursor.execute(""" SELECT * from selenium_parameters""").fetchall()
        
        b = []
        for i in a:
            di = {}
            for a in i.keys():
                di[a] = i[a]
            b.append(di)

        return b
    
    def get_selenium(self, fp ):

        query = """SELECT * from selenium as se
                   INNER JOIN edit_target et ON et.target_type = se.'type' 
                   WHERE se.fingerprint_db  = ?"""
        
        pprint(query)
        pprint(fp)
        selenium =self.cursor.execute(query, (fp,))
         
        rows= selenium.fetchall()

        row_list_parameters ={}
        
        row_list_parameters["test"] =[]



        for row in rows:
            row_parameters = dict(row)
            parameters = json.loads( row_parameters["parameters"])
            row_list_parameters["test"].append(parameters)
            row_list_parameters["url"] = row_parameters["target_edit_url"]

            #pprint(row_list_parameters)


        
        
        return row_parameters["type"], row_list_parameters


    
    def __create(self):
        #self.cursor.execute("""
        #    DROP TABLE IF EXISTS selenium;
        #""")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS selenium (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fingerprint_db TEXT NOT NULL,
            title TEXT,
            function TEXT,
            parameters TEXT,
            url TEXT NOT NULL,
            form_id INTEGER,
            type VARCHAR(30),
            created_at TEXT DEFAULT (datetime('now','localtime')) NOT NULL);
        """)

        self.cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS selenium_IDX ON selenium (id);
            """
        )

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS selenium_parameters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            delta_id VARCHAR(100),
            env  VARCHAR(50),
            form_reference VARCHAR(100),
            type VARCHAR(30),
            style VARCHAR(30),
            created_at TEXT DEFAULT (datetime('now','localtime')) NOT NULL);
        """)

        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS selenium_parameters_IDX ON selenium_parameters (id);
        """)


        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS edit_target (
                target_edit_url TEXT,
                target_type TEXT,
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
                , env VARCHAR(30));
        """)

        self.cursor.execute("""
        CREATE INDEX IF NOT EXISTS edit_target_id_IDX ON edit_target (id);
        """)

    def __load_sql(self):
        base_dir = os.getcwd()+os.sep+"sql"

        def read_file_sql(file):
            f = open(file,'r', encoding='utf-8')
            s = f.read()
            return s

        for r, d, f in os.walk(base_dir):
            for i in f :
                
                self.cursor.executescript(read_file_sql(r+os.sep+i))
    
    def delte_database(self):
        self.cursor.execute("DROP TABLE IF EXISTS selenium_parameters")
        self.cursor.execute("DROP TABLE IF EXISTS selenium")
        pprint("DROP DATABASE SQLITE")


    

