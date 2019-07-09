from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from  hand_common import hand_browse_webpage_wait,hand_browser_get,hand_focus_move_wait,hand_send_keys\
    ,hand_find_text_element,hand_click,hand_find_list_elements_by_list_pars,hand_find_int_element,hand_find_date_element\
        ,hand_find_text_element,hand_find_element,hand_scroll
from scrapy_tyc_orm.orm import create_session,CompanyBaseInfo
import selenium
from python_common.common import DataClear



class ScrapyTyc:
    dc=DataClear()

    
    def  __init__(self,user_name,password):
        
        chrome_driver='D:\software\chromedriver.exe'
        driverOptions = webdriver.ChromeOptions()
        
        driverOptions.add_argument(r"user-data-dir=D:\temp")
        self.driver = webdriver.Chrome(executable_path=chrome_driver,chrome_options=driverOptions)
        '''
        self.profileDir = r'D:\temp\fszippeh.default'
        self.user_name=user_name
        self.password=password
        self.profile = webdriver.FirefoxProfile(self.profileDir)
        self.driver = webdriver.Firefox(self.profile)
        '''
        hand_browser_get(self.driver,"https://www.tianyancha.com/")
        #检查是否登陆

    def search_by_name(self,search_name):
        hand_browse_webpage_wait()
        element_input_search = self.driver.find_element(By.XPATH,'//*[@id="home-main-search"]')
        hand_send_keys(element_input_search,search_name)
        hand_focus_move_wait()
        element_button_seatch=self.driver.find_element(By.XPATH,'//div[@class="input-group-btn btn -xl"]')
        hand_focus_move_wait()
        hand_click(element_button_seatch)
        element_company_links=None
        self.search_list_handle = self.driver.current_window_handle
        hand_browse_webpage_wait()


        

    def search_by_name_get_accurate_list(self,search_name):
        self.search_by_name(search_name)
        #读取页面的单位列表
        return hand_find_list_elements_by_list_pars(self.driver,[
            {'method':By.XPATH,'value':'//a[@class="name "]/em[text()="'+search_name+'")]/..'}
           ]
            
                       
        )

    def search_by_name_get_vague_list(self,search_name):
        self.search_by_name(search_name)
        #读取页面的单位列表
        return hand_find_list_elements_by_list_pars(self.driver,[
            {'method':By.XPATH,'value':'//a[@class="name "]/em[contains(text(),"'+search_name+'")]/..'}
            ,{'method':By.XPATH,'value':'//a[@class="name "]'}]
            
                       
        )

    #解析查询出来的{c_company_id:,c_name:,c_tianyancha_link:}
    def get_search_company_info(self,element_company):
        tianyancha_company_href=element_company.get_attribute('href')
        flag=tianyancha_company_href.index("/company/")
        c_company_id=tianyancha_company_href[flag+9:len(tianyancha_company_href)-1]
        c_name=element_company.text()
        return {'c_company_id':c_company_id,'c_name':c_name,'c_tianyancha_link':tianyancha_company_href}
    def get_search_companys_info(self,elements_company):
        companys_info=[]
        for element_company in elements_company:
            companys_info.append(self.get_search_company_info(element_company))
        return companys_info


       


    #打开各种页面的装饰器
    def handle_open_page(func):
        
        def _decorate(driver,c_type,c_id):
            early_handles = driver.window_handles

            #记录当前的windows句柄
            current_window_handle=driver.current_window_handle
            #https://www.tianyancha.com/company/2972836685
            #https://www.tianyancha.com/human/1998872833-c2972836685
            
            driver.execute_script('window.open("https://www.tianyancha.com/'+c_type+'/'+c_id+'");')
            #新的句柄集合
        
            later_handles = driver.window_handles
            new_handle=None
            for handle in later_handles:
                if handle not in early_handles:
                    new_handle=handle
            driver.switch_to.window(new_handle)
            hand_browse_webpage_wait()
            hand_scroll(driver)
            hand_browse_webpage_wait()
            func()
            driver.close()
            driver.switch_to.window(current_window_handle)
        return _decorate
    



    #查询结果的企业信息
    @handle_open_page
    def get_company_main_info(self,company_url):
        
       

        #单位名称
        c_name_h1=self.driver.find_element(By.XPATH,'.//div[contains(@class, "header")][1]/h1')
        #注册资本
        c_reg_capital=hand_find_int_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[1]/td[2]/div')
        
        c_real_capital=hand_find_int_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[1]/td[4]')
        
        c_start_date=hand_find_date_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[2]/td[2]/div')
        
        c_status=hand_find_text_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[2]/td[4]')

        c_uscc=hand_find_text_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[3]/td[2]')
        
        c_reg_code=hand_find_text_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[3]/td[4]')
        
        c_tax_code=hand_find_text_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[4]/td[2]')

        c_org_code=hand_find_text_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[4]/td[4]')

        c_type=hand_find_text_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[5]/td[2]')
        
        c_industry=hand_find_text_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[5]/td[4]')
        
        c_permit_date=hand_find_date_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[6]/td[2]')

        c_permit_gov=hand_find_text_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[6]/td[4]')

        c_business_period=hand_find_text_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[7]/td[2]/span')

        c_tax_level=hand_find_text_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[7]/td[4]')

        c_staff=hand_find_text_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[8]/td[2]')

        c_social_security_staff=hand_find_int_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[8]/td[4]')

        c_old_name=hand_find_text_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[9]/td[2]')

        c_english_name=hand_find_text_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[9]/td[4]')

        c_addr=hand_find_text_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[10]/td[2]')

        c_business=hand_find_text_element(self.driver,By.XPATH,'//*[@id="_container_baseInfo"]/table[2]/tbody/tr[11]/td[2]/span')

        companyBaseInfo=CompanyBaseInfo(c_business=c_business,c_addr=c_addr,c_english_name=c_english_name,c_old_name=c_old_name,c_social_security_staff=c_social_security_staff,c_staff=c_staff,c_tax_level=c_tax_level,c_business_period=c_business_period,c_permit_gov=c_permit_gov,c_permit_date=c_permit_date,c_industry=c_industry,c_type=c_type,c_org_code=c_org_code,c_tax_code=c_tax_code,c_reg_code=c_reg_code,c_uscc=c_uscc,c_start_date=c_start_date,c_company_id=c_company_id,c_name=c_name_h1.text,c_reg_capital=c_reg_capital,c_real_capital=c_real_capital)
        companyBaseInfo.saveOfUpdate(db_session)
        db_session.commit()
        db_session.close()

       


    #主要股东
    def shareholder(self):
        #定位股东表格
        table_shareholder=hand_find_element(self.driver,By.XPATH,'//*[@id="_container_holder"]/table/thead/tr/th[2][contains(text(),"股东（发起人）")]/../../..')
        table_rows = table_shareholder.find_elements_by_tag_name('tr')
        rows_len=len(table_rows)
        flag=1
        while flag<=rows_len:
            shareholder_order=dc.text_to_int(table_rows[flag].find_elements_by_tag_name('td')[0].text)
            element_shareholder = table_rows[flag].find_elements_by_tag_name('td')[1]
            shareholder_name=element_shareholder.text
            shareholder_href=element_shareholder.get_attribute('href')
            shareholder_percent = dc.text_to_float(table_rows[flag].find_elements_by_tag_name('td')[2].text)
            shareholder_amount = dc.text_to_float(table_rows[flag].find_elements_by_tag_name('td')[3].text)
            flag+=1
        


    def scrap_end(self):
        self.driver.close()

