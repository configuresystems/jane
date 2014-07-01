import requests
import json


class Internal():
    def __init__(self):
        pass

    def post(self, endpoint, dictionary):
        url = "http://23.253.96.98:80/api/{0}".format(endpoint)
        headers = {'Content-type': 'application/json'}
        req = requests.post(
                url,
                data=json.dumps(dictionary),
                headers=headers
                ).json()
        return req

    def get(self, endpoint, field):
        url = "http://23.253.96.98:80/api/{0}/{1}".format(
                endpoint,
                field
                )
        print url
        headers = {'Content-type': 'application/json'}
        req = requests.get(
                url,
                headers=headers
                ).json()
        return req

    def get_all(self, endpoint):
        url = "http://23.253.96.98:80/api/{0}".format(endpoint)
        headers = {'Content-type': 'application/json'}
        req = requests.get(
                url,
                headers=headers
                ).json()
        return req
