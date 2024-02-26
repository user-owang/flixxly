from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from secret import API_KEY, SECRET_KEY
from tmdb import *
from possible_actors import *
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///famegame'
app.config['SECRET_KEY'] = SECRET_KEY

actor_icon_url = 'https://media.themoviedb.org/t/p/w180_and_h180_face'
movie_icon_url = 'https://media.themoviedb.org/t/p/w188_and_h282_bestv2'

# connect_db(app)
# with app.app_context():
#         db.create_all()

set_list()

# api routes

@app.route('/api/search', methods=['POST'])
def search_db():
    """Searches tmdb API for person or movie. Input term; returns json object with a page's worth of result objects."""
    data = request.get_json()
    response = search_results(data['term'])
    return jsonify(response)

@app.route('/api/get_actor', methods=['POST'])
def get_actor():
    """Searches tmdb API for person. Input actor ID; returns json object for person."""
    data = request.get_json()
    response = create_actor(data['id'])
    return jsonify(response)

@app.route('/api/get_movie', methods=['POST'])
def get_movie():
    """Searches tmdb API for person. Input actor ID; returns json object for person."""
    data = request.get_json()
    response = create_movie(data['id'])
    return jsonify(response)

@app.route('/api/game_setup')
def game_setup():
    """return 2 random actors objects from list of possible actors"""
    actor1 = random.choice(list_of_actors)
    actor2 = random.choice(list_of_actors)
    while actor1['id'] == actor2['id']:
        actor2 = random.choice(list_of_actors)
    response = {
        'actor1': actor1,
        'actor2': actor2
    }
    return jsonify(response)


# website routes

@app.route('/game')
def show_game():
    return render_template('game.html')