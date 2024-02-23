from flask import  render_template, url_for, flash, redirect, session
from movies import app

from movies.controller import Movies_Controller
from movies.forms import UpdateForm, MoviesForm, MoviesFormWebsite

movies_controller = Movies_Controller()
transport_movie = None

@app.route("/home")
@app.route("/")
def home():
    movies = movies_controller.get_movies_data()
    return render_template("index.html", movies_data = movies)
    # return render_template("index.html")

@app.route("/update/<movie_id>/<movie_title>", methods=["POST","GET"])
def update_rating_review(movie_id, movie_title):
    upload_form = UpdateForm()
    print(f"{movie_id}|{movie_title}")
    if upload_form.validate_on_submit():
        print(f"{movie_id}|{movie_title}")
        movies_controller.update_movie_data(id = movie_id, rating = upload_form.rating.data, review = upload_form.review.data)
        return redirect("/home")
    return render_template("edit.html", form = upload_form, movie_id = movie_id, movie_title=movie_title)

@app.route("/delete/<movie_id>", methods=["POST","GET"])
def delete_movie(movie_id):
    print(movie_id)
    movies_controller.delete_movie(movie_id)
    return redirect("/home")

@app.route("/add",methods=["POST","GET"])
def add_movie():
    add_movie_form = MoviesForm()
    if add_movie_form.validate_on_submit():
        # print(add_movie_form.title.data)
        movies_controller.add_movie(add_movie_form)
        return redirect("/home")
    return render_template("add.html", form = add_movie_form)

@app.route("/select", methods=["POST","GET"])
def select_to_add_movie():
    global transport_movie
    movie_list = transport_movie
    return render_template("select.html", movie_data=movie_list)

@app.route("/addfromwebsite", methods=["POST","GET"])
def add_movie_from_web():
    global transport_movie
    add_movie_form_web = MoviesFormWebsite()
    if add_movie_form_web.validate_on_submit():
        movie_title = add_movie_form_web.title.data
        transport_movie=movies_controller.add_movie_from_web(movie_title)
        return redirect("/select")
    return render_template("add_from_web.html", form = add_movie_form_web)

@app.route("/select/movie/<id>", methods=["POST","GET"])
def add_selected_movie(id):
    # Temporary Route to add movie from web into a db
    # and to call the update function to update some of its info
    global transport_movie
    movie = transport_movie[len(id)]
    movies_controller.add_movie_from_web_to_database(movie)
    return redirect("/home")
