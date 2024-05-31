import requests

def get_client_ip():
    response = requests.get("https://httpbin.org/ip")
    return response.json()['origin']

def get_client_location(ip):
    # Using SypexGeo as an example
    response = requests.get(f"https://api.sypexgeo.net/json/{ip}")
    location_data = response.json()
    return {
        'latitude': location_data['city']['lat'],
        'longitude': location_data['city']['lon']
    }
