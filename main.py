#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from api import Api
from client import RequestsClient

class SampleData:

    def __init__(self, base_url):
        self.base_url = base_url

    def sync_sample_data(self):

        data = {}
        user_api_list = []
        for user in data['users']:
            client = Api(RequestsClient(self.base_url))
            user_api = self.create_user(client, user)
            user_api_list.append(user_api)

        relations = []

        for org in data['orgs']:
            owner = self.find_and_create_org(org, relations, user_api_list)
            self.org_add_other_user(owner, org)

    def create_user(self, client, user):
        user_api = client.get_user_api()
        user_api.register(user)
        return user_api

    def find_and_create_org(self, org, relations, user_api_list):
        for relation_user in relations:
            for user_org in relation_user['orgs']:
                if user_org['name'] == org['name'] and user_org['role'] == 'Admin':    
                    for user_api in user_api_list:
                        if user_api.username == relation_user['username']:
                            user_api.create_org(org)
                            break
                    return
    
    def org_add_other_user(self, org_api, org, relations):
        for relation_user in relations:
            for user_org in relation_user['orgs']:
                if user_org['name'] == org['name']:
                    org_api.add_member(relation_user['username'], user_org['role'])

    def find_and_create_user_app(self, app, relations, user_api_list):
        for relation_user in relations:
            for user_app in relation_user['apps']:
                if user_app['name'] == app['name'] and user_app['role'] == 'Manager':    
                    for user_api in user_api_list:
                        if user_api.username == relation_user['username']:
                            user_api.create_app(app)
                            break
                    return

    def find_and_create_org_app(self, app, relations, user_api_list):
        for relation_user in relations:
            for user_app in relation_user['apps']:
                if user_app['name'] == app['name'] and user_app['role'] == 'Manager':    
                    for user_api in user_api_list:
                        if user_api.username == relation_user['username']:
                            user_api.create_app(app)
                            break
                    return


def main():
    pass

if __name__ == "__main__":
    main()
