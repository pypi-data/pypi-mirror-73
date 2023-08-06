import requests
import hashlib
import base64
import urllib.parse
import re
import time


class Session(object):

    def __init__(self, target, username, password):
        """
        :param str target:
        :param str username:
        :param str password:
        """
        self.target = target
        self.s = requests.Session()
        password = hashlib.md5(password.encode()).hexdigest()  # b85b8105529de4cfc09286d8f24b32b8
        seed = '{}:{}'.format(username, password)
        auth = 'Basic ' + str(base64.b64encode(seed.encode('utf-8')), 'utf-8')
        self.s.cookies.set('Authorization', urllib.parse.quote(auth))
        self.s.headers.update({'referer': 'http://{}/'.format(target)})
        r = self.s.get("http://{}/userRpm/LoginRpm.htm?Save=Save".format(target))
        try:
            self.token = re.match(r'.*\/(.*)\/userRpm\/Index.htm.*', r.text).group(1)
        except AttributeError as ae:
            time.sleep(1)
            r = self.s.get("http://{}/userRpm/LoginRpm.htm?Save=Save".format(target))
            self.token = re.match(r'.*\/(.*)\/userRpm\/Index.htm.*', r.text).group(1)

    def get_url(self, path):
        """
        :param str path:
        :rtype: requests.Response
        """
        return self.s.get('http://{}/{}/userRpm/{}'.format(self.target, self.token, path))

    def post_url(self, path, data=None, json=None):
        """
        :param str path:
        :param str data:
        :param object json:
        :rtype: requests.Response
        """
        return self.s.post('http://{}/{}/userRpm/{}'.format(self.target, self.token, path), data=data, json=json)

    def get_status(self):
        status = self.post_url('lteWebCfg', json={'module': 'status', 'action': 0}).json()
        return {'imei': str(status['deviceInfo']['imei']),
                'imsi': str(status['deviceInfo']['imsi']),
                'model': str(status['deviceInfo']['model']),
                'network': status['wan']['operatorName'],
                'signal': int(status['wan']['signalStrength']),
                'rxSpeed': int(status['wan']['rxSpeed']),
                'txSpeed': int(status['wan']['txSpeed'])}
