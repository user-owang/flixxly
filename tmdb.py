import requests
from secret import READ_TOKEN
import urllib.parse

headshot_url = 'https://media.themoviedb.org/t/p/w470_and_h470_face'
poster_url = 'https://media.themoviedb.org/t/p/w440_and_h660_face'
person_icon_url = 'https://media.themoviedb.org/t/p/w132_and_h132_face'
movie_icon_url = 'https://media.themoviedb.org/t/p/w188_and_h282_bestv2'


def person_fetch(id):
    """Pulls basic person information from tmdb API given a person id. Returns a python dict"""
    url = f"https://api.themoviedb.org/3/person/{id}?append_to_response=movie_credits&language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {READ_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def person_credits(id):
    """Pulls person filmography from tmdb API given a person id. Returns a python dict"""
    url = f"https://api.themoviedb.org/3/person/{id}/movie_credits?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {READ_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def movie_fetch(id):
    """Pulls basic movie information from tmdb API given a movie id. Returns a python dict"""
    url = f"https://api.themoviedb.org/3/movie/{id}?append_to_response=credits&language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {READ_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    
    return response.json()

def movie_credits(id):
    """Pulls movie cast from tmdb API given a movie id. Returns a python dict"""
    url = "https://api.themoviedb.org/3/movie/{id}/credits?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {READ_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def multi_search(term):
    """Pulls search results"""
    query = urllib.parse.quote_plus(term)
    url = f"https://api.themoviedb.org/3/search/multi?query={query}&include_adult=false&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {READ_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def create_person(id):
    """Creates a simplified person python dict with only the information we will need. Requires a person id"""
    info = person_fetch(id)
    filmography = person_credits(id)

    response = dict()
    response['id'] = id
    response['name'] = info['name']
    response['img_url'] = f"{headshot_url}{info['profile_path']}"
    response['movies'] = []

    for credit in filmography['cast']:
        movie = {
            'title': credit['original_title'],
            'id': credit['id']
        }
        response['movies'].append(movie)
    
    return response

def create_movie(id):
    """Creates a simplified movie python dict with only the information we will need. Requires movie id"""
    info = movie_fetch(id)
    cast = movie_credits(id)

    response = dict()
    response['id'] = id
    response['title'] = info['title']
    response['img_url'] = f"{poster_url}{info['poster_path']}"
    response['actors'] = []
    
    for role in cast['cast']:
        actor = {
            'name': role['name'],
            'id': role['id']
        }
        response['actors'].append(actor)
    
    return response

def search_results(term):
    """Returns a search result python dict with a list of simplified dicts that contain only the information we need. Requires search term"""
    results_list = multi_search(term)
    response = {
        'results': []
    }

    for item in results_list['results']:
        if item['media_type'] != 'tv':
            query = {
                'type': item['media_type'],
                'id': item['id']
            }
            if item['media_type'] == 'person':
                query['img_url'] = f"{person_icon_url}{item['profile_path']}"
                query['name'] = item['name']
            if item['media_type'] == 'movie':
                query['img_url'] = f"{movie_icon_url}{item['poster_path']}"
                query['title']: item['title']
            response['results'].append(query)
    
    return response

# def create_feed(following):
    