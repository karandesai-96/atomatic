# Atomatic

Atomatic fetches all the data available on the [NIST Physical Measurements website](http://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=&all=all&ascii=html), about the Atomic Weights and Isotopic composition, parses the data, and generates a CSV file as an output.

### Requirements:
* [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/) ( >= 4.4.0)
* [Requests](http://docs.python-requests.org/en/master/) ( >= 2.9.0)
* [Pandas](http://pandas.pydata.org/) ( ( >= 0.17.0)

### Usage:
* Clone this repo :
```
git clone https://www.github.com/karandesai-96/atomatic
```

* Simply execute this while being in top-level directory. Upon completion, check for output csv file under **outdump** directory.

```
python atomatic.py
```

* For running tests, execute in the terminal : 
```
nosetests
```

