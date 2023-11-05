# gsb-ticketing

Django-powered web application for the 2023 Girton Spring Ball Ticketing platform.

## Development

1. Create a virtual environment: `python3 -m venv .venv`
2. Activate the environment: `. .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Install development dependencies: `pip install -r dev_requirements.txt`
5. Set up pre-commit: `pre-commit install`
6. Source required variables: `. app/dev.sh`
7. Install fixtures (make sure to load user_kind last as it has foreign key dependencies on all the other fixtures) `./import_fixtures.sh`
8. Run local development server: `python3 manage.py runserver`

### Starting out

1. Any `manage.py` command should automatically create the SQLite database.
2. Import seed data: `python manage.py loaddata ticketing/fixtures/*`
3. Migrate the database: `python manage.py migrate`

### Main dependencies

- Django
- ucamwebauth (custom fork, needs to be manually installed with `python setup.py install`)

## Lookup requests

Lookup requests are forwarded from a simple CGI script hosted inside the University.

We want to change this to something better - ideally carrying out the lookup request a proper API call with the appropriate credentials. Need to talk to university to see if these credentials can be issued for the spring ball platform. 


- Move to `public_html`
- Set appropriate permissions

## Production

Because of Reasons, we are using Heroku for deployment.

Changes to make:

1. Set the right env vars: django_settings_module, secret_key
2. Push: `git subtree push --prefix app heroku master` or ` git push heroku ``git subtree split --prefix app master``:master --force ` if you need to get yourself out of a pickle
3. Set yourself as superuser and staff via psql
4. Clean up any migrations, shortcuts: `heroku run bash` or `heroku psql`
5. Set the right promocode, change the wave, etc
6. Push instance to AWS Lambda and migrate PostGRESQL. Verify function
7. Liase and obtain any other fields that need to be added to the purchase form
8. Meet with Kim Pearson and Vicky about alumni tickets 
9. Ask Krish how alumni tickets were done and start actioning
10.  

## Ticket scanning

A custom scanner web app is used to scan tickets. A stripped out database is hosted on another Heroku instance.

To prepare the database, run the setup script to clean a fresh copy of the DB on a local machine then:

```
heroku pg:push gsb23_tickets DATABASE_URL --app gsb-scanner
```

## girtifier

Verifies that a list of Cambridge emails meet these requirements: current student + current member of Girton College.

Usage: `python3 girtifier.py -h` to find out.

## Resources

- [Single app project](https://zindilis.com/posts/django-anatomy-for-single-app/)
- [Useful prod setup](https://www.oreilly.com/library/view/lightweight-django/9781491946275/ch01.html)

### scanner

Web-based QR code scanner for ticket check-in.

## License

MIT

## Credits

Matias Silva 2022   
