# Calibretto

## What is it?
Calibretto allows you to choose keywords to track on Twitter and store associated tweets in your database.

## Prerequisites
To get the ball rolling, you’ll need:
- Python (Built using 2.7.6)
- A [PostgreSQL](http://www.postgresql.org) database (or, you can adapt to use what you’d like)
- A registered [Twitter App](https://apps.twitter.com)
- A few Python modules: [Twitter](https://pypi.python.org/pypi/twitter) and [psycopg2](http://initd.org/psycopg/) (if you’re using PostgreSQL)

## Getting started
1. *Create database tables*: Run each section of `database_setup.sql` to create the tables you need.
2. *Enter credentials*: I’ve dropped placeholders in for your Twitter and PostgreSQL credentials. You can find these in `{}`s on lines 10-13 (PostgreSQL) and line 20 (Twitter) of `calibretto.py`.
3. *Choose keywords*: Placeholders for keywords are in `{}`s on line 24 of `calibretto.py`. Add as many or as few as you’d like.
3. *Run the script*: Give her a whirl, `python ~/calibretto.py`. A summary will print out for all tweets added.
4. *Run, run, run*: Create a rake task to run this guy as often as you need to. Each run should request 100 tweets.

## Notes
- You can further refine yoru search by updating line 43 of `calibretto.py` with additional search parameters (see: [Twitter \> GET search/tweets](https://dev.twitter.com/rest/reference/get/search/tweets))

## Acknowledgements
- Much love to [Ryan Robitalle](http://ryrobes.com), whose Metallicanalysis was the basis for this project.
- [Matt Fulton](https://github.com/mful) for inspiration to get this thing done!