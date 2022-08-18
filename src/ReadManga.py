from .Base import BaseParser, MangaImgUrl
from selenium.webdriver.common.by import By

class RMParser(BaseParser):
    def __init__(self, site_url: str, manga_url: str, login: str, password: str, driver):
        super().__init__(site_url, manga_url, driver)
        self.login = login
        self.password = password
    
    def parse_manga_data(self):
        #Это парсер, ничего не могу поделать ¯\_(ツ)_/¯
        try:
            self.manga_data.names.append(self.find('.name').text)
        except Exception:
            self.manga_data.names.append('None')

        try:
            self.manga_data.names.append(self.find('.eng-name').text)
        except Exception:
            self.manga_data.names.append('None')

        try:
            self.manga_data.names.append(self.find('.expandable-text').text)
        except Exception:
            self.manga_data.names.append('None')

        try:
            self.manga_data.product_type = self.find('.names').text.split()[0]
        except Exception:
            self.manga_data.product_type = 'None'

        try:
            self.manga_data.year_publish = int(self.find('.elem_year ').text)
        except Exception:
            self.manga_data.year_publish = 0

        try:
            self.manga_data.product_status = self.find("//b[text()='Томов:']/parent::*", True, By.XPATH).text.split(',')[1].strip()
        except Exception:
            self.manga_data.product_status = 'None'
            
        try:
            self.manga_data.translate_status = self.find("//b[text()='Перевод:']/parent::*", True, By.XPATH).text.split(':')[1].strip()
        except Exception:
            self.manga_data.translate_status = 'None'
        
        try:
            for author in self.find('.elem_author', False):
                self.manga_data.author.append(author.text)
                self.manga_data.artist = self.manga_data.author
        except Exception:
            self.manga_data.author = []
            self.manga_data.artist = self.manga_data.author

        try:
            self.manga_data.publisher = self.find("//span[text()='Издательства:']/parent::*", True, By.XPATH).text.split(':')[1].strip().split(',')
        except Exception:
            self.manga_data.publisher = []

        try:
            self.manga_data.age_rating = self.find("//span[text()='Возрастная рекомендация:']/parent::*", True, By.XPATH).text.split(':')[1].strip()
        except Exception:
            self.manga_data.age_rating = 'None'
        
        try:
            self.find('.open > span:nth-child(1)').click()
        except Exception:
            pass

        try:
            chapters = self.find(".item-title > a", False)
            for chapter in chapters:
                self.manga_data.manga_imgs_urls.append(MangaImgUrl(chapter.get_attribute('href')))
            self.manga_data.volumes_count = len(chapters)
            self.manga_data.manga_imgs_urls.reverse()
        except Exception:
            self.manga_data.manga_imgs_urls = []
            self.manga_data.volumes_count = 0
        
        try:
            genres = self.find("//span[text()='Жанры:']/parent::*", True, By.XPATH).text.split(':')[1].strip().split(',')
        except Exception:
            genres = []
        
        try:
            tags = self.find("//span[text()='Теги:']/parent::*", True, By.XPATH).text.split(':')[1].strip().split(',')
        except Exception:
            tags = []
 
        self.manga_data.tags = genres + tags
    
    def login_page(self):
        self.open_page(self.find('.login-link').get_attribute('href'))
        self.find('#username').send_keys(self.login)
        self.find('#password').send_keys(self.password)
        self.find('.btn').click()
    
    def parse_volumes(self):
        if (len(self.manga_data.manga_imgs_urls) > 0):
            for index, url in enumerate(self.manga_data.manga_imgs_urls):
                self.driver.get(url.volume_url)

                try:
                    self.find("//strong[text()='Внимание!']", True, By.XPATH)
                    self.find('a.btn').click()
                    self.find('div.form-group:nth-child(2) > div:nth-child(2) > div:nth-child(1) > label:nth-child(3)').click()
                    self.find('#\ ').click()
                    self.driver.get(url.volume_url)
                    print(1)
                except Exception:
                    pass   

                for page in range(0, int(self.find('.pages-count').text)):
                    img = self.find('#mangaPicture').get_attribute('src')
                    self.manga_data.manga_imgs_urls[index].imgs_urls.append(img)
                    self.find('div.reader-controller:nth-child(5) > div:nth-child(1) > div:nth-child(2) > button:nth-child(5)').click()
                
