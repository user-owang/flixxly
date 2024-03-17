import requests
from secret import READ_TOKEN
import urllib.parse
import datetime

headshot_url = 'https://media.themoviedb.org/t/p/w470_and_h470_face'
poster_url = 'https://media.themoviedb.org/t/p/w440_and_h660_face'
person_icon_url = 'https://media.themoviedb.org/t/p/w132_and_h132_face'
movie_icon_url = 'https://media.themoviedb.org/t/p/w188_and_h282_bestv2'


def convert_date(data, key):
    """reformats a specified key in a dictionary provided from a date string 'mm-dd-yyyy' to 'Mon dd, yyyy' for all entries in results"""
    if 'results' in data:
        for item in data['results']:
            if item[key] != '':
                adate = item[key]
                newdate = datetime.datetime.strptime(adate, '%Y-%m-%d').strftime('%b %d, %Y')
                item['formatted_date'] = newdate

def person_fetch(id):
    """Pulls basic person information from tmdb API given a person id. Returns a python dict"""
    url = f"https://api.themoviedb.org/3/person/{id}?append_to_response=movie_credits&language=en-US"

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

def person_search(term, page):
    """pulls search results for people from tmdb API"""
    query = urllib.parse.quote_plus(term)
    url = f"https://api.themoviedb.org/3/search/person?query={query}&include_adult=false&language=en-US&page={page}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {READ_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def movie_search(term, page):
    """pulls search results for movies from tmdb API"""
    query = urllib.parse.quote_plus(term)
    url = f"https://api.themoviedb.org/3/search/movie?query={query}&include_adult=false&language=en-US&page={page}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {READ_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def first_result_type(term):
    """Returns person or movie or N/A (excluding other result types) depending on what media type the top search result for term is."""
    results_list = multi_search(term)
    result_index = 0
    while result_index < len(results_list['results']):
        media_type = results_list['results'][result_index]['media_type']

        if media_type == "person" or media_type == "movie":
            return media_type

        result_index += 1
    return "user"

def get_new_movies(follows, page):
    day = datetime.date.today()
    today = day.strftime('%Y-%m-%d')
    people = "%7C".join(follows)

    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page}&primary_release_date.gte={today}&sort_by=primary_release_date.asc&with_people={people}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {READ_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def get_old_movies(follows,page):
    day = datetime.date.today()
    today = f'{day.year}-{day.month}-{day.day}'
    people = "%7C".join(follows)

    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page}&primary_release_date.lte={today}&sort_by=primary_release_date.desc&with_people={people}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {READ_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def get_trending_movies():
    """Returns python object with a list of trending movies under the 'results' key"""
    url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {READ_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def get_trending_people():
    """Returns python object with a list of trending people under the 'results' key"""
    url = "https://api.themoviedb.org/3/trending/person/day?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {READ_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    return response.json()

def get_now_showing(page):
    """Returns python object with a list of movies in theatres under the 'results' key. Accepts page input."""
    url = f"https://api.themoviedb.org/3/movie/now_playing?language=en-US&page={page}&region=US"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {READ_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    return response.json()