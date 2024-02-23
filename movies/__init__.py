# __init__.py acts as an initiator to the
# movies folder, we design the folder this way
# to combat circular imports because we want
# to divide the movies model into a separate python
# file

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies-database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret_key"
Bootstrap(app)


db=SQLAlchemy(app)

# # Initial Test Data to test db connection
# from movies.movies_db import Movies
# movie = Movies(id = 1,
#                title="Phone Booth",
#                year="2002",
#                description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#                rating=7.3,
#                ranking=10,
#                review="My favourite character was the caller.",
#                img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# db.session.add(movie)
# db.session.commit()

# To Init the Database
db.create_all()

# We put the routes import here so that routes
# will import app when app and database has already been created
# if it is initialized before the database, it will throw us an error
from movies import routes