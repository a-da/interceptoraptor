import requests


def get_people(people_id: int, method='GET', url='https://swapi.dev/api/people/'):
    del method
    response = requests.get(url + people_id)
    return response.json()
