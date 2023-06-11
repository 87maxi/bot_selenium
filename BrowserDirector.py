from lib2to3.pytree import type_repr
from time import sleep

from lib.BrowserCore  import BrowserCore
from lib.SEreport import SEreport
from lib.SEdb import SEdb
from selenium.common.exceptions import WebDriverException
import yaml
import os
from pprint import pprint





browser_core=BrowserCore()

se_db = SEdb()
dir_pdf=browser_core.dir_pdf()
fp=browser_core.fingerprint("md5")


params={}
params["kw"] = {}

sp= se_db.get_parameters()        


def automation_init(file_name, config):
    
    
    def reflect(methods, params):
                    
        if "delta" in params:        
            [ reflect(k, v) for d in params["delta"] for k, v in d.items()]
            
        getattr(browser_core,methods )(params)


    
    browser_core.chrome(config.get("url"))
    pdf= SEreport()
    pdf.start_pdf_page()
    
    if config.get("implicitly_wait"):
        browser_core.driver.implicitly_wait(config.get("implicitly_wait"))
    
    env = config.get("env")
    print("#######", env)    
    

    for items in config.get("test"):

        
        params["methods"] = list(items.keys())[0]
        
        params["kw"] = list(items.values())[0]        
        params["kw"]["selenium_parameters"] = sp
        params["kw"]["env"] = env
        
        try:    
            
            reflect(params["methods"], params["kw"])


            
            
        except Exception as e:
            file_name = file_name+"-error"
            break
            
                 
        
        finally:
            try:
        
                
                browser_core.add_metadata( "url", browser_core.driver.current_url)
                browser_core.add_metadata("title", browser_core.driver.title)
                #sr.add_metadata("cookies", browser_core.bp.driver.get_cookies())
                browser_core.add_metadata("img", browser_core.get_screenshot())
                browser_core.add_metadata("fingerprint_db", fp )
                browser_core.add_metadata("parameters", params["kw"])
                
                browser_core.add_metadata("script", file_name)
                browser_core.add_metadata("form_id", browser_core.parse_url(browser_core.driver.current_url))
                browser_core.add_metadata("type", file_name)              

        
                if "flag" in browser_core.validation and "description" in browser_core.validation:
                    browser_core.add_metadata("flag", browser_core.validation["flag"])
                    browser_core.add_metadata("description", browser_core.validation["description"])


                
            except WebDriverException as e:
                pprint(e.msg)
                
                pprint("  NoSuchWindowException::::::: ")
            finally:               
                pdf.add_page()
                
                se_db.load_data()
                
                browser_core.validation.clear()
                
                    #pprint(browser_core.get_all_metadata())       
    pdf.print_pdf(dir_pdf+os.sep+file_name+".pdf")
                

        
    


def creator():   
    
    for file, config in browser_core.result:
        f = file.split(os.sep)[-1].replace('.yml', '')
        automation_init(f, config)
        
    browser_core.driver.close()

            
        
    #browser_core.remove()
    

def editor():

    file, test =  se_db.get_selenium(fp)
    automation_init(file_name=file, config=test)
    browser_core.driver.close()


creator()

se_db.delte_database()

#editor()



