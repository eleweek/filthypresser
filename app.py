from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
Bootstrap(app)
db = SQLAlchemy(app)


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.String(32), unique=True)
    permalink = db.Column(db.String(1024))
    url = db.Column(db.String(1024))
    score = db.Column(db.Integer)
    title = db.Column(db.String(1024))
    author_flair_text = db.Column(db.String(1024))
    selftext = db.Column(db.Text())
    created_utc = db.Column(db.DateTime())


@app.route("/")
def hello():
    return render_template("index.html", submissions_count=Submission.query.count())

if __name__ == "__main__":
    app.run(debug=True)
