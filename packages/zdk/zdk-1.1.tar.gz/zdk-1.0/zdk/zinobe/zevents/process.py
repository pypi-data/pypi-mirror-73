import json
import requests
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectTimeout


class Process:

    def __init__(self):
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def call_zevents(self, **data):

        dict_data = data.copy()
        del (dict_data["service"])
        response = requests.post(
            url="{}{}".format(
                'https://zevent.sg-zinobe.com/api/v1/',
                data["service"]),
            headers=self.headers,
            json=dict_data)
        return json.loads(response.content)
