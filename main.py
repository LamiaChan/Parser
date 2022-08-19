import pathlib
from src.Base import Cache
from src.ReadManga import RMParser
from selenium import webdriver
from flask import Flask, request

cache_path = pathlib.Path.home().joinpath('.lamia_chan/cache')
app = Flask(__name__)

@app.route('/readmanga')
def index():
    manga_url = str(request.args.get('manga_url'))
    login = str(request.args.get('login'))
    password = str(request.args.get('password'))
    cache_force = bool(request.args.get('force'))

    if cache_force:
        Cache.clear_cache(cache_path, manga_url)

    if not Cache.check_parsed(cache_path, manga_url):
        Cache.create_dir(cache_path, manga_url)
        base_dir = Cache.get_dir(cache_path, manga_url)
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

        Cache.save_manifest(base_dir, rm.to_json())
    return Cache.get_manifest(Cache.get_dir(cache_path, manga_url))
