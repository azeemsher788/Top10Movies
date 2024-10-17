from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Column
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os, dotenv

dotenv.load_dotenv()

# Please Add your values in .env file
API_TOKEN = os.getenv("MOVIE_DB_TOKEN")
MOVIE_DB_SEARCH_URL = os.getenv("MOVIE_DB_SEARCH_URL")
MOVIE_DB_INFO_URL = os.getenv("MOVIE_DB_INFO_URL")
MOVIE_DB_IMAGE_URL = os.getenv("MOVIE_DB_IMAGE_URL")

# CREATE DB
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db.init_app(app)
Bootstrap5(app)

# CREATE TABLE
class Movies(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(1000), nullable=True)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)

    def __repr__(self):
        return f'<movie {self.title}>'


with app.app_context():
    db.create_all()


class EditingForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5", validators=[DataRequired()])
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Submit")

class AddingForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Search")

@app.route("/")
def home():
    movies = db.session.execute(db.select(Movies).order_by(Movies.rating))
    all_movies = movies.scalars().all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", all_movies=all_movies)

@app.route("/edit", methods=["POST", "GET"])
def edit():
    form = EditingForm()
    movie_id = request.args.get("movie_id")
    movie = db.get_or_404(Movies, movie_id)
    if form.validate_on_submit():
        movie.rating = float(request.form.get("rating"))
        movie.review = request.form.get("review")
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", movie=movie, form=form)


@app.route("/delete", methods=["POST", "GET"])
def delete():
    movie_id = request.args.get("movie_id")
    movie_to_delete = db.get_or_404(Movies, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


data = []
@app.route('/search', methods=["POST", "GET"])
def search():
    form = AddingForm()
    if form.validate_on_submit():
        movie_name = request.form.get("name")
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {API_TOKEN}"
        }
        params = {
            "query": f"{movie_name}",
        }
        data = requests.get(url=MOVIE_DB_SEARCH_URL, headers=headers, params=params).json()["results"]
        return render_template("select.html", searched_movies=data, enumerate=enumerate)
    return render_template('add.html', form=form)

@app.route('/add')
def add():
    id = int(request.args.get("id"))
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    movie_detail = requests.get(f"{MOVIE_DB_INFO_URL}/{id}", headers=headers).json()
    new_movie = Movies(
        title=movie_detail["title"],
        year=movie_detail["release_date"].split("-")[0],
        description=movie_detail["overview"],
        img_url=f"{MOVIE_DB_IMAGE_URL}/{movie_detail['poster_path']}"
    )
    db.session.add(new_movie)
    db.session.commit()
    # return redirect(url_for("home"))
    return redirect(url_for('edit', movie_id=new_movie.id))
# s = {'adult': False, 'backdrop_path': None, 'belongs_to_collection': None, 'budget': 0, 'genres': [{'id': 35, 'name': 'Comedy'}], 'homepage': '', 'id': 411732, 'imdb_id': 'tt0033146', 'origin_country': ['US'], 'original_language': 'en', 'original_title': 'That Inferior Feeling', 'overview': 'Joe Doakes, like most men, is unable to cope with personal emergencies or those in a position of authority (real or imagined).', 'popularity': 1.096, 'poster_path': '/2FSjKy3yoRdA4HZjRaxeutY0vRn.jpg', 'production_companies': [{'id': 21, 'logo_path': '/usUnaYV6hQnlVAXP6r4HwrlLFPG.png', 'name': 'Metro-Goldwyn-Mayer', 'origin_country': 'US'}], 'production_countries': [{'iso_3166_1': 'US', 'name': 'United States of America'}], 'release_date': '1940-01-20', 'revenue': 0, 'runtime': 9, 'spoken_languages': [{'english_name': 'English', 'iso_639_1': 'en', 'name': 'English'}], 'status': 'Released', 'tagline': '', 'title': 'That Inferior Feeling', 'video': False, 'vote_average': 5.4, 'vote_count': 5}

if __name__ == '__main__':
    app.run(debug=True, port=8000)
