import requests

def cURL_AT_request(code, redirect_url, cliend_id, cliend_secret):
    data = [
    ('grant_type','authorization_code'),
    ('code', code),
    ('redirect_uri', redirect_url)
    ]

    response = requests.post('http://localhost:8000/o/token/', data=data,  auth=(cliend_id, cliend_secret))
    return response

def cURL_REV_request(token, token_type, cliend_id, cliend_secret):
    data = [
    ('token', token),
    ('token_type_hint', token_type)
    ]

    response = requests.post('http://localhost:8000/o/revoke_token/', data=data,  auth=(cliend_id, cliend_secret))
    return response
    