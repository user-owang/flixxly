from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from secret import READ_TOKEN, SECRET_KEY
from tmdb import *
import datetime
from forms import LoginForm, AddUserForm
from models import db, connect_db,User, Follow, Watchlist, Seenlist, Movie, Person

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flixxly'
app.config['SECRET_KEY'] = SECRET_KEY


person_icon_url = 'https://media.themoviedb.org/t/p/w180_and_h180_face'
movie_icon_url = 'https://media.themoviedb.org/t/p/w188_and_h282_bestv2'

connect_db(app)
with app.app_context():
    db.create_all()

# login/logout helpers

@app.before_request
def add_user_to_g():
    """If user is logged in, add curr user to Flask global."""

    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session['user_id'] = user.id


def do_logout():
    """Logout user."""

    if 'user_id' in session:
        del session['user_id']
        g.user = None
        flash('Successfully logged out.')
    else:
        flash('You are not signed in.')

def db_add_movie(id):
    """Adds a new movie from TMDB API to db associated with input id."""
    movie_to_add = movie_fetch(id)
    if movie_to_add.get('title'):
        movie = Movie(id=id,
                      title=movie_to_add['title'])
        if movie_to_add['poster_path']:
            movie.img_url = movie_to_add['poster_path']
        if movie_to_add['overview'] != '':
            movie.overview = movie_to_add['overview']
        if movie_to_add['release_date'] != "":
            input = movie_to_add['release_date']
            release = datetime.datetime.strptime(input, '%Y-%m-%d')
            year = int(input[:4])
            movie.release_date = release
            movie.release_year = year
        
        db.session.add(movie)
        db.session.commit()

def db_update_movie(id):
    """Checks TMDB API for any changes to movie with input id. If so, updates db copy to match API."""
    movie_api = movie_fetch(id)
    movie_db = Movie.query.get(id)
    if not movie_db.img_url or movie_db.overview == 'No overview available at this time.' or not movie_db.release_year:
        if movie_api['poster_path']:
            movie_db.img_url = movie_api['poster_path']
        if movie_api['overview'] != '':
            movie_db.overview = movie_api['overview']
        if movie_api['release_date'] != '':
            input = movie_api['release_date']
            release = datetime.datetime.strptime(input, '%Y-%m-%d')
            year = int(input[:4])
            movie_db.release_date = release
            movie_db.release_year = year
        
        db.session.commit()

def db_add_person(id):
    """Adds new person from TMDB API to db with input id."""
    person_to_add = person_fetch(id)
    if person_to_add.get('name'):
        person = Person(id=id,
                        name=person_to_add['name'],
                        known_for=person_to_add['known_for_department'])
        if person_to_add['profile_path']:
            person.img_url = person_to_add['profile_path']
        
        db.session.add(person)
        db.session.commit()

def db_update_person(id):
    """Checks TMDB for any changes to person with input id. If so, updates db copy to match."""
    person_api = person_fetch(id)
    person_db = Person.query.get(id)
    if not person_db.img_url:
        if person_api['profile_path']:
            person_db.img_url = person_api['profile_path']

        db.session.commit()

def find_age(str):
    '''Takes a string with date format YYYY-MM-DD. Outputs age in years.'''
    year,month,day = map(int, str.split("-"))
    today = datetime.date.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    return age

def return_gender(person):
    """Accepts person dictionary from API call as an input and returns string with gender value male/female/non-binary"""
    if person['gender'] == 0:
        return 'Not set / not specified'
    elif person['gender'] == 1:
        return 'Female'
    elif person['gender'] == 2:
        return 'Male'
    elif person['gender'] == 3:
        return'Non-binary'
    
def get_crew_dpts(movie):
    """Accepts a movie dictionary from an API call. returns"""
    departments = set()
    for member in movie['credits']['crew']:
        dpt = member.get('department')
        if dpt:
            departments.add(dpt)
    return sorted(departments)

def unwatch(movie):
    """Accepts a Movie object from a query. Removes movie from g.user watchlist."""
    g.user.watchlist.remove(movie)
    db.session.commit()

def unseen(movie):
    """Accepts a Movie object from a query. Removes movie from g.user seenlist."""
    g.user.seenlist.remove(movie)
    db.session.commit()

def unfollow(person):
    """Accepts a Person object from a query. Removes movie from g.user seenlist."""
    g.user.follows.remove(person)
    db.session.commit()

# api routes

@app.route('/api/search', methods=['POST'])
def search_db():
    """Searches tmdb API for person or movie. Input term; returns json object with a page's worth of result objects."""
    data = request.get_json()
    response = search_results(data['term'])
    return jsonify(response)

@app.route('/api/get_person', methods=['POST'])
def get_person():
    """Searches tmdb API for person. Input person ID; returns json object for person."""
    data = request.get_json()
    response = create_person(data['id'])
    return jsonify(response)

@app.route('/api/get_movie', methods=['POST'])
def get_movie():
    """Searches tmdb API for movie. Input movie ID; returns json object for person."""
    data = request.get_json()
    response = create_movie(data['id'])
    return jsonify(response)

# website routes

@app.route('/register', methods=['POST', 'GET'])
def registration():
    form = AddUserForm()
    if g.user:
        return redirect(f'/users/{g.user.id}')

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        if data['password'] != data['confirm_password']:
            flash('Passwords do not match')
            return redirect('/register')
        if User.query.filter_by(username=data['username']).first():
            flash('Username already exists.')
            return redirect('/register')
        if User.query.filter_by(email=data['email']).first():
            flash('Email is already associated with another account.')
            return redirect('/register')
        User.signup(data['username'], data['password'], data['email'])
        db.session.commit()
        user1 = User.query.filter_by(username=data['username']).first()
        do_login(user1)
        flash("Account successfully created")
        return redirect(f'/users/{user1.id}')
  
    return render_template('registration.html', form = form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if g.user:
        return redirect(f'/users/{g.user.id}')
  
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user1 = User.authenticate(username, password)
        if user1:
            do_login(user1)
            return redirect(f'/users/{user1.id}')
        flash('Incorrect login info.')
        return redirect('/login')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    return redirect('/login')

# user routes

@app.route('/users/<int:id>')
def show_user(id):
    user = User.query.get_or_404(id)
    return render_template('user.html', user=user)

@app.route('/users/<int:id>/edit')
def edit_user(id):
    user = User.query.get_or_404(id)
    if g.user.id != id:
        flash('You are not authorized to edit other profiles.')
        return redirect(f'/users/{g.user.id}')
    return render_template('edit_user.html', user=user)

# movie routes

@app.route('/movies/<int:id>')
def show_movie(id):
    movie = movie_fetch(id)
    departments = get_crew_dpts(movie)
    return render_template('movie.html', movie=movie, departments=departments)

@app.route('/movies/add-watchlist/<int:id>', methods=['POST'])
def add_watchlist(id):
    if not g.user:
        flash('Must be logged in to do that.')
        return redirect('/login')
    movie_to_add = movie_fetch(id)
    if movie_to_add.get('title'):
        if Movie.query.filter_by(id=id).first() == None:
            db_add_movie(id)
        else:
            db_update_movie(id)
        item = Watchlist(user_id = g.user.id, movie_id = id)
        
        db.session.add(item)
        db.session.commit()

        flash(f'{movie_to_add["title"]} successfully added to watchlist.')
    else:
        flash('Invalid movie.')
    prev = request.referrer
    return redirect(prev)

@app.route('/movies/remove-watchlist/<int:id>', methods=['POST'])
def remove_watchlist(id):
    if not g.user:
        flash("Must be logged in to do that.")
        return redirect('/login')
    movie = Movie.query.get_or_404(id)
    if movie:
        unwatch(movie)
        flash(f'{movie.title} removed from watchlist.')
    else:
        flash('Invalid movie.')
    prev = request.referrer
    return redirect(prev)

@app.route('/movies/add-seenlist/<int:id>', methods=['POST'])
def add_seenlist(id):
    if not g.user:
        flash('Must be logged in to do that.')
        return redirect('/login')
    movie_to_add = movie_fetch(id)
    if movie_to_add.get('title'):
        db_movie = Movie.query.filter_by(id=id).first()
        if db_movie == None:
            db_add_movie(id)
        else:
            db_update_movie(id)
        if db_movie in g.user.watchlist:
            unwatch(db_movie)
            flash(f'{movie_to_add["title"]} has been moved from watchlist to seenlist.')
        else:
            flash(f'{movie_to_add["title"]} successfully added to seenlist.')
        item = Seenlist(user_id = g.user.id, movie_id = id)
        
        db.session.add(item)
        db.session.commit()

        
    else:
        flash('Invalid movie.')
    prev = request.referrer
    return redirect(prev)

@app.route('/movies/remove-seenlist/<int:id>', methods=['POST'])
def remove_seenlist(id):
    if not g.user:
        flash("Must be logged in to do that.")
        return redirect('/login')
    movie = Movie.query.get_or_404(id)
    if movie:
        unseen(movie)
        flash(f'{movie.title} removed from seenlist.')
    else:
        flash('Invalid movie.')
    prev = request.referrer
    return redirect(prev)

# people routes

@app.route('/people/<int:id>')
def show_person(id):
    person = person_fetch(id)
    input = person.get('birthday')
    birthdate=''
    age= ''
    gender=''
    if input:
        birthday = datetime.datetime.strptime(input, '%Y-%m-%d')
        birthdate = birthday.strftime('%B %d, %Y')
        age = find_age(input)
    if person.get('gender'):
        gender = return_gender(person)
    return render_template('person.html', person=person, birthdate=birthdate, age=age, gender=gender)

@app.route('/people/add-follow/<int:id>', methods=['POST'])
def add_follow(id):
    if not g.user:
        flash('Must be logged in to do that.')
        return redirect('/login')
    person_to_add = person_fetch(id)
    if person_to_add.get('name'):
        if Person.query.filter_by(id=id).first() == None:
            db_add_person(id)
        else:
            db_update_person(id)
        item = Follow(user_id = g.user.id, person_id = id)
        
        db.session.add(item)
        db.session.commit()

        flash(f'You are now following {person_to_add["name"]}.')
    else:
        flash('Invalid person.')
    prev = request.referrer
    return redirect(prev)

@app.route('/people/remove-follow/<int:id>', methods=['POST'])
def remove_follow(id):
    if not g.user:
        flash("Must be logged in to do that.")
        return redirect('/login')
    person = Person.query.get_or_404(id)
    if person:
        unfollow(person)
        flash(f'You are no longer following {person.name}')
    else:
        flash('Invalid person.')
    prev = request.referrer
    return redirect(prev)