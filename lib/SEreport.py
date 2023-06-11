from fpdf import FPDF
from pprint import pprint 
import os
import json
from fpdf import FPDF

from .MetaData import MetaData


class SEreport(MetaData):

    def __init__(self) -> None:
        self.pdf =FPDF()
    
    def encode(self,v):
        return str(v).encode('latin-1', 'replace').decode('latin-1')

    def start_pdf_page(self):
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=9)        
        self.pdf.ellipse(1, 1,  1, 1)
        
    def set_title(self):
        self.pdf.ln(4)
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(1, 4, txt=" TITLE ->  {} ".format( self.get_metadata("title") ), ln=2)
        self.pdf.ln(2)
        self.pdf.cell (1, 4, txt=" URL ->  {} ".format(self.get_metadata("url")), ln=2)
        self.pdf.ln(4)

    def subtitle(self,text):
        self.pdf.ln(2)
        self.pdf.set_font_size(14)
        self.pdf.set_font(style="BU")
        self.pdf.cell(0, 10, txt=text,  ln=1)
        self.pdf.set_font(style="")
        self.pdf.set_font_size(12)

    def add_page(self):

        if self.get_metadata("title"):
            self.pdf.ln(2)
            self.set_title()
            

        if self.get_metadata("cookies"):
            self.pdf.ln(1)
            self.subtitle("cookies")
            self.pdf.set_font_size(7)
            for cookie in self.get_metadata("cookies"):
                for k,v in cookie.items():
                    self.pdf.multi_cell(w=0, h=3, txt=" {}  : {}".format(k, v), align="L" )
                    self.pdf.ln(1)
                

        
        if self.get_metadata("browser"):
            self.pdf.ln(1)
            self.subtitle("browser")
            self.pdf.set_font_size(9)
            for js in  self.get_metadata("browser"):
                [ self.pdf.multi_cell( w=160, h=5, txt="{} : {} ".format( k,v) )  for k, v in js.items() ]
                self.pdf.ln(1)
                
              
        self.pdf.ln(2)
        #for k,v in  self.get_metadata("action").items():
        #    self.pdf.cell(0, 9, txt="{}:".format(k), ln=0.09)            
        #    [self.pdf.cell(0, 4, txt="{}: {}".format(a,b) , ln=1)  for a,b in v.items()]
            
        

        """
        if "acciones" in a :
            self.subtitle("selenium acciones")
            self.pdf.ln(1)

            for k,v in  a.get("acciones").items():
                self.pdf.set_font_size(9)            
                self.pdf.multi_cell(txt="  {} : {}  \n\r".format(k,self.encode(v)), w=0, h=5 ,align = 'L' )
                self.pdf.ln(1)  
        self.pdf.ln(4)
        
        
       
        d = data['metadata']
   
        if "data" in d :
            self.subtitle("selenium data ")
            self.pdf.ln(1)

            for k,v in  d.get('data').items():
                self.pdf.set_font_size(9)            
                self.pdf.multi_cell(txt="  {} : {}  \n\r".format(k,self.encode(v)), w=0, h=5 ,align = 'L' )
                self.pdf.ln(1)  
            self.pdf.ln(4)
        """
        

        if self.get_metadata("description"):
            self.subtitle("Validación")
            self.pdf.ln(4)

            self.pdf.multi_cell(w=0, h=3, txt=" Descripcion  : {}".format(self.get_metadata("description")), align="L" )
            self.pdf.ln(2)

        if self.get_metadata("flag"):
            self.pdf.ln(4)
            
            self.pdf.ln(4)
            
            for resutl in self.get_metadata("flag"):
                for k,v in resutl.items():
                    self.pdf.ln(1)
                    self.pdf.multi_cell(w=0, h=3, txt=" {}  : {}".format(k, v), align="L" )
                    self.pdf.ln(1)

        if self.get_metadata("fingerprint"):
            self.pdf.multi_cell(w=0, h=3, txt=" {}  : {}".format("fingerprint" , self.get_metadata("fingerprint")), align="L" )




        if self.get_metadata("log"):
            self.subtitle("selenium log")
            self.pdf.ln(1)
            e = self.logs()


            #pprint(e)
            """
            for h in e:
               for i in h:
                       if isinstance(i, dict):
                             for k, v in i.items():
                                pprint(v)
                                #self.pdf.multi_cell(txt="  {} : {}  \n\r".format(k,self.encode(str(v))), w=0, h=5 ,align = 'L' )
            """              
                        
            

            self.pdf.set_font_size(9)            
                
                #self.pdf.multi_cell(txt="  {} : {}  \n\r".format(k,self.encode(v)), w=0, h=5 ,align = 'L' )
            self.pdf.ln(1)  
            self.pdf.ln(4)




        #self.pdf.line(10, 5, 10, 5)


        if self.get_metadata("img"):
            self.pdf.ln(3)
            try:
                self.pdf.image(self.get_metadata("img") , w=150)
                os.remove(self.get_metadata("img"))
            except FileNotFoundError as e:
                print(e.filename)
            self.pdf.ln(3)


        if self.get_metadata("cmd"):
            
            for k, v in self.get_metadata("cmd").items():
                
                if isinstance(v,dict):                
                    for a,b in v.items():
                        self.pdf.ln(3)
                        self.pdf.multi_cell(txt="  {} : {}  \n\r".format(a,self.encode(b)), w=0, h=5 ,align = 'L' )
                        self.pdf.ln(3)
                elif isinstance(v,str):
                    pass
                    #self.pdf.multi_cell(txt="  {} : {}  \n\r".format(k,self.encode(v)), w=0, h=5 ,align = 'L' )
        
        if self.get_metadata("fingerprint"):
            self.pdf.ln(3)
            self.pdf.multi_cell(txt="  fingerprint : {}  \n\r".format(self.encode(self.get_metadata("fingerprint"))), w=0, h=5 ,align = 'L' )
            self.pdf.ln(3)



    def logs(self):
        logs = self.get_metadata("log")
        
        for log in logs:
            for _, k in log.items():
                #pprint(k)
                if  isinstance(k, str):
                    if not "INFO" in k:
                        if "message" in k:
                            return json.loads(k)
       
    

    def print_pdf (self,path):
        
        self.pdf.output(path, "F")