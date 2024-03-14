<h1>Revou task by <bold>Dewa Surya Ariesta

## Requirement to run the project

### please set up the environment variable first

```bash
FLASK_DEBUG=True  // optional
USER_NAME= ..
PASSWORD= ..
SERVER=  ..
DB_NAME= ..

```

## How to set_up transaction API

1. set_up Environment - `poetry config virtualenvs.in-project true` // use to make the '.env' on the repo
2. Install all Dependency - `poetry install`
3. set up the environment `poetry shell`
4. run the app -`poetry run flask run`

## To see the swagger ui Document

- in locale `http://127.0.0.1:5000/swagger-ui`
- in production `<YOUR_URL>/swagger-ui`

## data base set up

```bash
//comment to set_up the data base
poetry run flask db

// comment to generate migration to set_up data base
poetry run flask db migrate

// comment to get ready your data base
poetry run flask db upgrade

// comment if you are lazy
poetry run flask db migrate && poetry run flask db upgrade

```

## Folder structure

```bash
.env
README.md
app
   |-- __init__.py
   |-- transaction_api
   |   |-- __init__.py
   |   |-- model
   |   |   |-- __init__.py
   |   |   |-- __pycache__
   |   |   |-- account.py
   |   |   |-- account_type.py
   |   |   |-- bills.py
   |   |   |-- budgets.py
   |   |   |-- transaction.py
   |   |   |-- transaction_categories.py
   |   |   |-- user.py
   |   |-- schemas
   |   |   |-- account.py
   |   |   |-- bills.py
   |   |   |-- budgets.py
   |   |   |-- category.py
   |   |   |-- transaction.py
   |   |   |-- user.py
   |   |-- service
   |   |   |-- DbModelService.py
   |   |   |-- ModelMatcher.py
   |   |   |-- __init__.py
   |   |-- util
   |   |   |-- JWTGetters.py
   |   |   |-- db.py
   |   |   |-- sql_phat.py
   |   |-- views
   |   |   |-- account.py
   |   |   |-- bills.py
   |   |   |-- budgets.py
   |   |   |-- transaction.py
   |   |   |-- user.py
data
   |-- milestone_2_account.sql
   |-- milestone_2_account_type.sql
   |-- milestone_2_alembic_version.sql
   |-- milestone_2_bill.sql
   |-- milestone_2_budget.sql
   |-- milestone_2_transaction.sql
   |-- milestone_2_transaction_category.sql
   |-- milestone_2_user.sql
migrations
poetry.lock
pyproject.toml
tests
   |-- __init__.py
   |-- data.db
   |-- views
   |   |-- ModelTestBase.py
   |   |-- __init__.py
   |   |-- test_account.py
   |   |-- test_user.py
```
