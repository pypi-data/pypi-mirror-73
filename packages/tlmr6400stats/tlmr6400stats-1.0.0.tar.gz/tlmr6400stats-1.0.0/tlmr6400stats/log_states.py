from influxdb import InfluxDBClient
from tlmr6400stats import Session, InfluxLogger

s = Session('192.168.1.1', 'admin', 'detsortehus')
i = InfluxDBClient('192.168.1.10', database='telegraf')
il = InfluxLogger(s, i, site='nordsøvej51')
il.log_states()