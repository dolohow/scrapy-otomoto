scrapy-otomoto
==============

This program allows you to fetch all cars from otomoto.pl


## Installation
```
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Usage
```
scrapy crawl -L WARNING otomoto -o otomoto.json
```

This will generate `otomoto.json` file with all cars that are currently
available.  You can further investigate them or create some analysis.


For some interesting applications check out this:
http://prokulski.net/index.php/2018/01/23/sprzedam-opla/


## Post scriptum
This suppose to be analysis repository for buying used car, but I found one
quickly, so...  Maybe some day.
