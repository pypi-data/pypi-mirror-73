import os
import warnings

import requests

from . import __version__
from .graphql_client import GraphQLClient
from .mutations.user import signin

MAX_RETRIES = 20


class KiliAuth(object):
    """
    from kili.authentication import KiliAuth
    from kili.playground import Playground
    kauth = KiliAuth(email=email, password=password)
    playground = Playground(kauth)
    assets = playground.assets(project_id=project_id)
    """

    def __init__(self,
                 email=os.getenv('KILI_USER_EMAIL'),
                 password=os.getenv('KILI_USER_PASSWORD'),
                 api_endpoint='https://cloud.kili-technology.com/api/label/graphql',
                 api_key=None):
        self.session = requests.Session()

        self.check_versions_match(api_endpoint)

        adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)
        self.client = GraphQLClient(api_endpoint, self.session)
        if api_key is None:
            auth_payload = signin(self.client, email, password)
            api_token = auth_payload['token']
            self.client.inject_token('Bearer: ' + api_token)
            self.user_id = auth_payload['user']['id']
        else:
            self.client.inject_token('X-API-Key: ' + api_key)

    def __del__(self):
        self.session.close()

    @staticmethod
    def check_versions_match(api_endpoint):
        url = api_endpoint.replace('/graphql', '/version')
        response = requests.get(url).json()
        version = response['version']
        if version != __version__:
            message = 'Kili Playground version should match with Kili API version.\n' + \
                      f'Please install version: "pip install kili=={version}"'
            warnings.warn(message, UserWarning)
