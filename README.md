# CranioQ Backend
Backend code for the CranioQ questionnaire application.

# Dependencies
## Python Modules
To install all required modules run 
`python -m pip install -r requirements.txt`

## Further Dependencies
The application uses a `PostegreSQL` database.

### Setting up the PostgreSQL Database
Start by installing postgres. If on Mac you can use homebrew: `brew install postgresql`.

Next connect to the database using `psql`. Now create a new database: `CREATE DATABASE cranioq_db;`.
We also need to create a new user, grant him permissions and set some standard parameters for him:
- `CREATE USER cranioq_django WITH PASSWORD 'cranioq_django';`
- `ALTER ROLE cranioq_django  SET client_encoding TO 'utf8';`
- `ALTER ROLE cranioq_django SET default_transaction_isolation TO 'read committed';`
- `ALTER ROLE cranioq_django SET timezone TO 'UTC';`
- `GRANT ALL PRIVILEGES ON DATABASE cranioq_db TO cranioq_django;`

Note that you can choose your own name for the database and your own credentials for the user, just make sure to modify the `pg_settings.py` file.

### Setting up Django to work with PostgreSQL
In the `cranioq_back module` (where the `settings.py` file is located) create a file called `pg_settings.py`. 
In this file add the following code:
```
dev_database = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DATABASE_NAME',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'USER': 'USER',
        'PASSWORD': 'PASSWORD'
    }
}
```

Make sure you installed the `psycopg2` Python package and run the Django database migrations after setting up everything:
`python manage.py migrate`