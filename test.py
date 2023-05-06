"""
Write some basic tests for the project.
"""
import pytest
from bot.core import Bot
from bot.constants import IMPLEMENTED
from bot.core   import GlassdoorBot,IndeedBot
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementNotSelectableException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoSuchAttributeException
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.common.exceptions import InvalidCookieDomainException
from selenium.common.exceptions import UnableToSetCookieException
from selenium.common.exceptions import UnexpectedTagNameException
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import ImeNotAvailableException



def test_bot():
    """
    Description:
    """
    bot = Bot("indeed")
    assert bot.job_title == "Data Scientist"
    assert bot.search_location == "Paris"
    assert bot.website == "indeed"
    assert bot.driver is not None
    assert bot.CONSTANTS == IMPLEMENTED["indeed"]
    
    bot.driver.quit()

def test_bot_not_implemented():
    """
    Description:
    """
    with pytest.raises(NotImplementedError):
        bot = Bot("not_implemented")
        bot.driver.quit()

def test_bot_glassdoor_search():
    """
    Description:
    """
    bot = GlassdoorBot("Data Engineer","Paris")
    bot.search_job()
    assert bot.page == 1
    
    bot.driver.quit()