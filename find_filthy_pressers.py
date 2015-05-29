import logging
import argparse
import time
import praw


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
            print s.id
            print s.score
            print s.created_utc
            print s.url.encode('utf-8') if s.url else None
            print s.title.encode('utf-8') if s.title else None
            print s.author_flair_text.encode('utf-8') if s.author_flair_text else None
            print s.selftext.encode('utf-8')
            # To make parsing using awk simpler
            print "====END_OF_RECORD===="

            # submission.replace_more_comments(limit=None)
            # for c in submission.comments:
            # TODO: use regex here
            #    if 'filthy presser' in c.body or "Filthy presser" in c.body:
            #        print c.id, (c.permalink if 'permalink' in dir(c) else None), c.body, c.author_flair_text

        cts2 = cts1
        cts1 = cts2 - current_ts_interval

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
