#from importlib.resources import path
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
import json
from .MetaData import MetaData
from time import sleep


class BrowserManager(MetaData):
    driver= None

   
    
    def chrome(self,url):

        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(url)
        self.driver.maximize_window()

        
        
        return self.driver
        
    
    def firefox(self,url):
        caps = DesiredCapabilities.FIREFOX
        caps['loggingPrefs'] = {'browser': 'ALL'}

        
        self.driver = webdriver.Firefox()
        #pprint(self.driver.get_log('browser'))
        
        self.driver.get(url)
        self.driver.maximize_window()
        
                          
                    
    
    def get_html(self):
        html = self.driver.page_source
        return html

    def get_status(self):
        
        d = self.logs()
        try:
            content_type = 'text/html' in d['message']['params']['response']['headers']['content-type']
            response_received = d['message']['method'] == 'Network.responseReceived'
            if content_type and response_received:
                return d['message']['params']['response']['status']
        except:
            pass

    def logs(self):
        logs = self.driver.get_log("performance")
        
        for log in logs:
            for _, k in log.items():
                #pprint(k)
                if  isinstance(k, str):
                    if not "INFO" in k:
                        if "message" in k:
                            return json.loads(k)

       
    
    def execute_script(self):
        script="""
            function remove_bar (){
                a= document.querySelector(".phpdebugbar")
                a.parentElement.removeChild(a);
                b= document.querySelector(".phpdebugbar-openhandler")
                b.parentElement.removeChild(b);
                c= document.querySelector(".phpdebugbar-openhandler-overlay")
                c.parentElement.removeChild(c);
            }
                $(document).ready(function(){ remove_bar() })
        """
        try:
            
            self.driver.execute_script(script)
        except WebDriverException as e:
            return "<<<<<<<< execute script >>>>>>>>>>>>>>>"

    
    def finish(self):
        self.driver.quit()
    

    #def server_proxy(self):
    #    server = Server("./tools/browsermob-proxy-2.1.4/bin/browsermob-proxy")
    #    return server.create_proxy({'captureHeaders': True, 'captureContent': True, 'captureBinaryContent': True})

    def chrome_options(self):
        co = webdriver.ChromeOptions()
        co.add_argument('--proxy-server={host}:{port}'.format(host='localhost', port=self.server_proxy().port))
        return co


    def firefox_profile(self):
        pass
    
        
    def invisibility_element(self, selector=None, value=None):
        
        try:
            wait = WebDriverWait(self.driver, 40)
            wait.until(EC.invisibility_of_element_located((getattr(By,  selector.upper()), value)))
        except TimeoutException as te:
            print("invisibility_element  >>>>> ", str(te.msg))
            raise    
    
    def visibility_element(self, selector=None, value=None):
        

        try:
            wait = WebDriverWait(self.driver, 40)
            wait.until(EC.visibility_of_element_located((getattr(By,  selector.upper()), value)))
        except TimeoutException as te:
            print("visibility_element  >>>>> ", str(te.msg))
            raise   
        
        
    
    def presence_elements(self, selector=None, value=None):
        
        try:
            wait = WebDriverWait(self.driver, 40)
            wait.until(EC.presence_of_all_elements_located((getattr(By,  selector.upper()), value)))
        except TimeoutException as te:
            print("presence_elements ", str(te.msg))
            
        except WebDriverException as wd:
            print("WebDriverException ->>>>", str(wd.msg))
    
    def presence_element(self, selector=None, value=None):
        try:
            wait = WebDriverWait(self.driver, 40)
            wait.until(EC.presence_of_element_located((getattr(By,  selector.upper()), value)))
        except TimeoutException as te:
            print( " presence_element >>>>  " + str(te.msg))
            
        except WebDriverException as wd:
            print("WebDriverException ->>>>", str(wd.msg))
    
    
    def available_and_switch_to_it(self, selector=None, value=None):
        try:
            wait = WebDriverWait(self.driver, 40)
            wait.until(EC.frame_to_be_available_and_switch_to_it((getattr(By,  selector.upper()), value)))
            
        except NoSuchWindowException as te:
                print("NoSuchWindowException", str(te.msg))
                raise


    def clickable(self, selector=None, value=None):
        try:
            wait = WebDriverWait(self.driver, 40)
            wait.until(EC.element_to_be_clickable((getattr(By,  selector.upper()), value)))
            return True
        except NoSuchWindowException as te:
            print("NoSuchWindowException", str(te.msg))
            return False
    

    def check_element_exist(self, selector=None, value=None):
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((getattr(By,  selector.upper()), value)))
            return True
        except Exception as te:
            print("NoSuchWindowException", str(te.msg))
            return False


    def check_exists_element(self, selector=None, value=None):
        
        is_element= True

        while is_element:
            try:
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.presence_of_element_located((getattr(By,  selector.upper()), value)))
                is_element=False
            except NoSuchElementException:
                is_element= True
            
