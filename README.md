# Calibretto

## What is it?
Calibretto allows you to choose keywords to track on Twitter and store associated tweets in your database.

## Prerequisites
To get the ball rolling, you’ll need:
- Python 3.x
- A [PostgreSQL](http://www.postgresql.org) database (or, you can adapt to use what you’d like)
- A registered [Twitter App](https://apps.twitter.com)
- A few Python modules: [Twitter](https://pypi.python.org/pypi/twitter) and [peewee](https://pypi.python.org/pypi/peewee/) (if you’re using PostgreSQL)

## Getting started
1. **Create database tables**: Run both sections of `database_setup.sql` to create the tables you need.
2. **Enter credentials**: I’ve dropped placeholders in for your Twitter and PostgreSQL credentials. You can find these in `{}`s on lines 12-15 (Twitter) and lines 28-32 (PostgreSQL) of `calibretto.py`.
3. **Choose keywords**: Placeholders for keywords are in `{}`s on line 36 of `calibretto.py`. Add as many or as few as you’d like.
3. **Run the script**: Give her a whirl, `python ~/calibretto.py`. A summary will print out for all tweets added.
4. **Run, run, run**: Create a rake task to run this guy as often as you need to. Each run should request 100 tweets but beware: [Twitter limits](https://dev.twitter.com/rest/public/rate-limits) each app to 450 request per 15 minute window.

## Notes
- You can further refine your search by updating line 83 of `calibretto.py` with additional search parameters (see: [Twitter \> GET search/tweets](https://dev.twitter.com/rest/reference/get/search/tweets))

## Acknowledgements
- Much love to [Ryan Robitaille](http://ryrobes.com), whose Metallicanalysis was the basis for this project.
- [Charles Leifer](https://github.com/coleifer) and team for their amazing work on [peewee](https://github.com/coleifer/peewee).
- [Matt Fulton](https://github.com/mful) for inspiration to get this thing done!
