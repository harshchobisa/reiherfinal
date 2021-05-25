# reiherfinal

## Usage

### Frontend
- navigate to "/frontend"
- run `npm install` to resolve all dependencies
- run `yarn start` to initiate the app
- page should render at http://localhost:3000

### Backend
```python
cd frontend && yarn build && cd .. && mv frontend/build/index.html templates && python3 manage.py collectstatic --clear
python3 manage.py runserver
```