"""
Functions for cURL requests.
"""
import json
import requests
from django.conf import settings


def update_access_token(request):
    """
    Function to update access_token with refresh token.
    """
    token = request.session['refresh_token']
    curl_res = cURL_RT_request(token)
    request.session['access_token'] = json.loads(curl_res.text)['access_token']
    request.session['refresh_token'] = json.loads(curl_res.text)['refresh_token']
    return request.session['access_token']

def cURL_AT_request(code):
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.HOST_DOMAIN + '/webapp/access_token/',
        'scope': 'read introspection'
    }

    response = requests.post(settings.AUTH_DOMAIN + '/o/token/', data=data, auth=(client_id, client_secret))
    return response

def cURL_RT_request(refresh_token):
    data = {
    'grant_type': 'refresh_token',
    'client_id': client_id,
    'client_secret': client_secret,
    'refresh_token': refresh_token
    }

    response = requests.post(settings.AUTH_DOMAIN + '/o/token/', data=data)
    return response

def cURL_REV_request(token, token_type):
    data = [
    ('token', token),
    ('token_type_hint', token_type)
    ]

    response = requests.post(settings.AUTH_DOMAIN + '/o/revoke_token/', data=data, auth=(client_id, client_secret))
    return response
    
def cURL_GET_request(token, url):
    headers = {
    'Authorization': 'Bearer '+ token,
    }
    response = requests.get(url, headers=headers)
    return response

def cURL_POST_request(token, url, data):
    headers = {
    'Authorization': 'Bearer '+ token,
    }
    response = requests.post(url, headers=headers, data=data) 
    return response

def cURL_PUT_request(token, url, data):
    headers = {
    'Authorization': 'Bearer '+ token,
    }
    response = requests.put(url, headers=headers, data=data) 
    return response

def cURL_DELETE_request(token, url, data):
    headers = {
    'Authorization': 'Bearer '+ token,
    }
    response = requests.delete(url, headers=headers, data=data) 
    return response