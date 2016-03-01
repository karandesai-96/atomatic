# Atomatic

[![Travis CI](https://travis-ci.org/karandesai-96/atomatic.png?branch=develop)](https://travis-ci.org/karandesai-96/atomatic)
[![Coverage Status](https://coveralls.io/repos/github/karandesai-96/atomatic/badge.svg?branch=develop)](https://coveralls.io/github/karandesai-96/atomatic?branch=develop)

Atomatic fetches all the data available on the [NIST Physical Measurements website](http://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=&all=all&ascii=html), about the Atomic Weights and Isotopic composition, parses the data, and generates a CSV file as an output.

### Requirements:
* [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/) ( >= 4.4.0)
* [Requests](http://docs.python-requests.org/en/master/) ( >= 2.9.0)
* [Pandas](http://pandas.pydata.org/) ( >= 0.17.0)
* [SQLAlchemy](http://www.sqlalchemy.org/) ( >= 1.0)

### Usage:
* Clone this repo :
```
git clone https://www.github.com/karandesai-96/atomatic
```

* Update proper database credentials to `tests/db_credentials.json`

* Simply execute this while being in top-level directory. Upon completion, check for output csv file under `bin` directory.

```
python atomatic.py
```

* For running tests, execute in the terminal : 
```
nosetests
```

