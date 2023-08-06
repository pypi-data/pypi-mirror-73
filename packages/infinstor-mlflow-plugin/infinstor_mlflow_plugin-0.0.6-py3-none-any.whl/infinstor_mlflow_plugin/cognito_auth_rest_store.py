from mlflow.store.tracking.rest_store import RestStore
from mlflow.utils.rest_utils import MlflowHostCreds
import datetime
import requests
from requests.exceptions import HTTPError
import json
from infinstor_mlflow_plugin.tokenfile import read_token_file, write_token_file
from os.path import expanduser
from os.path import sep as separator

verbose = False
token = None
refresh_token = None
token_time = None
client_id = None
service = None

class CognitoAuthenticatedRestStore(RestStore):
    def renew_token(self):
        global token_time
        global token
        global refresh_token
        global client_id
        global service

        payload = "{\n"
        payload += "    \"AuthParameters\" : {\n"
        payload += "        \"REFRESH_TOKEN\" : \"" + refresh_token + "\"\n"
        payload += "    },\n"
        payload += "    \"AuthFlow\" : \"REFRESH_TOKEN_AUTH\",\n"
        payload += "    \"ClientId\" : \"" + client_id + "\"\n"
        payload += "}\n"

        url = 'https://cognito-idp.us-east-1.amazonaws.com:443/'

        headers = {
                'Content-Type': 'application/x-amz-json-1.1',
                'X-Amz-Target' : 'AWSCognitoIdentityProviderService.InitiateAuth'
                }

        try:
            response = requests.post(url, data=payload, headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            raise
        except Exception as err:
            print(f'Other error occurred: {err}')
            raise
        else:
            authres = response.json()['AuthenticationResult']
            token = authres['IdToken']
            token_time = round(datetime.datetime.timestamp(datetime.datetime.utcnow()))
            tokfile = expanduser("~") + separator + '.infinstor' + separator + '/token'
            write_token_file(tokfile, token_time, token, refresh_token, client_id, service)

    def get_token(self):
        global token_time
        global token
        global refresh_token
        global client_id
        global service

        if (token == None):
            tokfile = expanduser("~") + separator + '.infinstor' + separator + '/token'
            token, refresh_token, token_time, client_id, service = read_token_file(tokfile)

        time_now = round(datetime.datetime.timestamp(datetime.datetime.utcnow()))
        if ((token_time + (45 * 60)) < time_now):
            if (verbose):
                print('InfinStor token has expired. Calling renew ' + str(token_time)\
                        + ', ' + str(time_now))
            self.renew_token()
        else:
            if (verbose):
                print('InfinStor token has not expired ' + str(token_time) + ', ' + str(time_now))
        return True

    def cognito_host_creds(self):
        global token
        global service
        self.get_token()
        return MlflowHostCreds('https://mlflow.' + service + '.com:443/', token=token)

    def get_service(self):
        global service
        return service

    def get_token_string(self):
        global token
        self.get_token()
        return token

    def __init__(self, store_uri=None, artifact_uri=None):
        super().__init__(self.cognito_host_creds)

