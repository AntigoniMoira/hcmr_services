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

def get_tilte(product, region, language):
    if language == 'gr':
        if product == 'weather':
            if region == 'gr':
                return 'Πρόγνωση Καιρού για την Ελλάδα'
            elif region == 'eur':
                return 'Πρόγνωση Καιρού για την Ευρώπη'
            else: #bsea
                return 'Πρόγνωση Καιρού για τη Μαύρη Θάλασσα'
        elif product == 'sea-state':
            if region == 'aeg':
                return 'Πρόγνωση Κυματισμού για το Αιγαίο'
            elif region == 'med':
                return 'Πρόγνωση Κυματισμού για τη Μεσόγειο'
            else: #bsea
                return 'Πρόγνωση Κυματισμού για τη Μαύρη Θάλασσα'
        elif product == 'sailing':
            if region == 'naeg':
                return 'Προγνώσεις Ναυσιπλοΐας (Άνεμος - Κυματισμός) για το Βόρειο Αιγαίο'
            elif region == 'saeg':
                return 'Προγνώσεις Ναυσιπλοΐας (Άνεμος - Κυματισμός) για το Νότιο Αιγαίο'
            elif region == 'cycl':
                return 'Προγνώσεις Ναυσιπλοΐας (Άνεμος - Κυματισμός) για τις Κυκλάδες'
            elif region == 'ion':
                return 'Προγνώσεις Ναυσιπλοΐας (Άνεμος - Κυματισμός) για το Ιόνιο'
            else: #dod
                return 'Προγνώσεις Ναυσιπλοΐας (Άνεμος - Κυματισμός) για τα Δωδεκάνησα'
        elif product == 'sea-level':
            return 'Πρόγνωση Θαλάσσιας Στάθμης'
        elif product == 'ocean':
            if region == 'aeg':
                return 'Πρόγνωση Κυκλοφορίας για το Αιγαίο'
            else: #med
                return 'Πρόγνωση Κυκλοφορίας για τη Μεσόγειο'
        else: #ecosystem
            return 'Πρόγνωση Οικοσυστήματος για τη Μεσόγειο'
    else:
        if product == 'weather':
            if region == 'gr':
                return 'Weather Forecast for Greece'
            elif region == 'eur':
                return 'Weather Forecast for Europe'
            else: #bsea
                return 'Weather Forecast for Black Sea'
        elif product == 'sea-state':
            if region == 'aeg':
                return 'Sea State Forecast for Aegean'
            elif region == 'med':
                return 'Sea State Forecast for Mediterranean'
            else: #bsea
                return 'Sea State Forecast for Black Sea'
        elif product == 'sailing':
            if region == 'naeg':
                return 'Sailing (Wind and Sea State) Forecast for North Aegean'
            elif region == 'saeg':
                return 'Sailing (Wind and Sea State) Forecast for South Aegean'
            elif region == 'cycl':
                return 'Sailing (Wind and Sea State) Forecast for Cyclades'
            elif region == 'ion':
                return 'Sailing (Wind and Sea State) Forecast for Ionian'
            else: #dod
                return 'Sailing (Wind and Sea State) Forecast for Dodecanesse'
        elif product == 'sea-level':
            return 'Sea Level Forecast'
        elif product == 'ocean':
            if region == 'aeg':
                return 'Ocean Forecast for Aegean'
            else: #med
                return 'Ocean Forecast for Mediterranean'
        else: #ecosystem
            return 'Ecosystem Forecast for Mediterranean'
        

def get_params(product, region, language):
    if language == 'gr':
        if product == 'weather':
            if region == 'gr' or region == 'bsea':
                params = [{'value' :'meteo^windb', 'html': 'Άνεμος επιφάνειας (10μ)'},{'value' : 'meteo^rain', 'html' : 'Βροχόπτωση (χιλ. ανά 3ωρο)'}, {'value' : 'meteo^snow', 'html' : 'Χιονόπτωση (χιλ. ανά 3ωρο)'},
                {'value' : 'meteo^cloud', 'html' : 'Νεφοκάλυψη'}, {'value' : 'meteo^tem', 'html' : 'Θερμοκρασία Αέρα (2μ)'}, {'value' : 'meteo^msl', 'html' : 'Ατμοσφαιρική Πίεση'}]
            elif region =='eur':
                params = [{'value' :'meteo^windb', 'html': 'Άνεμος επιφάνειας (10μ)'},{'value' : 'meteo^rain', 'html' : 'Βροχόπτωση (χιλ. ανά 3ωρο)'}, {'value' : 'meteo^snow', 'html' : 'Χιονόπτωση (χιλ. ανά 3ωρο)'},
                {'value' : 'meteo^cloud', 'html' : 'Νεφοκάλυψη'}, {'value' : 'meteo^tem', 'html' : 'Θερμοκρασία Αέρα (2μ)'}, {'value' : 'meteo^dust', 'html' : 'Φορτίο Σκόνης'}, {'value' : 'meteo^msl', 'html' : 'Ατμοσφαιρική Πίεση'}]
        elif product == 'sea-state':
            params = [{'value' : 'waves^wht', 'html' : 'Ύψος  & Κατεύθυνση Κύματος'}]
        elif product == 'sailing':
                params =[{'value' :'meteo^windb', 'html': 'Άνεμος επιφάνειας (10μ)'}, {'value' : 'waves^wht', 'html' : 'Ύψος  & Κατεύθυνση Κύματος'}]
        elif product == 'sea-level':
            params =[{'value' :'surge^etotal', 'html': 'Συνολική ανύψωση'}, {'value' : 'surge^tide', 'html' : 'Παλιρροιακή ανύψωση'}, {'value' : 'surge^surge', 'html' : 'Surge Elevation'}]
        elif product == 'ocean':
            params =[{'value' :'ocean^temp', 'html': 'Θερμοκρασία Επιφάνειας'}, {'value' : 'ocean^sal', 'html' : 'Αλατότητα Επιφάνειας'}, {'value' : 'ocean^vel', 'html' : 'Κυκλοφορία Επιφάνειας'}, {'value' : 'ocean^sse', 'html' : 'Ανύψωση Ελεύθερης Επιφάνειας'}]
        else: #ecosystem
            params = [{'value' : 'ecology^chl', 'html' : 'Χλωροφύλλη-α (0-10 μ. μ.ο.)'},
                        {'value' : 'ecology^n3n', 'html' : 'Νιτρικά (Επιφάνεια)'},
		                {'value' : 'ecology^n1p', 'html' : 'Φωσφορικά (Επιφάνεια)'},
		                {'value' : 'ecology^b1c', 'html' : 'Βακτηριδιακή Βιομάζα (Επιφάνεια)'},
		                {'value' : 'ecology^z4c', 'html' : 'Μεσοζωοπλανκτόν (Επιφάνεια)'},
		                {'value' : 'ecology^phy', 'html' : 'Βιομάζα Φυτοπλανκτού (Επιφάνεια)'},
		                {'value' : 'ecology^netpp', 'html' : 'Πρωτογενής Παραγωγή (Επιφάνεια)'},
		                {'value' : 'ecology^prodb1', 'html' : 'Βακτηριδιακή Παραγωγή (Επιφάνεια)'},
		                {'value' : 'ecology^netppI', 'html': 'Πρωτογενής Παραγωγή (Ολοκληρωμένη)'},
		                {'value' : 'ecology^prodb1I', 'html' : 'Βακτηριδιακή Παραγωγή (Ολοκληρωμένη)'},
		                {'value' : 'ecology^chlTrJ', 'html' : 'Χλωροφύλλη-α(Δ-Α κατακορυφη τομη)'},
		                {'value' : 'ecology^chlTrI', 'html' :  'Χλωροφύλλη-α(Ν-Β κατακόρυφη τομή)'},
		                {'value' : 'ecology^n1pTrJ',  'html' : 'Φωσφορικά(Δ-Α κατακόρυφη τομή)'},
		                {'value' : 'ecology^n1pTrI', 'html' : 'Φωσφορικά (Ν-Β κατακόρυφη τομή)'},
		                {'value' : 'ecology^n3nTrJ', 'html' : 'Νιτρικά(Δ-Α κατακόρυφη τομή)'},
		                {'value' : 'ecology^n3nTrI', 'html' : 'Νιτρικά (Ν-Β κατακόρυφη τομή)'}]
        return params
    else:
        if product == 'weather':
            if region == 'gr' or region == 'bsea':
                params = [{'value' :'meteo^windb', 'html': 'Surface Wind (10m)'},{'value' : 'meteo^rain', 'html' : 'Rainfall (mm/3h)'}, {'value' : 'meteo^snow', 'html' : 'Snowfall (mm/3h)'},
                {'value' : 'meteo^cloud', 'html' : 'Cloudiness'}, {'value' : 'meteo^tem', 'html' : 'Air Temperature (2m)'}, {'value' : 'meteo^msl', 'html' : 'Atmospheric Pressure'}]
            elif region =='eur':
                params = [{'value' :'meteo^windb', 'html': 'Surface Wind (10m)'},{'value' : 'meteo^rain', 'html' : 'Rainfall (mm/3h)'}, {'value' : 'meteo^snow', 'html' : 'Snowfall (mm/3h)'},
                {'value' : 'meteo^cloud', 'html' : 'Cloudiness'}, {'value' : 'meteo^tem', 'html' : 'Air Temperature (2m)'}, {'value' : 'meteo^dust', 'html' : 'Dust Load'}, {'value' : 'meteo^msl', 'html' : 'Atmospheric Pressure'}]
        elif product == 'sea-state':
            params = [{'value' : 'waves^wht', 'html' : 'Wave Height & Direction'}]
        elif product == 'sailing':
                params =[{'value' :'meteo^windb', 'html': 'Surface Wind (10m)'}, {'value' : 'waves^wht', 'html' : 'Wave Height & Direction'}]
        elif product == 'sea-level':
            params =[{'value' :'surge^etotal', 'html': 'Total Elevation'}, {'value' : 'surge^tide', 'html' : 'Tidal Elevation'}, {'value' : 'surge^surge', 'html' : 'Surge Elevation'}]
        elif product == 'ocean':
            params =[{'value' :'ocean^temp', 'html': 'Sea Surface Temperature'}, {'value' : 'ocean^sal', 'html' : 'Sea Surface Salinity'}, {'value' : 'ocean^vel', 'html' : 'Surface (5m) Circulation'}, {'value' : 'ocean^sse', 'html' : 'Free Surface Elevation'}]
        else: #ecosystem
            params = [{'value' : 'ecology^chl', 'html' : 'Chlorophyll-a (0-10m aver.)'},
                        {'value' : 'ecology^n3n', 'html' : 'Nitrates (Surface)'},
		                {'value' : 'ecology^n1p', 'html' : 'Phosphates (Surface)'},
		                {'value' : 'ecology^b1c', 'html' : 'Bacteria Biomass (Surface)'},
		                {'value' : 'ecology^z4c', 'html' : 'Mesozooplankton (Surface)'},
		                {'value' : 'ecology^phy', 'html' : 'Phytoplankton Biomass (Surface)'},
		                {'value' : 'ecology^netpp', 'html' : 'Primary Production (Surface)'},
		                {'value' : 'ecology^prodb1', 'html' : 'Bacterial Production (Surface)'},
		                {'value' : 'ecology^netppI', 'html': 'Primary Production (Integrated)'},
		                {'value' : 'ecology^prodb1I', 'html' : 'Bacterial Production (Integrated)'},
		                {'value' : 'ecology^chlTrJ', 'html' : 'Chlorophyll-a(West-East transect)'},
		                {'value' : 'ecology^chlTrI', 'html' :  'Chlorophyll-a(South-North transect)'},
		                {'value' : 'ecology^n1pTrJ',  'html' : 'Phosphates (West-East transect)'},
		                {'value' : 'ecology^n1pTrI', 'html' : 'Phosphates (South-North transect)'},
		                {'value' : 'ecology^n3nTrJ', 'html' : 'Nitrates (West-East transect)'},
		                {'value' : 'ecology^n3nTrI', 'html' : 'Nitrates (South-North transect)'}]
        return params