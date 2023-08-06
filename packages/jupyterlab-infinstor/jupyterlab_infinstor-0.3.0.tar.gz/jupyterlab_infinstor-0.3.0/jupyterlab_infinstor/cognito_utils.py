import requests
from requests.exceptions import HTTPError
import json
import builtins
import os
from os.path import expanduser
from os.path import sep as separator
import datetime

def perform_infinstor_login(username, password):
    payload = "{\n"
    payload += "    \"AuthParameters\" : {\n"
    payload += "        \"USERNAME\" : \"" + username + "\",\n"
    payload += "        \"PASSWORD\" : \"" + password + "\"\n"
    payload += "    },\n"
    payload += "    \"AuthFlow\" : \"USER_PASSWORD_AUTH\",\n"
    payload += "    \"ClientId\" : \"" + builtins.clientid + "\"\n"
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
        print('Authorization success!')
        challenge = response.json().get('ChallengeName')
        if challenge == "NEW_PASSWORD_REQUIRED":
            return response.json()
        else:
            authres = response.json()['AuthenticationResult']
            builtins.idtoken = authres['IdToken']
            builtins.refreshtoken = authres['RefreshToken']

    setup_token_for_mlflow()

    payload = ("ProductCode=" + builtins.prodcode)
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': builtins.idtoken
            }

    url = 'https://api.' + builtins.service + '.com/customerinfo'

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
        print('customerinfo success!')
        return response.json()


def setup_token_for_mlflow():
    home = expanduser("~")
    dotinfinstor = home + separator + ".infinstor"
    print("Setting up token for mlflow in " + dotinfinstor)
    if (not os.path.exists(dotinfinstor)):
        try:
            os.mkdir(dotinfinstor, mode=0o755)
        except Exception as err:
            print('Error creating dir ' + dotinfinstor)
    tokfile = dotinfinstor + separator + "token"
    with open(tokfile, 'w') as wfile:
        wfile.write("Token=" + builtins.idtoken + "\n")
        wfile.write("RefreshToken=" + builtins.refreshtoken + "\n")
        wfile.write("ClientId=" + builtins.clientid + "\n")
        wfile.write("TokenTimeEpochSeconds="\
                + str(round(datetime.datetime.timestamp(datetime.datetime.utcnow()))) + "\n")
        wfile.write("Service=" + builtins.service + "\n")
        wfile.close()

