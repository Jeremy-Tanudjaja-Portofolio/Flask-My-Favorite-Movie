from movies.movies_db import Movies, db, app  # , User
from flask_uploads import configure_uploads, IMAGES, UploadSet
import os, requests

class Movies_Controller():
    def __init__(self):
        pass

    def get_movies_data(self):
        """Query Top 10 Movie Data with descending order """
        return Movies.query.order_by(Movies.rating.desc()).limit(10).all()

    def update_movie_data(self, id, rating, review):
        """Function to Update SQLite Movie rating and review data"""
        # Cast ID into int because id column in DB is in INT
        id_int = int(id)

        # Grabs the Corresponding Movie Row Data based on ID
        update_movie = Movies.query.get(id_int)

        # Check if data is empty or not
        if review is not None or review == "":
            # Update the Data
            update_movie.review = review
        if rating is not None or rating == "":
            # Cast the rating into a float because DB Column type is Real Number(eg: floats)  from a String
            rating = float(rating)
            # Update the Data
            update_movie.rating = rating
        # Commit the change, this will finally update the row data
        db.session.commit()

    def add_movie_from_web(self, form_data):
        """This will take a title string from a form and use request.get to call
        The Movie Database Website API. The API will return us a JSON data with
        which we can use the information to add to our database. it will also
        make an API call to the same website to get the poster picture using
        JSON that we got from the previous get request"""
        print(form_data)
        API_KEY_AUTH3 = '9011c3574c6ada256ec6846520258f5e'
        url = "https://api.themoviedb.org/3/search/movie"
        param = {
            "api_key": API_KEY_AUTH3,
            "query": form_data
        }
        movie_list = []
        with requests.get(url, params=param) as connection:
            if connection.status_code != 200:
                connection.raise_for_status()
            movies = connection.json()["results"]

            for counter in range(0,len(movies)):
                try:
                    movie_info = {"id": counter, "title": movies[counter]['title'], "release_date": movies[counter]['release_date'],
                            "description": movies[counter]['overview'], "rating": movies[counter]['vote_average'],
                            "image_path": f'https://image.tmdb.org/t/p/w500{movies[counter]["poster_path"]}'}
                except KeyError:
                    movie_info["release_date"] = "2000-01-01"
                    print("There is a key error")
                finally:
                    movie_list.append(movie_info)
        print(movie_list)
        return movie_list

    def add_movie_from_web_to_database(self,data):

        # We grab the filename and add the relative path to save to our database
        # the path is seen from the perspective of the html file
        print(data['title'])
        movie = Movies(title=data['title'], year=data['release_date'], description=data['description'],
                       rating=data['rating'], review="", img_url=data['image_path'])
        db.session.add(movie)
        db.session.commit()

    def add_movie(self, form_data):
        """Upload an Image from WTForms, also adds the path and other field from
        WTForms to the database"""
        # Configure Image Upload, we use app.config['UPLOADED_IMAGES_DEST'] to set the upload
        # path, UploadSet to tell the computer what we are going to upload, then we configure it
        # using configure_uploads
        app.config['UPLOADED_PHOTOS_DEST'] = 'movies/static/res/img/movies'
        images = UploadSet('photos', IMAGES)
        configure_uploads(app, images)

        # images.save will take an Image Object and save it to the destination set by
        # app.config. This function also returns the filename
        filename = images.save(form_data.img_url.data)

        # We grab the filename and add the relative path to save to our database
        # the path is seen from the perspective of the html file
        picture_path = f"../static/res/img/movies/{filename}"
        print(form_data.title.data)
        print(picture_path)
        movie = Movies(title=form_data.title.data, year=form_data.year.data, description=form_data.description.data,
                       rating=form_data.rating.data, review=form_data.review.data, img_url=picture_path)
        db.session.add(movie)
        db.session.commit()

    def delete_movie(self, id):
        delete_movie = Movies.query.get(id)

        # The path is seen from the perspective of the main.py file
        # thus we need to update the image url
        movie_name = delete_movie.img_url
        movie_delete_path = f"movies/static/res/img/movies/{movie_name.split('/')[-1]}"
        print(movie_delete_path)
        # Deletes the Movie Picture from the File
        if os.path.exists(movie_delete_path):
            os.remove(movie_delete_path)
        else:
            print("The file does not exist")

        db.session.delete(delete_movie)
        db.session.commit()
