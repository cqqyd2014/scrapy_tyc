import selenium
import random
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from python_common.common import DataClear


dc=DataClear()


def hand_scroll(driver):
        t=random.uniform(500, 1000)
        js_scroll = "var q=document.documentElement.scrollTop="+str(t)  # documentElement表示获取根节点元素
        driver.execute_script(js_scroll)


def hand_wait(start,end):
        t=random.uniform(start, end)
        time.sleep(t)
def hand_type_word_wait():
        hand_wait(0.1,1)
def hand_browse_webpage_wait():
        hand_wait(5,20)
def hand_focus_move_wait():
        hand_wait(1,3)


def hand_send_keys(input_control,input_text):
    for word in input_text:
        hand_type_word_wait()
        input_control.send_keys(word)

def hand_browser_get(browser,url):

        browser.get(url)
        t=random.uniform(0.1, 1)


def hand_click(button):
        button.click()


def hand_find_date_element(webdriver,byMethod,value):
        element_text=hand_find_text_element(webdriver,byMethod,value)
        if element_text==None:
                return None
        else:
                return dc.text_to_date(element_text)
        
def hand_find_int_element(webdriver,byMethod,value):
        element_text=hand_find_text_element(webdriver,byMethod,value)
        if element_text==None:
                return None
        else:
                return dc.text_to_int(element_text)

def hand_find_text_element(webdriver,byMethod,value):
        element=hand_find_element(webdriver,byMethod,value)
        if element==None:
                return None
        else:
                element_text=element.text if element.text!='-' else None
                
                return element_text

def hand_find_element(webdriver,byMethod,value):
        element=None
        try:
                element=webdriver.find_element(byMethod,value)
        except selenium.common.exceptions.NoSuchElementException as e:
                pass
        return element

# 智能等待10s之后获取元素，获取的是多个元素
def hand_find_list_elements_by_list_pars(webdriver,list_pars):
        all_elements=[]
        for par in list_pars:
                #print(par)
                try:
                        elements = WebDriverWait(webdriver, 10).until(EC.presence_of_all_elements_located((par['method'],par['value'])))
                        all_elements.extend(elements)
                        
                        
                except selenium.common.exceptions.TimeoutException as e:
                        pass
        return all_elements
                
    