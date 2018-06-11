import requests

def cURL_request(code, redirect_url, cliend_id, cliend_secret):
    data = [
    ('grant_type','authorization_code'),
    ('code', code),
    ('redirect_uri', redirect_url)
    ]

    response = requests.post('http://localhost:8000/o/token/', data=data,  auth=(cliend_id, cliend_secret))
    return response