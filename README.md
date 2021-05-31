# reiherfinal

## Context

## Architecture
- Python/Django backend
    - `urls.py` defines the endpoints
    - `views.py` contains the functions that the endpoints run
    - `/matching/` contains matching logic
- Javascript/React frontend
    - `/frontend/src/App.js` is the main page of the app with the frontend routes
    - `/frontend/src/Pages/` defines the components of each page
    
## Usage

### Rebuilding the app
- we deploy a static build of the app from Django
- run the following script
```python
cd frontend && yarn build && cd .. && mv frontend/build/index.html templates && python3 manage.py collectstatic --clear
python3 manage.py runserver
```

### Deploying the app
- TODO

## Features

### As a normal user
- create account
- login
- fill out profile
- view family matching

### As an admin user
- *note: hit special create admin user endpoint instead of using UI*
- login
- create bulk users
- run pairings
- delete all users