# -*- coding: utf-8 -*-
from ast import walk
from pprint import pprint


from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyautogui
import os
from time import sleep, time
import random
import datetime
from .BrowserParser import BrowserParser
from .Cmd2 import Cmd2
import re
from random import sample





class BrowserCore(BrowserParser, Cmd2):
   
    def __init__(self):
        super().__init__()
        
        self.validation = {}
              

    def ck_editor(self, kw):
        
        self.execute_script()        

        self.check_element(kw)

        self.selector(**kw["selector"])    
        actions = ActionChains(self.driver)
        [actions.move_to_element(element) for element in self.elements]
        actions.perform()
        
        self.action_type(attr="click")
        
        hash =""
        if "fingerprint" in kw:
           hash= self.fingerprint(**kw["fingerprint"])
           self.add_metadata("fingerprint", hash)
           hash= " # "+ hash
        

        
        
        if "clear"in kw["action_type"] :
            
            a= ActionChains(self.driver)
            a.key_down(Keys.CONTROL)
            a.send_keys("a")
            a.key_up(Keys.CONTROL)
            a.perform()

        string= kw["action_type"]["value"]+hash
        action = ActionChains(self.driver)
        action.send_keys(string)
        action.perform()
    

    def start_switch_to_alert(self, kw):
        self.selector(**kw["selector"])
        self.action_type(attr="click")

        self.driver.switch_to.alert.accept()



    def start_switch_to_window(self, kw):
        
        self.selector(**kw["selector"])
        self.action_type(attr="click")
        
        child = self.driver.window_handles[-1]
        self.driver.switch_to.window(child)          
    



    def end_switch_to_window(self, kw):
        print("_______________________")
        
        
        self.driver.switch_to.window(self.driver.window_handles[0])        
        
    def input_select(self, kw):
        self.selector(**kw["selector"])
        select = Select(self.elements[0])
        select.select_by_visible_text(**kw['input'])

    def random_select(self, kw):
        self.selector(**kw["selector"])
        select = Select(random.sample(self.elements, 1))
        #select.select_by_visible_text(**kw['input'])


    def multi_select(self, kw):
        self.selector(**kw["selector"])
        
        
        
        if "invisibility_element" in kw:            
            self.invisibility_element(**kw["invisibility_element"])           
        try:
            self.partial_elements(".//li")
            self.randomize().action_type(attr="click")
        except Exception as e :
            return "multi_select"
        
        
    
    def random_select(self, kw):            
        self.selector(**kw["selector"])
        self.partial_elements(".//option")
        if "skip" in kw:
            self.elements= [ element  for element in self.elements if element.text != kw["skip"]["text"] ]
        self.randomize().action_type(attr="click")


    def input_text(self, kw):
        def clear():
                self.action_type(attr="send_keys", value=Keys.CONTROL + "a" )
                self.action_type(attr="send_keys", value=Keys.DELETE )
        
        def delta_form(kw):
            sleep(0.5)
            print("env >>>>>>>", kw["env"])
            Type = kw["delta_form"]["type"]
            
            delta =  [ el for el in  kw["selenium_parameters"] if kw["env"] in el.values() and  Type in el.values()  ]
            
            delta= random.sample(delta,1)
            
            
            delta = delta[0][kw["delta_form"]["field"]]
            action_type = {"attr": "send_keys", "value": delta}
            
            return action_type
            

        
        self.check_element(kw)
               
        self.selector(**kw["selector"])

        if not re.search( "input", kw["selector"]["value"]) and not  re.search( "textarea", kw["selector"]["value"]):            
            self.partial_elements(".//input[@type='text' or @type='password' or @type='email' or @type='search' ] | .//textarea")
            

        self.action_type(attr="click")

        if "test" in kw:
            
            self.keys_test()
            self.action_type(attr="send_keys", value=Keys.ENTER )
            
            clear()
            
        if  "clear" in  kw["action_type"]:
            if  kw["action_type"]["clear"] == True:
                clear()
                del kw["action_type"]["clear"]
        
        
        hash =""
        if "fingerprint" in kw:
            hash= " # "+ self.fingerprint(**kw["fingerprint"])
            
            kw["action_type"]["value"] = kw["action_type"]["value"]+hash
        
        
        
        if "delta_form" in kw:            
           
           kw["action_type"] = delta_form(kw)
           
           self.action_type(**kw["action_type"])
           sleep(3)
        else:
           
            self.action_type(**kw["action_type"])
        
        
        


    def input_checkbox(self, kw):
        self.selector(**kw["selector"])
        self.partial_elements(".//input[@type='checkbox' and not(@checked) ]")
        self.randomize().action_type(attr="click")

    def random_input_select(self, kw):
        self.selector(**kw["selector"])
        self.randomize().action_type(attr="click")

        
       
    def input_radio(self,kw):
        self.selector(**kw["selector"])        
        self.partial_elements(".//input[@type='radio']")
        self.randomize().action_type(attr="click")
    
    def select_click(self, kw):
        
        self.execute_script()

        self.check_element(kw)      
        
        self.action_type(attr="click")
    
    
    
    def refresh_select_click(self, kw):

        self.execute_script()


        self.refresh_to_find_element(kw)

        


        
    def list_select_click(self, kw):
        
        self.selector(**kw["selector"])
                             

    def upload_file(self, kw):

        mypath= "configs "+ self.load_app +" include files "+kw["selector"]["type"]

        
        mypath = mypath.split(" ")
        mypath = (os.sep).join(mypath)

        mypath = os.getcwd()+ os.sep + mypath 

        f = os.listdir(mypath)
        mypath= mypath + str(os.sep) + random.sample(f, 1)[0]


        sleep(3)
        
        pyautogui.typewrite(mypath, interval=0.03 )
        pyautogui.press('enter')


   
    def get_screenshot(self):

        try:
            now = datetime.datetime.now()
            img_path= "{}{}{}{}{}{}.png".format(now.year, now.month,now.day,now.hour, now.minute,now.second)
            img_path= os.getcwd() + os.sep + "tmp" + os.sep + img_path    
             

            if  len(self.driver.window_handles) == 2:                       
                child = self.driver.window_handles[1]
                self.driver.switch_to.window(child)
                self.driver.save_screenshot(img_path)
            
            if len(self.driver.window_handles) == 1:
            
                self.driver.save_screenshot(img_path)

            return  img_path

        except NoSuchWindowException as e:
            pprint(e.msg)

    

        


    
    def check_validation(self, kw ):
        self.selector(**kw["selector"])               
             
        flag = []
        for text in kw["text"]["match"]:
            if self.match_text(text["check_text"]):
                data = "correcto"
            else:
                data = "incorrecto"
        
            flag.append( {"estado": data, "text" : text["check_text"]})
            
        self.validation ={"flag" : flag,
                          "description" : kw["text"]["description"]
        }
        

    
    def dir_pdf(self):
        now = datetime.datetime.now()
        directory =os.getcwd()+os.sep+ "pdf_report" + os.sep + "{}_{}_{}_{}_{}_{}".format(now.year, now.month,now.day,now.hour, now.minute,now.second)

        if not os.path.exists(directory):
            os.makedirs(directory)
            return directory
        else:
            return False
    
    def move_over_element(self, kw):
        self.selector(**kw["selector"])
        if len(self.elements) == 1:       
            actions = ActionChains(self.driver)
            actions.move_to_element(self.elements[0])
            actions.perform()


    def reload_page(self,kw):

        print("reload_page")
        while self.check_element_exist(**kw["selector"]) :
            self.driver.refresh()
            sleep(2)
    

    def filter_select_bootstrap(self, kw):
        self.execute_script()



        search = ["de", "la", "le", "en"]

        if "words" in kw:
            search = kw["words"]["match"].split(", ")
            pprint(search)
        
        

        search = sample(search, 1)
        search = search[0]

        self.selector(**kw["selector"])

        self.action_type(attr="click")
                
        self.partial_elements(".//input")

        self.action_type(attr="send_keys", value=search)

        self.check_exists_element(selector='xpath', value="//ul[@class='select2-results__options']/li[not(contains(@class,'loading-results')) and not(contains(@class,'select2-results__message'))]")
        
        self.selector(selector="xpath",value="//ul[@class='select2-results__options']/li" )
        
        self.randomize().action_type(attr="click")


        
 
                

        
        

