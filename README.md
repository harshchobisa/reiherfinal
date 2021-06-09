# CS M148 Final Project

## Context
In this project we provide a user-facing interface for an organization such as MentorSEAS. Users can onboard themselves onto the platform to be matched in the future. An admin user can then programatically match mentors and mentees using a proprietary algorithm based on K-means clustering to ensure high-quality pairings. Users are then able to view their own pairings and establish relationships with their family. 

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
- we deloyed the app using AWS Elastic Beanstalk
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html
- AWS Certificate Manager allows for configuration of SSL/TLS certificates on Elastic Load Balancer to ensure secure HTTPS connection
https://aws.amazon.com/certificate-manager/

- domain:  env-10.eba-3jpwws2e.us-west-2.elasticbeanstalk.com (currently down to save costs)
- had to buy new domain to configure SSL, no encryption on locallhost version

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
