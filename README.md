# Vacancies/Keywords DataSet generator from HH.ru

Collection of simple scripts for crawling vacancies from HH.ru site
via API for generating CSV file by fields data like: name,
description and key skills.

It helps to generate CSV file with following format:
```csv
"$name1 & $description1","key skills1"
"$name2 & $description2","key skills2"
"$name3 & $description3","key skills3"
...
```

Scripts tested on python 3.10 but should work on previous versions too.

## How to use

Clone this repo.

Install all requirements:

```shell
pip install -r requirements.txt
```

### Get pages

Change `text` field in `download.py` to yours:

```python
text = 'NAME:Data science'
```

Then run script

```shell
python3 download.py
```

This script will download save results from API to `./docs/pagination`
folder in JSON format.

### Get details about vacancies

On the next step we need to download extended details about vacancies:

```shell
python3 parse.py
```

Script will call API and save responses to `./docs/vacancies` folder.

### Generate CSV

```shell
python3 generate.py
```

Result will be saved to `./docs/csv` folder.

## Links

* https://office-menu.ru/python/96-api-hh
* https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
* https://pythonspot.com/files-spreadsheets-csv/
