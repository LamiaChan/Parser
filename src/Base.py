from pathlib import Path
import json, dataclasses, urllib.request, os
from dataclasses import dataclass, field
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

@dataclass
class MangaImgUrl:
    """
    Struct representing a manga img data
    """
    volume_url: str = field(default_factory=str)
    imgs_urls: list[str] = field(default_factory=list[str])
    imgs_paths: list[str] = field(default_factory=list[str])


@dataclass
class MangaData:
    """
    Struct representing a manga data
    """
    names: list[str] = field(default_factory=list[str])
    product_type: str = field(default_factory=str)
    year_publish: int = field(default_factory=int)
    product_status: str = field(default_factory=str)
    translate_status: str = field(default_factory=str)
    author: list[str] = field(default_factory=list[str])
    artist: list[str] = field(default_factory=list[str])
    publisher: list[str] = field(default_factory=list[str])
    age_rating: str = field(default_factory=str)
    volumes_count: int = field(default_factory=int)
    tags: list[str] = field(default_factory=list[str])
    manga_imgs_urls: list[MangaImgUrl] = field(default_factory=list[MangaImgUrl])

class Cache:
    @classmethod
    def check_parsed(cls, cache_path: str, manga_name: str) -> bool:
        return os.path.exists(Path.joinpath(cache_path, manga_name)) 
    
    @classmethod
    def create_dir(cls, cache_path: str, manga_name: str) -> Path:
        Path(f'{cache_path}/{manga_name}').mkdir(parents=True, exist_ok=True)
        return Path(f'{cache_path}/{manga_name}')

    @classmethod
    def create_img_dir(cls, cache_path: str, manga_name: str) -> Path:
        Path(f'{cache_path}/{manga_name}/img').mkdir(parents=True, exist_ok=True)
        return Path(f'{cache_path}/{manga_name}/img')
    
    @classmethod
    def save_manifest(cls, path: str, manifest: json):
        with open(f'{path}/data.json', 'w') as f:
            f.write(manifest)

class BaseParser:
    """
    Class representing Base Parser for manga
    """
    def __init__(self, site_url: str, manga_url: str, driver = webdriver.Firefox()) -> None:
        self.site_url = site_url
        self.manga_url = manga_url
        self.manga_data = MangaData()
        self.driver = driver

    def open_page(self, url):
        """
        Method opening page
        """
        self.driver.get(url)
    
    def find(self, selector: str, find_one: bool = True, selenium_selector = By.CSS_SELECTOR):
        """
        Method selenium find implementation
        """
        res = lambda x: self.driver.find_element(selenium_selector, selector) if x else self.driver.find_elements(By.CSS_SELECTOR, selector)
        return res(find_one)
    
    def to_json(self):
        """
        Method to convert manga_data to json string
        """
        return json.dumps(self.manga_data, cls=EnhancedJSONEncoder)

    def parse_manga_data(self) -> None:
        """
        Method for parsing title data
        """
        pass

    def parse_volumes(self) -> None:
        """
        Method for parsing volumes with imgs
        """
        pass
    
    #todo: починитьт это я пытался прилепить path из cache class'a но я сейчас слишком пьян для этого !
    def load_imgs(self, path: str) -> None:
        """
        Method for loading imgs from url
        """
        for vol_inx, url in enumerate(self.manga_data.manga_imgs_urls):
            for page_inx, img_url in enumerate(url.imgs_urls):
                print(path.joinpath(str(vol_inx)))
                # path.joinpath(vol_inx).mkdir(parents=True, exist_ok=True)
                # urllib.request.urlretrieve(img_url, f'{path}/{vol_inx}/{page_inx}.png')
                # self.manga_data.manga_imgs_urls[vol_inx].imgs_paths.append(os.path.abspath(path.joinpath(f'{vol_inx}/{page_inx}.png')))
