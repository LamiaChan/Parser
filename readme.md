# LamiaChan Parser
Manga parsers for lamia chan ecosystem

## Installation
- [install selenium web driver](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/)
- create python venv
```
pip install -r requirements.txt
```

## Run 
```
flask --app main run
```

### Example
```
http://127.0.0.1:5000/readmanga?manga_url=manga_name_url&login=login&password=pass&force=0
```

## Supported sites
| Site | Is supported |
| ------ | ------ |
| grouple.co | yes |
| mangalib.me | no |
| manga-chan.me | no |

### TODO:
- need to parse authors
- automation load download manga to db
- create watchers
- tests
