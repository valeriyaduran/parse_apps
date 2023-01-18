from selenium import webdriver


class SetupBrowser:
    def __init__(self):
        self.wd = webdriver.Chrome()
        self.wd.maximize_window()

    def start_page(self):
        self.wd.get('https://apps.microsoft.com/store/category/Business')

    def quit(self):
        self.wd.close()