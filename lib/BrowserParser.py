 # -*- coding: utf-8 -*-
from datetime import datetime
from tkinter import NO
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions  import ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait   
from time import sleep
import random
from  .BrowserManager import BrowserManager 
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint
import unicodedata
import hashlib
import re
from selenium.webdriver.support.ui import WebDriverWait

class BrowserParser(BrowserManager):

    elements = []
    
    value=None
    selectors=None
    def __await_to_select(self, selector=None, value=None ):
        
        try:
            self.presence_elements(selector=selector, value=value)
           # self.clickable(selector=selector, value=value)
            #self.visibility_element(selector=selector, value=value)
        except WebDriverException as wde:
            print( "WebDriverException =====", str(wde.msg))
            raise
    
    def selector(self, selector=None, value=None):
        '''
        :param kwargs:
        :return:

        CLASS_NAME = 'class name'
        CSS_SELECTOR = 'css selector'
        ID = 'id'
        LINK_TEXT = 'link text'
        NAME = 'name'
        PARTIAL_LINK_TEXT = 'partial link text'
        TAG_NAME = 'tag name'
        XPATH = 'xpath'
        '''
        self.value=value

        self.selectors= selector

        
        self.elements = self.driver.find_elements(getattr(By,  selector.upper() ), value)
        
        
      
    def randomize(self):
        #ToDo set by positio
        try:
            
            self.elements =  random.sample(self.elements,1)
        except ValueError as e:
            pprint(">>>>>>> ValueError")
            raise 
               
        return self
    
    def keys_test(self):
        
        n_ch =random.randint(20,90)
        
        k =  ["NUMPAD0", "NUMPAD1", "NUMPAD2", "NUMPAD3", "NUMPAD4", "NUMPAD5", "NUMPAD6", "NUMPAD7", "NUMPAD8", "NUMPAD9"
        , "SEPARATOR", "EQUALS", "HELP", "BACKSPACE", "TAB"
        , "RETURN", "ENTER", "SHIFT", "CONTROL", "ALT", "PAUSE", "ESCAPE", "SPACE", "PAGE_UP", "PAGE_DOWN", "END", "HOME", "LEFT", "UP", 
        "RIGHT",  "DOWN", "INSERT", "DELETE", "SEMICOLON", "EQUALS", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12","ADD",
        "SEPARATOR", "SUBTRACT", "DECIMAL", "DIVIDE"]
        
        ch= "` ¬ | ° ´ ó ú é á à è ù ò !¸ } ] ¬ ½ · @ # $ % & / ( ) = ? ' \ ¡ ¿ < > - _ : . ; * - + ' ö ä ë r ÿ ü ï q ~ } [ { ] Ñ ñ ^ û   ô ê î ŝ ĝ ĥ â ĉ b"
        ch = ch.encode('utf-8').decode("utf-8").split(" ")

        n = 0
        while n_ch > n:
            n +=1
            random.shuffle(k)            
            random.shuffle(ch)                        
            self.action_type(attr="send_keys", value=getattr(Keys, k[0] ))            
            self.action_type(attr="send_keys", value= ch[0])            
        #self.selector(selector="xpath", value="//*[@type='submit']")
        #self.action_type(attr="click")
        #self.action_type(attr="send_keys", value=Keys.ENTER)
        sleep(3)
        
       

    def core_action_type(self, attr='text', value=False, clear=False):
            if attr in ["click", "clear"]:
                # methods
                [getattr(element, attr)() for element in self.elements]
                print("ok -> click")
                
            elif value:
                # methods and params
                [getattr(element, attr)(value) for element in self.elements]
                print("ok -> value")
                    
            else:
                # properties
                [getattr(element, attr) for element in self.elements]

                print("properties ")
                    

    def action_type(self, **kw):
        self.execute_script()


        t = 0
        while t < 10 :
            
            self.check_element(kw)
            try:
                
                self.core_action_type(**kw)
                break
            except ElementClickInterceptedException as a:
                t += 1
                print("ElementClickInterceptedException") 
                
                try:
                    
                    
                    self.driver.execute_script("arguments[0].click();", self.elements[0])
                    #self.move_to_element(i)
                    break
                    
                except Exception:
                    t += 1
            
                print(a.msg)
                self.execute_script()
                
            except  StaleElementReferenceException as sere :
                
                t +=1

                
                pprint("<<<<<<<< StaleElementReferenceException  >>>>>  "+ sere.msg )

                self.selector(value=self.value, selector=self.selectors)

    
            except ElementNotInteractableException as e :
                t += 1
                print( "<<<<<<< ElementNotInteractableException >>>>>  "+ e.msg)
                
                #TODO refator de estot
                
                action = ActionChains(self.driver)
                action.move_to_element(self.elements[0])
                action.click()
                action.perform()
                break
                #TODO refator de estot++t
            
                
                
            print(t)
        return self
                
        
    def partial_elements(self, xpath):
        try:
            self.elements = [element.find_elements(By.XPATH,  xpath) for element in self.elements]
        except NoSuchElementException as nsee:
            pprint("NoSuchElementException partial_elements  ")
            raise "NoSuchElementException " + str(nsee.msg)


        if len(self.elements) == 1:
            self.elements = self.elements[0]
        
        return self
    
    def move_to_element(self):        
        action= ActionChains(self.driver)
        [action.move_to_element(element) for element in self.elements]
        action.perform()
    
      
    
    def match_text(self, validation):

        def normalize(text):
           text= unicodedata.normalize("NFKD", text).encode("ascii","ignore").decode("ascii")
           text = text.upper()
           text = text.replace(" ", "")
           text = text.replace(",", "")
           text = text.replace(".", "")
           text = text.strip('\n')
           text = text.strip('\r')
           

           return text

        text = [normalize(i.text) for i in self.elements ]   
        match = normalize(validation)
       
        if match in text:
           return True
        else :
           return False
    

    def fingerprint(self, kind=None  ):
        
        now=datetime.now()

        timestamp = " {}:{}:{}:{},{},{} ".format(now.year, now.month,now.day,now.hour, now.minute,now.second)

        md5 = hashlib.md5(timestamp.encode('utf-8')).hexdigest()

        number = " {}{}{}{}{}{} ".format(now.year, now.month,now.day,now.hour, now.minute,now.second)
        
        if kind ==  "timestamp":
            fp= timestamp
        elif kind == "md5":                
            fp=md5
        elif kind == "number":
            fp = number
        
        return fp
    
    def parse_url(self,url):
        m = re.search('(\d+)', url)

        if m:
            return m.group(0)
        else:
            return None

    def list_of_elements(self, xpath):

        self.selector(selector="xpath", value=xpath)

        while len(self.elements)  == 1:            
            self.list_of_elements(xpath)

        return self
    
    def refresh_to_find_element(self, kw):

            
        t = True
        while t  :
            try:
                
                
                self.check_element(kw)
                
                self.action_type(attr="click")
            
                t=False
            except  StaleElementReferenceException as sere :
                
                t =True
                

                #self.core_action_type(attr, value, clear)
                
                pprint("<<<<<<<< StaleElementReferenceException  >>>>>  "+ sere.msg )

                # TODO refator de esto 
                self.driver.refresh()

                self.check_element(kw)

    

    def check_element(self, kw):
        
        
        if "move_to_element" in kw:
            self.selector(**kw["move_to_element"])
            self.move_to_element()        
        
        if "visibility_element" in kw:
           self.visibility_element(**kw["visibility_element"])
        
        if "invisibility_element" in kw:
            
            self.invisibility_element(**kw["invisibility_element"])


        if "presence_element" in kw:
            self.presence_element(**kw["presence_element"])
        
        
        if "clickable" in kw:
            self.clickable(**kw["clickable"])

        
        if "selector" in kw:
            self.selector(**kw["selector"]) 
        
         




        
     