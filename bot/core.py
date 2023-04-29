from uuid import uuid4
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import polars as pl
from core.constants import IMPLEMENTED

class UcChromeDriver(uc.Chrome):
    """"
    Description:
    This class is a wrapper for the undetected_chromedriver package but with basic options

    """

    def __init__(self)->None:
       

        options = webdriver.ChromeOptions()

        options.add_argument('--log-level=3')
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
        
        self.CONSTANTS = IMPLEMENTED[website]
        self.wait = WebDriverWait(self.driver, 10)

    def find_element_try(self,*args,**kwargs):
        """
        Description:
        This method will try to find an element and return None if it fails"""
        try:
           return self.driver.find_element(*args,**kwargs)
        except:
            return None
    def next_page(self):
        """
        Description:
        This method will find the next page button"""
        self.page = self.find_element_try(**self.CONSTANTS["NEXT_PAGE"])

    def save_offers(self,offers):
        """"
        Description:
        This method will save the offers in parquet format"""
        if offers:
            if offers[0]["job_title"]:
                try:
                    pl.DataFrame(
                        offers
                    ).write_parquet(f"{self.CONSTANTS['DATA_PATH']}/{self.website}_{uuid4()}.parquet")
                except Exception as e:
                    print(offers)
                    print(e)

    def get_offers_off_page(self):
        """
        Description:
        This method will get the offers on the page and return a list of offers"""

        return self.driver.find_elements(**self.CONSTANTS["LIST_PAGE_OFFERS"])
    def search_job(self):
        """
        
        Description:
        This method will search the job title in the search bar and click on the search button"""
 
        self.driver.get(self.CONSTANTS["START_URL"])
        
        self.driver.implicitly_wait(2)


        self.driver.find_element(**self.CONSTANTS["SEARCH_BAR"]).send_keys(self.job_title)
        self.driver.find_element(**self.CONSTANTS["SEARCH_LOCATION"]).send_keys(self.search_location)
        
        self.driver.find_element(**self.CONSTANTS["SEARCH_BUTTON"]).click()

        self.driver.implicitly_wait(2)

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
        
        


    
    
    def go_trough_offers(self,result_list):
        """
        Description:
        This method will go trough the offers and save the data in a list of dict"""

        for offer in result_list:

                offer_dict= dict()
                for i in ("job_title","id","company","text","salary_range"):
                    offer_dict[i]=None
                
                list_fetch_ids = pl.scan_parquet(f'{self.CONSTANTS["DATA_PATH"]}/*.parquet').filter(pl.col("text").is_not_null()).select(pl.col("id").unique()).collect().to_series() 
                try:
                    offer_dict["job_title"] = None
                    offer_dict['id'] = offer.find_element(**self.CONSTANTS["OFFER_ID"]).get_attribute('id')
                    if offer_dict['id']  not in list_fetch_ids:
                        
                        offer_dict["job_title"] =offer.find_element(**self.CONSTANTS["OFFER_TITLE"]).text
                        offer_dict["company"] = offer.find_element(**self.CONSTANTS["OFFER_COMPANY"]).text
                        self.wait.until(EC.visibility_of(offer))
                        offer.click()
                        text_offer =self.wait.until(EC.visibility_of_element_located(self.CONSTANTS["OFFER_TEXT"]))
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
        self.search_job()
        
        
