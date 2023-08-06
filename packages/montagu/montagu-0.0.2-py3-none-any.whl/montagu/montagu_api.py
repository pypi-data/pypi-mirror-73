import requests


class MontaguAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        auth_url = self.build_url('authenticate')
        data = 'grant_type=client_credentials'
        auth = (username, password)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(auth_url, data=data, auth=auth,
                                 headers=headers)
        if response.status_code != 200:
            msg = 'Unexpected status code: {}. Unable to authenticate.'
            raise Exception(msg.format(response.status_code))
        self.token = response.json()['access_token']

    def diseases(self):
        return self.get('diseases')

    def get(self, route):
        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        url = self.build_url(route)
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            msg = 'Unexpected status code: {}'
            raise Exception(msg.format(response.status_code))
        return response.json()['data']

    def build_url(self, route):
        return '{}/v1/{}/'.format(self.base_url, route)
