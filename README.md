### Setup

#### Using pipenv:
- Install dependencies and start virtual environment: `pipenv install`

#### Using pip:
- Create virtual environment: `venv vendomatic`
- Install dependencies: `pip install -r requirements.txt`

### Run project
- Populate db with vending machine and inventory: `python manage.py populate_db`
- Run server: `python manage.py runserver`

### Test endpoints

You can test the api using postman or the browsable api from a browser

- Add coin: PUT `http://localhost:8000/api/`, body: `{"coin": 1}`
- Get coins back: DELETE `http://localhost:8000/api/`

- Get inventory list: GET `http://localhost:8000/api/inventory/`
- Get inventory item detail: GET `http://localhost:8000/api/inventory/:id`

- Buy beverage: PUT `http://localhost:8000/api/inventory/:id`
