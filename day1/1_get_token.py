import requests
import json

API_KEY = ''
SECRET_KEY = ''

def login():

    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}"
    
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    result = response.json()
    print(result)
    token = result['access_token']
    print('login success', token)
    return token

if __name__ == '__main__':
    login()