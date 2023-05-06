import os
from uuid import uuid4
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import polars as pl
from selenium.webdriver.common.by import By
from bot.constants import IMPLEMENTED
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,ElementNotInteractableException
import logging
from selenium.webdriver.support import expected_conditions
import time 

class UcChromeDriver(uc.Chrome):
    """"
    Description:
    This class is a wrapper for the undetected_chromedriver package but with basic options

    """

    def __init__(self)->None:
       

        options = webdriver.ChromeOptions()

        options.add_argument('--log-level=1')
        # Adding argument to disable the AutomationControlled flag 
        options.add_argument("--disable-blink-features=AutomationControlled") 
        
        # Exclude the collection of enable-automation switches 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        
        # Turn-off userAutomationExtension 
        options.add_experimental_option("useAutomationExtension", False)
        
        self.driver = uc.Chrome(executable_path="chromedriver",chrome_options=options)
                              
        # driver.set_window_size(1920,1080)
        
    def get_driver(self):
        return self.driver
    

class Bot:
    """
    Description:
    """
    def __init__(self,
                 website:str,
                 job_title:str="Data Scientist",
                 search_location:str="Paris",
                 ) -> None:
        
       
        if website not in list(IMPLEMENTED.keys()):
            raise NotImplementedError(f"{website} not implemented yet")
        
        self.job_title = job_title
        self.search_location = search_location
        
        self.website = website

        self.driver = UcChromeDriver().get_driver()
        self.driver.implicitly_wait(5)
        
        self.CONSTANTS = IMPLEMENTED[website]
        self.wait = WebDriverWait(self.driver, 5,poll_frequency=0.2)

    def find_element_try(self,element=None,verbose=False,*args,**kwargs):
        """
        Description:
        This method will try to find an element and return None if it fails"""
        try:
           if element:
               return element.find_element(*args,**kwargs)
           return self.driver.find_element(*args,**kwargs)
        except NoSuchElementException as e:
            if verbose:
                print(e)
            return None


    def save_offers(self,offers,schema=None):
        """"
        Description:
        This method will save the offers in parquet format"""
        if offers:
            if offers[0]["job_title"]:
                try:
                    pl.DataFrame(
                        offers,
                        schema=schema
                    ).write_parquet(f"{self.CONSTANTS['DATA_PATH']}/{self.website}_{uuid4()}.parquet")
                except Exception as e:
                    print(offers)
                    print(e)

    def get_offers_off_page(self):
        """
        Description:
        This method will get the offers on the page and return a list of offers"""
        
        # self.wait.until(EC.visibility_of_all_elements_located(self.CONSTANTS["LIST_PAGE_OFFERS"]))

        return self.wait.until(EC.visibility_of_all_elements_located(self.CONSTANTS["LIST_PAGE_OFFERS"]))
    
    def search_job(self):
        """
        
        Description:
        This method will search the job title in the search bar and click on the search button"""
 
        self.driver.get(self.CONSTANTS["START_URL"])
        
        search_bar = self.wait.until(EC.visibility_of_element_located(tuple(self.CONSTANTS["SEARCH_BAR"].values()) ))

        webdriver.ActionChains(self.driver).move_to_element(search_bar).click().perform()
    
        webdriver.ActionChains(self.driver).send_keys(self.job_title).perform()
        # self.driver.find_element(**self.CONSTANTS["SEARCH_BAR"])
        location  = self.driver.find_element(**self.CONSTANTS["SEARCH_LOCATION"])
    
        location.send_keys(Keys.CONTROL + "a")
        location.send_keys(Keys.DELETE)
        location.clear()
   
        webdriver.ActionChains(self.driver).move_to_element(location).click().perform()
        
        # self.search_location=""
        location.send_keys(self.search_location)
        location.send_keys(Keys.ENTER)






        self.page = 1

        self.offers = []

    



class IndeedBot(Bot):
    """
    Description:
    This class is a bot that will scrap the indeed website and save the data in parquet forma
    """
    
    def __init__(self,
                 *args,
                 **kwargs
                 ) -> None:
        """
        Description:
        This method is the constructor of the class
        Parameters:
        job_title: str
        This parameter is the job title that will be searched
        @TODO: Add a parameter to choose the location
        """
        super().__init__("indeed", 
                          *args,
                        **kwargs)
        
    def run(self):
        """
        Description:
        This method is the main method of the class, it will run the bot and save the data in parquet format
        @TODO : Add a method to save the data in a database
        @TODO : Implement logging
        """
        self.search_job()

        while self.page:
       
            if self.page != 1:
                self.driver.get(self.page.get_attribute('href'))
                webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        
            result_list = self.get_offers_off_page()
            self.go_trough_offers(result_list)
            self.next_page()
            self.save_offers(self.offers)
            # page = None
        self.driver.quit()
        print("Done")
        
        
    def next_page(self):
        """
        Description:
        This method will find the next page button"""
        self.page = self.find_element_try(**self.CONSTANTS["NEXT_PAGE"])

    
    
    def go_trough_offers(self,result_list):
        """
        Description:
        This method will go trough the offers and save the data in a list of dict"""

        for offer in result_list:

                offer_dict= dict()
                for i in ("job_title","id","company","text","salary_range"):
                    offer_dict[i]=None
                try:
                    os.listdir(self.CONSTANTS["DATA_PATH"])
                    list_fetch_ids = pl.scan_parquet(f'{self.CONSTANTS["DATA_PATH"]}/*.parquet').filter(pl.col("text").is_not_null()).select(pl.col("id").unique()).collect().to_series() 

                except FileNotFoundError as e :
                    list_fetch_ids = []
                try:
                    
                    offer_dict['id'] = offer.find_element(**self.CONSTANTS["OFFER_ID"]).get_attribute('id')
                    if offer_dict['id']  not in list_fetch_ids:
                        
                        offer_dict["job_title"] =offer.find_element(**self.CONSTANTS["OFFER_TITLE"]).text
                        offer_dict["company"] = offer.find_element(**self.CONSTANTS["OFFER_COMPANY"]).text
                        webdriver.ActionChains(self.driver).move_to_element(offer).click(offer ).perform()
                        text_offer =self.driver.find_element(*self.CONSTANTS["OFFER_TEXT"])
                        offer_dict["text"] = text_offer.text
                        offer_dict["salary_range"] = offer.find_element(**self.CONSTANTS["OFFER_SALARY"]).text
                        self.offers.append(offer_dict)

                except Exception as e:
                    print(offer_dict.get("id",None))
                    print(e)
    


  
    


class GlassdoorBot(Bot):
    """
    Description:
    This class is a bot that will scrap the glassdoor website and save the data in parquet forma
    """
    
    def __init__(self,
                 *args,
                 **kwargs
                 ) -> None:
        """
        Description:
        This method is the constructor of the class
        Parameters:
        job_title: str
        This parameter is the job title that will be searched
        """
        super().__init__("glassdoor", 
                          *args,
                        **kwargs)
        

    def run(self):
        self.search_job()
        while self.page:
       
            if self.page != 1:
                # self.driver.get(self.page.get_attribute('href'))
                webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        
            result_list = self.get_offers_off_page_glassdoor()
            self.go_trough_offers(result_list)
            self.next_page()
            # s
            # self.save_offers(self.offers,schema=schema)
            # page = None
        schema = dict(
                job_title=pl.Utf8(),
                id=pl.Utf8(),
                company=pl.Utf8(),
                text=pl.Utf8(),
                salary_range=pl.Utf8(),
                location=pl.Utf8(),
                age=pl.Utf8(),
                company_rating=pl.Utf8(),
                company_info=pl.Utf8(),
                is_easy_apply=pl.Utf8(),
                salary_range_provenance=pl.Utf8()

            )
        self.save_offers(self.offers,schema=schema)
        self.driver.quit()
        print("Done")
    def get_offers_off_page_glassdoor(self):
       


        """
        Description:
        This method will get the offers on the page and return a list of offers"""
        
        # self.wait.until(EC.visibility_of_all_elements_located(self.CONSTANTS["LIST_PAGE_OFFERS"]))
        offers= self.wait.until(EC.visibility_of_all_elements_located(self.CONSTANTS["LIST_PAGE_OFFERS"]))
        offer_list = []
        for offer in offers:
            ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
            o = WebDriverWait(self.driver, 10,ignored_exceptions=ignored_exceptions).until(expected_conditions.visibility_of(offer
                                                                                                                                           )).get_attribute('data-id')

    
            offer_list.append(o)

        return offer_list
    def next_page(self):
        """
        Description:
        This method will find the next page button"""
        self.page = self.driver.find_element(**self.CONSTANTS["NEXT_PAGE"])
        if self.page:
            webdriver.ActionChains(self.driver).move_to_element(self.page ).click(self.page ).perform()
        else:
            print("No more pages")

            
    
    def go_trough_offers(self,result_list):
        """
        Description:
        This method will go trough the offers and save the data in a list of dict"""
        self.count = 0
        for c,offer in enumerate(result_list):
            
            self.count = c + 1
        
            offer_dict= dict()
            for i in ("job_title","id","company","text","salary_range","location","age","company_rating","company_info","is_easy_apply","salary_range_provenance"):
                offer_dict[i]=None
            try:
                os.listdir(self.CONSTANTS["DATA_PATH"])
                list_fetch_ids = pl.scan_parquet(f'{self.CONSTANTS["DATA_PATH"]}/*.parquet').filter(pl.col("text").is_not_null()).select(pl.col("id").unique()).collect().to_series() 

            except FileNotFoundError as e :
                list_fetch_ids = []
           
               
            offer_dict['id'] = offer

            if offer_dict['id']  not in list_fetch_ids:
                
                # offer_dict["job_title"] =offer.find_element(**self.CONSTANTS["OFFER_TITLE"]).text
                offer_xpath = f"//li[@data-id='{offer_dict['id']}']"
                location_xpath = f"//li[@data-id='{offer_dict['id']}']" + self.CONSTANTS["OFFER_LOCATION"]["value"]
                age_xpath = f"//li[@data-id='{offer_dict['id']}']" + self.CONSTANTS["OFFER_AGE"]["value"]
                company_rating_xpath = f"//li[@data-id='{offer_dict['id']}']" + self.CONSTANTS["COMPANY_RATING"]["value"]
                company_info_xpath = f"//li[@data-id='{offer_dict['id']}']" + self.CONSTANTS["COMPANY_INFO"]["value"]
                is_easy_apply_xpath = f"//li[@data-id='{offer_dict['id']}']" + self.CONSTANTS["OFFER_IS_EASY_APPLY"]["value"]
                
                salary_range_provenance_xpath = f"//li[@data-id='{offer_dict['id']}']" + self.CONSTANTS["OFFER_SALARY_PROVENANCE"]["value"]
                salary_range_xpath = f"//li[@data-id='{offer_dict['id']}']" + self.CONSTANTS["OFFER_SALARY"]["value"]
                job_title_xpath = f"//li[@data-id='{offer_dict['id']}']" + self.CONSTANTS["OFFER_JOB_TITLE"]["value"]

                ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
                offer_element = WebDriverWait(self.driver, 10,ignored_exceptions=ignored_exceptions).until(expected_conditions.visibility_of_element_located((By.XPATH,offer_xpath)
                                                                                                                                        ))

                
                webdriver.ActionChains(self.driver).move_to_element(offer_element).click(offer_element ).perform()
                webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

            
                offer_dict["location"] = self.find_element_try(by=By.XPATH,value=location_xpath)
                offer_dict["age"] = self.find_element_try(by=By.XPATH,value=age_xpath)

        
                offer_dict["salary_range_provenance"] = self.find_element_try(by=By.XPATH,value=salary_range_provenance_xpath)
                

                offer_dict["job_title"] = self.find_element_try(**self.CONSTANTS["OFFER_JOB_TITLE"])
                #takes too much time
                offer_dict["company_rating"] = self.find_element_try(**self.CONSTANTS['COMPANY_RATING'])
                #takes too much time
                offer_dict["company_info"] = self.find_element_try(**self.CONSTANTS["COMPANY_INFO"])
                offer_dict["is_easy_apply"] = self.find_element_try(**self.CONSTANTS["OFFER_IS_EASY_APPLY"])
                offer_dict["text"] = self.find_element_try(**self.CONSTANTS["OFFER_TEXT"])
                offer_dict["company"] = self.find_element_try(**self.CONSTANTS["OFFER_COMPANY"])
                offer_dict["salary_range"] = self.find_element_try(by=By.XPATH,value=salary_range_xpath)

                for i in offer_dict:
                    if type(offer_dict[i])==uc.webelement.WebElement:
                        offer_dict[i] = offer_dict[i].text

                self.offers.append(offer_dict)

                if c % 5 == 0 :
                    schema = dict(
                        job_title=pl.Utf8(),
                        id=pl.Utf8(),
                        company=pl.Utf8(),
                        text=pl.Utf8(),
                        salary_range=pl.Utf8(),
                        location=pl.Utf8(),
                        age=pl.Utf8(),
                        company_rating=pl.Utf8(),
                        company_info=pl.Utf8(),
                        is_easy_apply=pl.Utf8(),
                        salary_range_provenance=pl.Utf8()

                    )
                    self.save_offers(self.offers,schema=schema)


          

class LinkedinBot(Bot):
    """
    Description:
    This class is a bot that will scrap the glassdoor website and save the data in parquet forma
    """
    
    def __init__(self,
                 *args,
                 **kwargs
                 ) -> None:
        """
        Description:
        This method is the constructor of the class
        Parameters:
        job_title: str
        This parameter is the job title that will be searched
        """
        super().__init__("linkedin", 
                          *args,
                        **kwargs)
        
    def get_offers_off_page_linkedin(self):
       


        """
        Description:
        This method will get the offers on the page and return a list of offers"""
        
        # self.wait.until(EC.visibility_of_all_elements_located(self.CONSTANTS["LIST_PAGE_OFFERS"]))
        offers= self.wait.until(EC.visibility_of_all_elements_located(self.CONSTANTS["LIST_PAGE_OFFERS"]))
        offer_list = []
        for offer in offers:
            ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
            o = WebDriverWait(self.driver, 10,ignored_exceptions=ignored_exceptions).until(expected_conditions.visibility_of(offer
                                                                                                                                           ))

    
            offer_list.append(o)

        return offer_list
        

    def run(self):
        self.search_job()
        schema = dict(
                        job_title=pl.Utf8(),
                        id=pl.Utf8(),
                        company=pl.Utf8(),
                        location=pl.Utf8(),
                        age=pl.Utf8(),
                        date=pl.Utf8(),
                        date_parsed=pl.Float64(),
                        benefits=pl.Utf8(),
                        text=pl.Utf8(),
                        candidates=pl.Utf8(),
                    )
        while True:

            
            if not self.find_element_try(by=By.CLASS_NAME,value="infinite-scroller__show-more-button"):
                # Comment: if there is no more offers to load, stop
                break

            result_list = self.get_offers_off_page_linkedin()
            
            ids_to_pass = pl.read_parquet('linkedin_data/linkedin*.parquet').select("id").unique().to_series().to_list()
            
            result_list_filtered = list(filter(
                lambda x: x.get_attribute("data-entity-urn") not in ids_to_pass,result_list
            ))

            if not result_list_filtered :

                webdriver.ActionChains(self.driver).move_to_element(result_list[-1]).scroll_to_element(result_list[-1]).scroll_by_amount(delta_x=0,delta_y=100).perform()
                next_button =   self.find_element_try(by=By.CLASS_NAME,value="infinite-scroller__show-more-button")
                time.sleep(2)

                if next_button:
                    try:
                        webdriver.ActionChains(self.driver).move_to_element(next_button).click(next_button).perform()
                    except  ElementNotInteractableException as e:
                        continue
                


                continue
            
            
            for offer in result_list_filtered:
                offer_dict = {}
                offer_dict["job_title"] = offer.find_element(**self.CONSTANTS["OFFER_JOB_TITLE"]).text
                offer_dict["id"] = offer.get_attribute("data-entity-urn")
                offer_dict["company"] = offer.find_element(**self.CONSTANTS["OFFER_COMPANY"]).text
                offer_dict["location"] = offer.find_element(**self.CONSTANTS["OFFER_LOCATION"]).text


                offer_dict["age"] = self.find_element_try(offer,**self.CONSTANTS["OFFER_AGE"])
                if not offer_dict["age"]:
                    offer_dict["age"] = self.find_element_try(offer,**self.CONSTANTS["OFFER_AGE_NEW"])
                
                if offer_dict["age"]:
                    offer_dict["age"],offer_dict["date"]= offer_dict["age"].text,offer_dict["age"].get_attribute("datetime")
                
                offer_dict["date_parsed"] = time.time()


                offer_dict["benefits"] = self.find_element_try(offer,**self.CONSTANTS["OFFER_BENEFITS"])
                if offer_dict["benefits"]:
                    offer_dict["benefits"]= offer_dict["benefits"].text
                
                webdriver.ActionChains(self.driver).move_to_element(offer).click(offer).perform()
                time.sleep(2)
                offer_dict["text"] = self.driver.find_element(*self.CONSTANTS["OFFER_TEXT"]).text
                offer_dict["candidates"] = self.driver.find_element(**self.CONSTANTS["OFFER_CANDIDATES"]).text
                self.offers.append(offer_dict)
            
                
                print(offer_dict)
                # s
                # self.save_offers(self.offers,schema=schema)
                # page = None
            
            self.save_offers(self.offers,schema=schema)
            

        print("Done")
        time.sleep(60)
        self.driver.quit()