
# Web Scraper of COVID-19 data for Poland

Python package [covid19poland](https://pypi.org/project/covid19poland/) provides access to COVID-19 data of Poland.

The data is scraped from Wikipedia.

## Setup and usage

Install from [pip](https://pypi.org/project/covid19poland/) with

```python
pip install covid19poland
```

Importing main `fetch()` function with 

```python
import covid19poland as PL

x = PL.fetch()
```

Package is regularly updated. Update with

```bash
pip install --upgrade covid19poland
```

## Parametrization

### Level

Level is a setting for granularity of data

1. Country level (default)
2. State level

```python
import covid19poland as PL

# country level
x1 = PL.fetch(level = 1)
# state level
x2 = PL.fetch(level = 2)
```

## Offline

The package contains manually checked dataset from Twitter.
It can be read and parsed from json to pandas dataframe using `offline` submodule. 

```python
import covid19poland as PL

# parse offline
x = PL.offline.read()
```

## Contribution

Developed by [Martin Benes](https://github.com/martinbenes1996).

Join on [GitHub](https://github.com/martinbenes1996/covid19poland).



