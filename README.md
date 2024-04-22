# Flixxly

Flixxly is an onlline movie database that tracks a user's movie watching history and their interests that uses the TMDB API. The app server is built with Python using the Flask framework as a capstone project for my coding bootcamp.

## Features

The key feature that set Flixxly apart is the ability to follow actors, directors, producers or any other people that are involved in the production of a movie. Users are then able to see future movies that credit the people they follow on their Release Radar.

Additionally, users are able to keep track of movies they have seen (Seenlist) and/or movies they have been meaning to watch (Watchlist). Users can use the searchbar to find more people/movies/users to discover more things they might be interested in.

## How to set up the app

### Required technologies

- Python version 3.10.12
  - Venv module
- PostgreSQL 14.11
- TMDB API access and API Read Access Token

### Instructions

1. Go into your terminal and clone this repo down to your local machine:

    ```
    git clone https://github.com/user-owang/flixxly.git
    ```

(DELETE ME: Are we missing steps here?)

2. Create a psql database.

    ```
    createdb flixxly
    ```

3. cd into the project folder

    ```
    cd <INSERT_PROJECT_FOLDER_PATH>
    ```

4. Create virtual environment

    ```
    python3 -m venv venv
    ```

5. Activate your venv

  - For Mac/Linux:

    ```
    source venv/bin/activate
    ```

  - For Windows:

    ```
    source venv/Scripts/activate
    ```

6. Install the project dependencies

    ```
    pip install -r requirements.txt
    ```

7. Create a file named `.env` at the root folder

8. In the `.env` file, define your secret key, your TMDB API Read Access Token and your database URI as SECRET_KEY, READ_TOKEN and DATABASE_URI respectively. It should look like:

    ```
    SECRET_KEY=<INSERT_SECRET_KEY_HERE>
    READ_TOKEN=<INSERT_TMDB_READ_TOKEN_HERE>
    DATABASE_URI=<INSERT_DB_URI_HERE>
    ```

9. Launch the app locally

    ```
    flask run
    ```

## Future Roadmap

### Additional Features

- Flesh out account creation/editing

  - add email verification
  - allow users to change passwords
  - allow users to delete accounts

- Add the ability to friend request other users
  - Add the ability to see Watchlist movies in common with friends
  - Invite friends to set a date to watch a movie together

### Bug fixes/known issues

- Send add/remove post requests via forms using JS and Axios requests instead of form post requests with a redirect.
- Refactor some helper functions in app.py into a separate file.
