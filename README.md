# Flixxly

Flixxly is an onlline movie database that tracks a user's movie watching history and their interests that uses the TMDB API. The app server is built with Python using the Flask framework as a capstone project for my coding bootcamp.

## Features

The key feature that set Flixxly apart is the ability to follow actors, directors, producers or any other people that are involved in the production of a movie. Users are then able to see future movies that credit the people they follow on their Release Radar.

Additionally, users are able to keep track of movies they have seen (Seenlist) and/or movies they have been meaning to watch (Watchlist). Users can use the searchbar to find more people/movies/users to discover more things they might be interested in.

## How to set up the app

To use the functionality provided by the TMDB API, you will need to register for an account with them and apply for an API key. More info can be found here: https://developer.themoviedb.org/docs/faq
Additionally, I am using Flask SQLAlchemy to manage database queries. You will need to set up a database (I used PostgreSQL).
Lastly you will need to set up an additional file named secret.py. In it you should define the read token provided by the TMDB API as READ_TOKEN, a secret key defined as SECRET_KEY, and the database URI defined as DATABASE_URI.

## Future Roadmap

### Additional Features
- Add the ability to friend request other users
  - Add the ability to see Watchlist movies in common with friends
  - Invite friends to set a date to watch a movie together

### Bug fixes/improvements
- Send add/remove post requests via forms using JS and Axios requests instead of form post requests with a redirect.
- Refactor some helper functions in app.py into a separate file.
