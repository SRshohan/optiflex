# Making Sure of LiteLLM works properly and able to fetch all the models
Python has a "backpack" (Not a literal Term). What it basically does is, it can have attachment like other classes or functions and I can have other
other stuff with it


1. Prepare Environment 
Go to the directory:
```sh
cd open-webui/backend
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

2. Sync
If database is already exists. Need to tell Alembic that the DB is current so it doesnt  try to recreate existing tbales: 
```sh
alembic -c open-webui/alembic.ini stamp head
```

3. Create a Migration (When you change Models)
Whenever modify happen in `model/*.py` (e.g add a column or table):
- Edit the python Model files
- Generating the Migration scripts
```sh
alembic -c open_webui/alembic.ini revision --autogenerate -m "describe your change"
```
4. Apply the migration
To update the database schema to match new models:
```sh
alembic -c open_webui/alembic.ini upgrade head
```

