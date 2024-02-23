from flask_sqlalchemy import SQLAlchemy
# Because we have an init file, we can import variable
# using a folder name, it will automatically go to the
# init file to search for the variable that we've called
from movies import db, app

class Movies(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    title =db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer(), nullable=False )
    description = db.Column(db.String(255), nullable =False)
    rating = db.Column(db.Float(4),nullable = False)
    ranking =db.Column(db.Integer(), nullable=True)
    review = db.Column(db.Text(), nullable =True)
    img_url = db.Column(db.String(255), nullable=False, default="static/res/img/movies/default.jpg")

    def __repr__(self):
        return f"Movies('{self.title}','{self.year}','{self.description}','{self.rating}','{self.ranking}','{self.review}','{self.img_url}')"
#
# class User(db.Model):
#     pass