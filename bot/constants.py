from selenium.webdriver.common.by import By

IMPLEMENTED = {
            'indeed':{
                    "START_URL":"https://www.indeed.com/",
                    "SEARCH_BAR":dict(
                        by=By.ID,
                        value="text-input-what"
                    ),
                    "SEARCH_LOCATION":dict(
                        by=By.ID,
                        value = "text-input-where"
                    ),
                    "SEARCH_BUTTON":dict(
                        by=By.CLASS_NAME,
                        value="yosegi-InlineWhatWhere-primaryButton"
                    ),
                    "NEXT_PAGE":dict(
                        by=By.XPATH,
                        value='//a[@aria-label="Next Page"]'
                    ),
                    "DATA_PATH" : "indeed_data",
                    "LIST_PAGE_OFFERS":(
                        By.CLASS_NAME,
                        "tapItem"
                    ),
                    "OFFER_ID":dict(
                        by=By.XPATH,
                        value="//h2[contains(@class, 'jobTitle')]/a"
                    ),
                    "OFFER_TITLE":dict(
                        by=By.CLASS_NAME,
                        value="jobTitle"
                    ),
                    "OFFER_COMPANY":dict(
                        by=By.CLASS_NAME,
                        value="companyName"
                    ),
                    "OFFER_TEXT":(
                        By.ID,
                        "jobDescriptionText"
                    ),
                    "OFFER_SALARY":dict(
                        by=By.XPATH,
                        value="//div[contains(@class, 'salary-snippet-container')]/div"
                    )
                      },
            "glassdoor":{
                    "START_URL":"https://www.glassdoor.com/Emploi",
                    "SEARCH_BAR":dict(
                        by=By.ID,
                        value="sc.keyword"
                    ),
                    "SEARCH_LOCATION":dict(
                        by=By.ID,
                        value = "sc.location"
                    ),
                    "SEARCH_BUTTON":dict(
                        by=By.XPATH,
                        value='//button[@data-test="search-bar-submit"]'
                    ),
                
                    "NEXT_PAGE":dict(
                        by=By.XPATH,
                        value='//button[@aria-label="Next"]'
                    ),
                    "DATA_PATH" : "glassdoor_data",
                    "LIST_PAGE_OFFERS":(
                        By.XPATH,
                        "//li[contains(@class, 'react-job-listing')]"
                      
                    ),
                    "OFFER_TITLE":dict(
                        by=By.CLASS_NAME,
                        value="jobLink"
                    ),
                    "OFFER_JOB_TITLE":dict(
                        by=By.XPATH,
                      value="//div[@data-test='jobTitle']"
                    ),
                    "OFFER_COMPANY":dict(
                        by=By.XPATH,
                        value='//div[@data-test="employerName"]'
                    ),
                    "OFFER_TEXT":(
                        By.ID,
                        "JobDescriptionContainer"
                    ),
                    "OFFER_SALARY":dict(
                        by=By.XPATH,
                        value='//span[@data-test="detailSalary"]'
                    ),
                    "OFFER_SALARY_PROVENANCE":dict(
                        by=By.XPATH,
                        value="//span[@data-test='detailSalary']/span[contains(@class,'css-0')]"
                    ),
                 
                    "OFFER_LOCATION":dict(
                        by=By.XPATH,
                        value="//span[@data-test='emp-location']"
                    ),
                    "OFFER_AGE":dict(
                        by=By.XPATH,
                        value="//div[@data-test='job-age']"
                    ),
                    "COMPANY_INFO":dict(
                        by=By.ID,
                        value="EmpBasicInfo"
                    ),
                    "COMPANY_RATING":dict(
                        by=By.XPATH,
                        value="//div[@data-test='company-ratings']"
                    ),
                    "OFFER_IS_EASY_APPLY":dict(
                        by=By.XPATH,
                        value="//button[@data-test='applyButton']"
                    ),
            },
              "linkedin":{
                    "START_URL":"https://fr.linkedin.com/jobs/search",
                    "SEARCH_BAR":dict(
                        by=By.ID,
                        value="job-search-bar-keywords"
                    ),
                    "SEARCH_LOCATION":dict(
                        by=By.ID,
                        value = "job-search-bar-location"
                    ),
                    "SEARCH_BUTTON":dict(
                        by=By.CLASS_NAME,
                        value='base-search-bar__submit-btn'
                    ),
                
                    
                    "DATA_PATH" : "linkedin_data",
                    "LIST_PAGE_OFFERS":(
                        By.CLASS_NAME,
                        "base-search-card--link"
                      
                    ),
                    "OFFER_ID":dict(
                        by=By.CLASS_NAME,
                        value="base-search-card--link"
                    ),
                   
                    "OFFER_JOB_TITLE":dict(
                        by=By.CLASS_NAME,
                      value="base-search-card__title"
                    ),
                    "OFFER_COMPANY":dict(
                        by=By.CLASS_NAME,
                        value='base-search-card__subtitle'
                    ),
                    "OFFER_TEXT":(
                        By.CLASS_NAME,
                        "show-more-less-html__markup"
                    ),
                
                 
                    "OFFER_LOCATION":dict(
                        by=By.CLASS_NAME,
                        value="job-search-card__location"
                    ),
                    "OFFER_AGE":dict(
                        by=By.CLASS_NAME,
                        value="job-search-card__listdate"
                    ),
                    "OFFER_AGE_NEW":dict(
                        by=By.CLASS_NAME,
                        value="job-search-card__listdate--new"
                    ),
                    "OFFER_CANDIDATES":dict(
                        by=By.CLASS_NAME,
                        value="num-applicants__caption"
                    ),
                    "OFFER_BENEFITS":dict(
                        by=By.CLASS_NAME,
                        value="result-benefits__text"
                    ),
                  
            }
                       }