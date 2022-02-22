#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tempfile, PIL

class Api:

    class UserApi:

        def __init__(self, client, username=''):
            self.username = username
            self.client = client

        def set_username(self, username):
            self.username = username

        def register(self, user):
            r = self.client.post('user/register', user)
            if r.status_code == 201:
                self.username = r.json()['username']
                self.client.set_username = self.username
                self.client.set_token = r.json()['token']
            return r

        def login(self, user):
            r = self.client.post('user/login', user)
            if r.status_code == 200:
                self.username = r.json()['username']
                self.client.set_username = self.username
                self.client.set_token = r.json()['token']
            return r

        def logout(self):
            return self.client.post('user/logout')

        def me(self):
            return self.client.get('user/me')

        def create_org(self, org):
            return self.client.post('orgs', org)

        def get_org_list(self):
            return self.client.get('orgs')

        def create_app(self, app):
            return self.client.post('/users/' + self.username + 'apps', app)

        def get_app_list(self, username=None):
            ownername = username
            if ownername is None:
                ownername = self.username
            return self.client.get('/users/' + ownername + 'apps')

    class OrganizationApi:
        
        def __init__(self, client, org_name):
            self.client = client
            self.base_path = '/orgs/' + org_name

        def create_app(self, app):
            return self.client.post(self.base_path + '/apps', app)

        def get_app_list(self):
            return self.client.get(self.base_path + '/apps')
        
        def get_org(self):
            return self.client.get(self.base_path)

        def update_org(self, org):
            return self.client.put(self.base_path, org)

        def remove_org(self):
            return self.client.delete(self.base_path)

        def change_or_set_icon(self, icon_file_path=None):
            if icon_file_path is None:
                image = PIL.Image.new('RGB', size=(1, 1))
                file = tempfile.NamedTemporaryFile(suffix='.jpg')
                image.save(file)
                file_path = file.name
            else:
                file_path = icon_file_path

            with open(file_path, 'rb') as fp:
                data = {'icon_file': fp}
                return self.client.upload_post(self.base_path + '/icon', data=data)

        def rempve_icon(self):
            return self.client.delete(self.base_path + '/icon')

        def add_member(self, username, role):
            collaborator = {
                'username': username,
                'role': role
            }
            return self.client.post(self.base_path + '/people/collaborators', collaborator)

        def get_member(self, username):
            return self.client.get(self.base_path + '/people/collaborators/' + username)

        def get_member_list(self):
            return self.client.get(self.base_path + '/people/collaborators')

        def change_member_role(self, username, role):
            data = {
                'role': role
            }
            return self.client.put(self.base_path + '/people/collaborators/' + username, data)

        def remove_member(self, username):
            return self.client.delete(self.base_path + '/people/collaborators/' + username)

    class ApplicationApi:

        def __init__(self, client, base_path):
            self.client = client
            self.base_path = base_path

        def get_app(self):
            return self.client.get(self.base_path)

        def update_app(self, app):
            return self.client.put(self.base_path, app)

        def remove_app(self):
            return self.client.delete(self.base_path)

        def change_or_set_icon(self, icon_file_path=None):
            if icon_file_path is None:
                image = PIL.Image.new('RGB', size=(1, 1))
                file = tempfile.NamedTemporaryFile(suffix='.jpg')
                image.save(file)
                file_path = file.name
            else:
                file_path = icon_file_path

            with open(file_path, 'rb') as fp:
                data = {'icon_file': fp}
                return self.client.upload_post(self.base_path + '/icon', data=data)

        def rempve_icon(self):
            return self.client.delete(self.base_path + '/icon')

        def add_member(self, username, role):
            collaborator = {
                'username': username,
                'role': role
            }
            return self.client.post(self.base_path + '/people/collaborators', collaborator)

        def get_member(self, username):
            return self.client.get(self.base_path + '/people/collaborators/' + username)

        def get_member_list(self):
            return self.client.get(self.base_path + '/people/collaborators')

        def change_member_role(self, username, role):
            data = {
                'role': role
            }
            return self.client.put(self.base_path + '/people/collaborators/' + username, data)

        def remove_member(self, username):
            return self.client.delete(self.base_path + '/people/collaborators/' + username)

        def upload_package(self, file_path):
            with open(file_path, 'rb') as fp:
                data = {'file': fp}
                return self.client.upload_post(self.base_path + '/distribute/packages', data=data)

        def get_package(self, internal_build):
            return self.client.get(self.base_path+ '/distribute/packages/' + str(internal_build))

        def get_package_list(self):
            return self.client.get(self.base_path + '/distribute/packages')

        def update_package(self, internal_build, package):
            return self.client.put(self.base_path + '/distribute/packages/' + str(internal_build), package)

        def remove_package(self, internal_build):
            return self.client.delete(self.base_path + '/distribute/packages/' + str(internal_build))

        def create_release(self, env, release):
            return self.client.post(self.base_path + '/distribute/releases/' + env, release)            

        def get_release(self, release_id):
            return self.client.get(self.base_path + '/distribute/releases/' + str(release_id))

        def get_release_list(self, env):
            return self.client.get(self.base_path + '/distribute/releases/' + env)

        def update_release(self, release_id, release):
            return self.client.put(self.base_path + '/distribute/releases/' + str(release_id), release)

        def remove_release(self, release_id):
            return self.client.delete(self.base_path + '/distribute/releases/' + str(release_id))            


    def __init__(self, client):
        self.client = client

    def get_user_api(self, username=''):
        return Api.UserApi(self.client, username)

    def get_org_api(self, org_name):
        return Api.OrganizationApi(self.client, org_name)

    def get_org_app_api(self, org_name, app_name):
        return Api.ApplicationApi(self.client, '/orgs/' + org_name + '/apps/' + app_name)

    def get_user_app_api(self, username, app_name):
        return Api.ApplicationApi(self.client, '/users/' + username + '/apps/' + app_name)
