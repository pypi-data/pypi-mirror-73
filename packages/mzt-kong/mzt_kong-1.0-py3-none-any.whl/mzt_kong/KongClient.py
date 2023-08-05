from mzt_http_utils.HTTPUtils import *


class KongClient:

    def __init__(self, server, port=8001):
        if server is None or server == '':
            raise KongException('Server cannot be empty')
        self.server = server + ':' + str(port)
        self.http = HTTPUtils()

    def create_user(self, username: str, custom_id: str):
        if username is None or username == '':
            raise KongException('Username cannot be empty')
        if custom_id is None or custom_id == '':
            raise KongException('Custom ID cannot be empty')
        req = RequestArgs()
        req.method = HTTPMethod.POST
        req.url = self.server + '/consumers'
        req.data = {
            'username': username,
            'custom_id': custom_id
        }
        response = json.loads(self.http.execute(req))
        text = json.loads(response['text'])
        if response['status_code'] == 201:
            return {
                'status': 201,
                'id': text['id']
            }
        else:
            return {
                'status': response['status_code'],
                'id': text['message']
            }

    def get_key(self, username):
        if username is None or username == '':
            raise KongException('Username cannot be empty')
        req = RequestArgs()
        req.method = HTTPMethod.GET
        req.url = self.server + '/consumers/' + username + '/key-auth'
        response = json.loads(self.http.execute(req))
        text = json.loads(response['text'])
        if response['status_code'] == 200:
            return {
                'status': 200,
                'id': text['data'][0]['id'],
                'key': text['data'][0]['key']
            }
        else:
            return {
                'status': response['status_code'],
                'id': '',
                'key': 'Error'
            }

    def create_key(self, username):
        if username is None or username == '':
            raise KongException('Username cannot be empty')
        key = self.get_key(username)
        if key['status'] == 200 and key['key'] is not None and key['key'] != '':
            req = RequestArgs()
            req.method = HTTPMethod.DELETE
            req.url = self.server + '/consumers/' + username + '/key-auth/' + key['id']
            self.http.execute(req)
        req = RequestArgs()
        req.method = HTTPMethod.POST
        req.url = self.server + '/consumers/' + username + '/key-auth'
        req.data = {}
        response = json.loads(self.http.execute(req))
        text = json.loads(response['text'])
        if response['status_code'] == 201:
            return {
                'status': 201,
                'key': text['key']
            }
        else:
            return {
                'status': response['status_code'],
                'key': text['message']
            }

    def get_user(self, key):
        if key is None or key == '':
            raise KongException('Key cannot be empty')
        req = RequestArgs()
        req.url = self.server + '/key-auths/' + key + '/consumer'
        response = json.loads(self.http.execute(req))
        text = json.loads(response['text'])
        if response['status_code'] == 200:
            return {
                'status': 200,
                'id': text['id'],
                'custom_id': text['custom_id'],
                'username': text['username']
            }
        else:
            return {
                'status': response['status_code'],
                'id': text['message'],
                'custom_id': '',
                'username': ''
            }


class KongException(Exception):

    def __init__(self, message):
        self.message = message
