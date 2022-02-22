#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

class RequestsClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def set_token(self, token):
        self.token = token

    def set_username(self, username):
        self.username = username

    def build_url(self, path):
        return self.base_url + path

    def headers(self):
        if self.token:
            return {
                'Authorization': 'Bearer ' + self.token
            }
        return {}

    def get(self, path):
        return requests.get(self.build_url(path), headers=self.headers())

    def post(self, path, body):
        return requests.post(self.build_url(path), json=body, headers=self.headers())

    def put(self, path, body):
        return requests.put(self.build_url(path), json=body, headers=self.headers())

    def delete(self, path):
        return requests.delete(self.build_url(path), headers=self.headers())

    def upload_post(self, path, data):
        return requests.post(self.build_url(path), files=data, headers=self.headers())
