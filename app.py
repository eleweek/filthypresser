from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
Bootstrap(app)
db = SQLAlchemy(app)


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


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


@app.route("/all_submissions/<int:page>")
@app.route("/all_submissions", defaults={'page': 1})
def all_submissions(page):
    submissions = Submission.query.order_by(Submission.id).paginate(page=page, per_page=20)
    return render_template("index.html", submissions_count=Submission.query.count(), submissions=submissions)


@app.route("/filthy_pressers/<int:page>")
@app.route("/filthy_pressers", defaults={'page': 1})
def filthy_pressers(page):
    regex = '(filth(y)?[ ]*presser)|(follow(er)?[ ]*(of)?[ ]*(the)?[ ]*shade)|(non-?[ ]*presser[*]forever)|(gr[ea]y[ ]*forever)'
    submissions = Submission.query.filter(or_(Submission.author_flair_text != 'non presser',
                                              Submission.author_flair_text != "can't press",
                                              Submission.author_flair_text != None))\
                                  .filter(or_(Submission.selftext.op("~")(regex),
                                              Submission.title.op("~")(regex)))\
                                  .order_by(Submission.id.desc()).paginate(page=page, per_page=20)  # NOQA

    return render_template("index.html", submissions_count=Submission.query.count(), submissions=submissions)


@app.route("/")
def index():
    return redirect(url_for("filthy_pressers"))

if __name__ == "__main__":
    app.run(debug=True)
