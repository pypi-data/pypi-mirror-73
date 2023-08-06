import requests
from django.conf import settings
import os
import json


class TayLoggerAPIConsumer:


    def __init__(self, token):
        self.url = "http://tayloggerapi.herokuapp.com/"
        self.api_key = token

    def create_log_group(self, data):
        endpoint = self.url + "logger/group/create/"

        headers = {"Authorization": f"Token {self.api_key}"}
        name = data.get("name")[:29]

        if name:
            requests.post(url=endpoint, data={"name": name}, headers=headers)


    def create_log(self, data):
        token = self.api_key
        print(token)
        endpoint = self.url + "logger/log/create/"
        to_be_sent_data = {
            "group": data.get("group"),
            "message": data.get("message")
        }
        headers = {"Authorization": f"Token {token}"}
        requests.post(url=endpoint, data=to_be_sent_data, headers=headers)
