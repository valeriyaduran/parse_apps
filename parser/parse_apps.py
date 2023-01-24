from loguru import logger
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from db.db_scripts_service import DBScriptsService
from html_page.add_business_apps_to_html import HTMLHelper
from setup_browser_service import SetupBrowser


class ParseApps:
    @staticmethod
    def get_all_apps(wd):
        business_apps = []
        is_last_page = False
        while len(business_apps) < 200 and not is_last_page:
            current_items = [web_element.get_attribute("href") for web_element in
                             wd.find_elements(By.XPATH, '//div[@id="all-list-container"]//a')]
            if len(current_items) == 0:
                is_last_page = True
            if len(current_items) >= 200:
                business_apps = current_items[:200]
            else:
                business_apps = current_items
            wd.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        return business_apps

    @staticmethod
    def get_all_fields(wd, business_apps):
        data = []
        counter = 1
        for i in range(len(business_apps)):
            wd.get(f"{business_apps[i]}")
            business_app_name = ParseApps.get_business_app_name(wd)
            company_name = ParseApps.get_company_name(wd, business_app_name)
            release_year = ParseApps.get_release_year(wd, company_name)
            email = ParseApps.get_email(wd, company_name)
            data.append({"business_app_name": business_app_name,
                         "company_name": company_name,
                         "release_year": release_year,
                         "email": email})
            logger.info(f"Info has been written to data list for {company_name}, app number {counter}")
            counter += 1
            wd.execute_script("window.history.go(-1)")
            wd.implicitly_wait(3)
        DBScriptsService().insert_data_into_table(data)
        HTMLHelper.save_data_to_rows(data)
        return data

    @staticmethod
    def get_business_app_name(wd):
        business_app_name = ""
        app_not_ready = True
        while app_not_ready:
            try:
                business_app_name = WebDriverWait(wd, 10).until(expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, "#main h1"))).text
                app_not_ready = False
            except TimeoutException:
                logger.info("Timeout exception")
                wd.implicitly_wait(10)
                wd.refresh()
            except NoSuchElementException:
                logger.info("No business_app_name")
                return business_app_name
        return business_app_name

    @staticmethod
    def get_company_name(wd, business_app_name):
        company_name = ''
        try:
            company_name = WebDriverWait(wd, 10).until(expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, "#main h1 + a"))).text
        except NoSuchElementException:
            logger.info(f"No company_name for {business_app_name}")
            return company_name
        return company_name

    @staticmethod
    def get_release_year(wd, company_name):
        release_year = ""
        year_not_ready = True
        while year_not_ready:
            try:
                release_year = wd.find_element(By.XPATH,
                                               '//h6[@id="versionHeader_desktop"]/parent::div//div/*[1]').get_attribute(
                    'innerHTML')[-4:]
                year_not_ready = False
            except StaleElementReferenceException:
                logger.info("Page for getting year has been refreshed")
                wd.refresh()
            except NoSuchElementException:
                logger.info(f"No release_year for  {company_name}")
                return release_year
        return release_year

    @staticmethod
    def get_email(wd, company_name):
        email = ""
        contact_info_not_ready = True
        while contact_info_not_ready:
            try:
                contact_info_button = wd.find_element(By.ID, "contactInfoButton_desktop")
                contact_info_button.click()
                contact_info_not_ready = False
                try:
                    wd.find_element(By.XPATH, '//div[@role="dialog"]//h6[contains(text(), "Email")]')
                    email = wd.find_element(By.XPATH, '//div[@role="dialog"]//a').text
                except NoSuchElementException:
                    logger.info(f"No email for  {company_name}")
                    contact_info_not_ready = False
                close_button = wd.find_element(By.ID, "closeButton")
                close_button.click()
            except NoSuchElementException:
                contact_info_not_ready = False
                logger.info(f"No contact information for {company_name}")
            except StaleElementReferenceException:
                wd.refresh()
                logger.info("Page for getting contact info has been refreshed")
        return email


if __name__ == "__main__":
    service = SetupBrowser()
    service.start_page()
    business_apps = ParseApps.get_all_apps(service.wd)
    ParseApps.get_all_fields(service.wd, business_apps)
    service.quit()
