import pathlib
from src.Base import Cache
from src.ReadManga import RMParser
from selenium import webdriver
from flask import Flask

cache_path = pathlib.Path.home().joinpath('.lamia_chan/cache')
app = Flask(__name__)

@app.route('/readmanga/<string:manga_url>/<string:login>/<string:password>')
def index(manga_url: str, login: str, password: str):
    if not Cache.check_parsed(cache_path, manga_url):
        
        base_dir = Cache.create_dir(cache_path, manga_url)
        base_dir_img = Cache.create_img_dir(cache_path, manga_url)

        rm = RMParser(
            'https://readmanga.live/', 
            f'https://readmanga.live/{manga_url}/', 
            login, 
            password, 
            webdriver.Firefox()
        )

        rm.open_page(rm.site_url)
        rm.login_page()
        
        rm.open_page(rm.manga_url)
        rm.parse_manga_data()
        rm.parse_volumes()
        rm.driver.quit()

        rm.load_imgs(base_dir_img)

        Cache.save_manifest(cache_path, rm.to_json())
    return ''
