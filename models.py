"""SQLAlchemy models for Flixxly"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import UniqueConstraint

bcrypt = Bcrypt()
db = SQLAlchemy()

class Follow(db.Model):
    """Table showing user ids and person ids which are pulled from the tmdb API representing people being followed by a user"""

    __tablename__='follows'

    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'person_id'),)

class Watchlist(db.Model):
    """Table showing user ids and movie ids which are pulled from the tmdb API representing movies on a user's watchlist"""

    __tablename__ = 'watchlist'

    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    date_added = db.Column(db.DateTime, server_default=db.func.now())

    __table_args__ = (UniqueConstraint('user_id', 'movie_id'),)

class Seenlist(db.Model):
    """Table showing user ids and movie ids which are pulled from the tmdb API representing movies on a user's seenlist"""

    __tablename__ = 'seenlist'

    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    date_added = db.Column(db.DateTime, server_default=db.func.now())

    __table_args__ = (UniqueConstraint('user_id', 'movie_id'),)

class User(db.Model):
    """User Model. Tracks past games."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    bio = db.Column(db.String(100), nullable=True)
    img_url = db.Column(db.String, default='https://static-00.iconduck.com/assets.00/avatar-default-symbolic-icon-1920x2048-qj0yfpqi.png')

    follows = db.relationship('Person', secondary='follows', backref='followers')
    watchlist = db.relationship('Movie', secondary='watchlist', backref='users_watching')
    seenlist = db.relationship('Movie', secondary='seenlist', backref='users_seen')

    def is_following(self, person_id):
        """Is this user following a person?"""

        found_person_list = [person.id for person in self.follows if person.id == person_id]
        return bool(len(found_person_list) == 1)

    def is_watching(self, movie_id):
        """Is this movie on a user's watchlist?"""

        found_movie_list = [movie.id for movie in self.watchlist if movie.id == movie_id]
        return bool(len(found_movie_list) == 1)

    def has_seen(self, movie_id):
        """Is this movie on a user's seenlist?"""

        found_movie_list = [movie.id for movie in self.seenlist if movie.id == movie_id]
        return bool(len(found_movie_list) == 1)

    @classmethod
    def signup(cls, username, password, email):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Movie(db.Model):
    """Table with very basic info about a movie from the tmdb API. Just enough to populate the user page."""

    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    release_year = db.Column(db.Integer, nullable=True)
    overview = db.Column(db.String, default='No overview available at this time.')

class Person(db.Model):
    """Table with very basic info about a person from the tmdb API. Just enough to populate the user page."""

    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=True)
    known_for = db.Column(db.String, nullable=False)

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)