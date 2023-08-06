import datetime
import re
from influxdb import InfluxDBClient
from influxdb.resultset import ResultSet
from tlmr6400stats import Session


class InfluxLogger(object):
    def __init__(self, session, influx, site, measurement='tlmr6400stats'):
        """
        :param Session session:
        :param InfluxDBClient influx:
        :param str site:
        """
        self.session = session
        self.influx = influx  # assume database already set
        self.site = site
        self.measurement = measurement

    def log_states(self):
        state = self.session.get_status()
        points = []
        try:
            prev_qry = 'SELECT * FROM {}_history where imei = \'{}\' GROUP BY * ORDER BY DESC LIMIT 1'
            prev = self.influx.query(prev_qry.format(self.measurement, state['imei']))
            prev_points = list(prev.get_points())
            if prev_points:
                pp = next(iter(prev_points))
                if 'imsi' not in pp:
                    pp['imsi'] = pp['network'] = 'unknown'
                pp.update(next(iter(prev.raw['series']))['tags'])
                if pp['imsi'] != state['imsi']:
                    p_dt = datetime.datetime.strptime(re.sub(r'\.\d+','', pp['time']), "%Y-%m-%dT%H:%M:%SZ")
                    diff = datetime.datetime.utcnow()-p_dt
                    dur_txt = '{} days, {} hours'.format(diff.days, int(diff.seconds/3600))
                    points.append({
                        'measurement': '{}_history'.format(self.measurement),
                        'tags': {'site': self.site, 'imei': state['imei']},
                        'fields': {
                            'imsi': state['imsi'],
                            'sim_change': '{}->{} ({}->{})'.format(
                                pp['network'], state['network'], pp['imsi'], state['imsi']
                            ),
                            'duration': dur_txt
                        }
                    })
            else:
                # we need to logg first record here..
                points.append({
                    'measurement': '{}_history'.format(self.measurement),
                    'tags': {'site': self.site, 'imei': state['imei']},
                    'fields': {
                        'imsi': state['imsi'],
                        'sim_change': 'First record {}({})'.format(state['network'], state['imsi']),
                        'dur_txt': 'N/A'
                    }
                })
        except Exception as e:
            print(e)
        points.append({
            'measurement': self.measurement,
            'tags': {
                'site': self.site,
                'imei': state['imei'],
                'imsi': state['imsi']
            },
            #  'time': '2020-03-25T18:00:00Z',
            'fields': {k: v for k, v in state.items() if k not in ['imei', 'imsi']}
        })
        self.influx.write_points(points)
        return state


