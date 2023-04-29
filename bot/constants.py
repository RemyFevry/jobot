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
                    "LIST_PAGE_OFFERS":dict(
                        by=By.CLASS_NAME,
                        value="tapItem"
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
                    "SEARCH_BUTTON":dict(
                        by=By.CLASS_NAME,
                        value="gd-ui-button"
                    ),
                    "NEXT_PAGE":dict(
                        by=By.XPATH,
                        value='//a[@aria-label="Next"]'
                    ),
                    "DATA_PATH" : "glassdoor_data",
                    "LIST_PAGE_OFFERS":dict(
                        by=By.CLASS_NAME,
                        value="react-job-listing"
                    ),
                    "OFFER_TITLE":dict(
                        by=By.CLASS_NAME,
                        value="jobLink"
                    ),
                    "OFFER_COMPANY":dict(
                        by=By.XPATH,
                        value='//div[@data-test="EmployerName"]'
                    )
            }
                       }