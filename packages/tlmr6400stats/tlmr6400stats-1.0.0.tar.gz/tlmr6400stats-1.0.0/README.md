# tlmr6400stats
Tool to read stats from TL-MR6400 LTE router and push these to influxdb

## Requirements.

Python 3.6+

## Installation & Usage
### pip install


```sh
pip install tlmr6400stats
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com//.git`)

Then import the package:
```python
import tlmr6400stats
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
from tlmr6400stats import InfluxRSync
```

## Getting Started
Install and then run the following:

```python
from influxdb import InfluxDBClient
from tlmr6400stats import Session, InfluxLogger

s = Session('192.168.1.1', 'admin', 'admin')
print(s.get_status())
i = InfluxDBClient('192.168.1.10', database='tlmr6400stats')
il = InfluxLogger(s, i, site='home')
il.log_states()  # logs stats to the influxdb
```
would produce:
{'imei': 'xxxxxx', 'imsi': 'yyyyy', 'model': 'MR6400(EU) 2.0', 'network': 'ATT', 'signal': 4, 'rxSpeed': 167, 'txSpeed': 196}
```
> select * from tlmr6400stats
name: tlmr6400stats
time			imei		imsi		model		network	rxSpeed	signal	site		txSpeed
----			----		----		-----		-------	-------	------	----		-------
1585159200000000000	xxxx	yyyyyy	MR6400(EU) 2.0	ATT	8234	4	home	7900
1585731248806189544	xxxx	yyyyyy	MR6400(EU) 2.0	ATT	13990	4	home	3771

```


## Author

ssch@wheel.dk

