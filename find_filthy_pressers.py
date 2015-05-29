import logging
import argparse
import time
import praw
from app import Submission, db
from datetime import datetime


# Downloads all the self posts from given subreddit
def find_filthy_pressers(ts_interval, largest_timestamp):
    r = praw.Reddit(user_agent='filthypresser project 0.1 by /u/godlikesme')
    if largest_timestamp is None:
        largest_timestamp = int(time.time()) + 12*3600
    cts2 = largest_timestamp
    cts1 = largest_timestamp - ts_interval
    current_ts_interval = ts_interval
    while True:
        try:
            search_results = list(r.search('timestamp:{}..{}'.format(cts1, cts2), subreddit='thebutton', syntax='cloudsearch'))
        except Exception as e:
            logging.exception(e)
            continue

        logging.info("Got {} submissions in interval {}..{}".format(len(search_results), cts1, cts2))
        if len(search_results) == 25:
            current_ts_interval /= 2
            cts1 = cts2 - current_ts_interval
            logging.debug("Reducing ts interval to {}".format(current_ts_interval))
            continue

        for s in search_results:
            # FIXME check url length etc
            try:
                if Submission.query.filter_by(submission_id=s.id).first() is not None:
                    continue
                dbs = Submission(submission_id=s.id,
                                 score=s.score,
                                 permalink=s.permalink,
                                 created_utc=datetime.utcfromtimestamp(s.created_utc),
                                 url=s.url,
                                 title=s.title,
                                 author_flair_text=s.author_flair_text,
                                 selftext=s.selftext)

                db.session.add(dbs)
            except Exception as e:
                logging.exception(e)
                db.session.rollback()

            # submission.replace_more_comments(limit=None)
            # for c in submission.comments:
            # TODO: use regex here
            #    if 'filthy presser' in c.body or "Filthy presser" in c.body:
            #        print c.id, (c.permalink if 'permalink' in dir(c) else None), c.body, c.author_flair_text

        cts2 = cts1
        cts1 = cts2 - current_ts_interval
        try:
            db.session.commit()
        except Exception as e:
            logging.exception(e)
            db.session.rollback()

        if cts1 < 0:
            break

        if len(search_results) <= 7:
            current_ts_interval *= 2
            logging.debug("Increasing ts interval to {}".format(current_ts_interval))


def main():
    logging.getLogger().setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description='filthy presser app/bot')
    parser.add_argument("--timestamp_interval", dest="timestamp_interval", type=int, required=True)
    parser.add_argument("--largest_timestamp", dest="largest_timestamp", type=int, required=False, default=None)
    args = parser.parse_args()

    find_filthy_pressers(args.timestamp_interval, args.largest_timestamp)

if __name__ == "__main__":
    main()
