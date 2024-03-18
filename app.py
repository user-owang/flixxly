from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from secret import READ_TOKEN, SECRET_KEY
from tmdb import *
import datetime
from forms import LoginForm, AddUserForm, EditProfileForm
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
            form_date = release.strftime('%b %d, %Y')
            movie.release_date = release
            movie.release_year = year
            movie.formatted_date = form_date
        
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

def is_upcoming(movie):
    """checks to see if a movie has a future release date or not. returns true or false"""
    input = movie['release_date']
    if input == '':
        return True
    release = datetime.datetime.strptime(input, '%Y-%m-%d')
    today = datetime.date.today()
    if release > today:
        return True
    return False

def user_search(term):
    """returns a python dictionary with the results of a User query looking for users with a username similar to term"""
    query = User.query.filter(User.username.ilike(f'%{term.replace(" ","")}%')).all()
    response = dict()
    if query:
        results = list()
        for user in query:
            result = dict()
            result['id'] = user.id
            result['username'] = user.username
            result['bio'] = user.bio
            result['img_url'] = user.img_url
            results.append(result)
        response['results'] = results
        response['total_results'] = len(results)
    else:
        response['results'] = []
        response['total_results'] = 0
    
    return response

# api routes

@app.route('/api/release-radar', methods=['POST'])
def rr_np():
    """Returns json object with input page of results for release radar for all people g.user is following."""
    data = request.get_json()
    follows = list()
    for person in g.user.follows:
        follows.append(str(person.id))
    response = get_new_movies(follows, data['page'])
    # convert_date(response, 'release_date')
    return jsonify(response)

@app.route('/api/past-films', methods=['POST'])
def pf_np():
    """Returns json object with input page of results for past films for all people g.user is following."""
    data = request.get_json()
    follows = list()
    for person in g.user.follows:
        follows.append(str(person.id))
    response = get_old_movies(follows, data['page'])
    # convert_date(response, 'release_date')
    return jsonify(response)

@app.route('/api/now-showing', methods=['POST'])
def ns_np():
    """Returns json object with input page of results for movies currently in theatres."""
    data = request.get_json()
    response = get_now_showing(data['page'])
    # convert_date(response, 'release_date')
    return jsonify(response)

@app.route('/api/search-results', methods=['POST'])
def sr_np():
    """Returns json object with input page of search results for term."""
    data = request.get_json()
    response = dict()
    if data['search_type'] == 'movie':
        response = movie_search(data['term'], data['page'])
        convert_date(response, 'release_date')
    if data['search_type'] == 'person':
        response = person_search(data['term'], data['page'])
    if data['search_type'] == 'user':
        response = user_search(data['term'])
    return jsonify(response)

@app.route('/api/get-follows')
def get_follows():
    """returns json object with list of person.id's from g.user.follows or empty dict"""
    response = dict()
    follows = list()
    response['user'] = False
    if g.user:
        response['user'] = True
        for person in g.user.follows:
            follows.append(person.id)
    
    response['follows'] = follows
    
    return jsonify(response)

@app.route('/api/get-watchlist')
def get_watchlist():
    """returns json object with list of movie.id's from g.user.watchlist or empty dict"""
    response = dict()
    watchlist = list()
    response['user'] = False
    if g.user:
        response['user'] = True
        for movie in g.user.watchlist:
            watchlist.append(movie.id)    
    
    response['watchlist'] = watchlist
    
    return jsonify(response)

@app.route('/api/get-seenlist')
def get_seenlist():
    """returns json object with list of movie.id's from g.user.seenlist or empty dict"""
    response = dict()
    seenlist = list()
    response['user'] = False
    if g.user:
        response['user'] = True
        for movie in g.user.seenlist:
            seenlist.append(movie.id)
    
    response['seenlist'] = seenlist
    
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

@app.route('/edit-user', methods=['GET', 'POST'])
def edit_user():
    if g.user:
        form = EditProfileForm(obj=g.user)

        if form.validate_on_submit():
            curr_user = User.authenticate(g.user.username, form.confirm_password.data)
            if curr_user:
                curr_user.username = form.username.data
                curr_user.email = form.email.data
                curr_user.bio = form.bio.data
                if form.img_url.data:
                    curr_user.img_url = form.img_url.data
                else:
                    curr_user.img_url = 'https://static-00.iconduck.com/assets.00/avatar-default-symbolic-icon-1920x2048-qj0yfpqi.png'
                
                db.session.commit()
                flash('Profile updated')
                return redirect(f'/users/{curr_user.id}')
            flash('Incorrect Password')
            return redirect('/edit-user')
        
        return render_template('edit-profile.html', form=form)

    else:
        flash('Must be logged in to do that!')
        return redirect('/login')

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

@app.route('/')
def show_home():
    if g.user:
        follows = list()
        for person in g.user.follows:
            follows.append(str(person.id))
        release_radar = get_new_movies(follows,1)
        convert_date(release_radar, 'release_date')
        old_movies = get_old_movies(follows,1)
        convert_date(old_movies, 'release_date')
        return render_template('following-home.html', release_radar=release_radar, old_movies=old_movies, followlist=g.user.follows)
    else:
        trending_m = get_trending_movies()
        trending_p = get_trending_people()
        theatres = get_now_showing(1)
        convert_date(trending_m, 'release_date')
        convert_date(theatres, 'release_date')
        return render_template('landing-page.html', trending_m=trending_m, trending_p=trending_p, theatres=theatres)
    
@app.route('/search')
def show_search_results():
    term = request.args.get('q','').strip()
    
    if not term:
        return render_template('search-results.html', results=None, type1=None)
    
    results = None
    type1 = first_result_type(term)
    if type1 == 'movie':
        results = movie_search(term, 1)
        convert_date(results, 'release_date')
    if type1 == 'person':
        results = person_search(term, 1)
    if type1 == 'user':
        results = user_search(term)
        if results['total_results'] == 0:
            type1 = None
    return render_template('search-results.html', results = results, type1=type1)

@app.route('/trending-movies')
def show_trending_movies():
    response = get_trending_movies()
    convert_date(response, 'release_date')
    movies = response['results']
    return render_template('trending-movies-home.html', movies=movies)

@app.route('/trending-people')
def show_trending_people():
    response = get_trending_people()
    people = response['results']
    return render_template('trending-people-home.html', people=people)

@app.route('/in-theatres')
def show_in_theatres():
    response = get_now_showing(1)
    convert_date(response, 'release_date')
    movies = response['results']
    return render_template('now-showing-home.html', movies=movies)

# user routes

@app.route('/users/<int:id>')
def show_user(id):
    user = User.query.get_or_404(id)
    return render_template('user.html', user=user)

# movie routes

@app.route('/movies/<int:id>')
def show_movie(id):
    movie = movie_fetch(id)
    if movie['release_date'] != '':
        adate = movie['release_date']
        newdate = datetime.datetime.strptime(adate, '%Y-%m-%d').strftime('%b %d, %Y')
        movie['formatted_date'] = newdate
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