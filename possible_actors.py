"""defines a list of 300 actors born in the USA sorted by popularity that provide users with non-obscure starting points"""
import requests
import json
from tmdb import *

# secret is a file that contains an API key for tmdb's API which you will need to provide yourself should you want to use this code
from secret import READ_TOKEN

list_of_actors = []
headshot_url = 'https://media.themoviedb.org/t/p/w470_and_h470_face'
    
def set_list():
    while len(list_of_actors) < 10:
        page = 1
        url = f"https://api.themoviedb.org/3/person/popular?language=en-US&page={page}"
        headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {READ_TOKEN}"
        }
        response = requests.get(url, headers=headers)
        search = response.json()
        for actor in search["results"]:
            if len(list_of_actors) >=10:
                break
            person = actor_fetch(actor['id'])
            if person['place_of_birth'] is not None and 'USA' in person['place_of_birth']:
                item = create_actor(actor['id'])
                list_of_actors.append(item)
        if len(list_of_actors) < 10:
            page += 1

def reset_list():
    list_of_actors = []
    set_list()