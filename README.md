# shopify-backend-challenge-2022
Shopify Backend Coding Challenge 2022

## Setup
To clone the project and set up virtual environment:
```
git clone https://github.com/dchen3121/shopify-backend-challenge-2022.git
cd shopify-backend-challenge-2022
python3 -m venv venv
```
To activate virtual environment and install dependencies:
```
. venv/bin/activate
python3 -m pip install -e .
```
Then, to initialize the database and run the app locally:
```
export FLASK_APP=inventory
export FLASK_ENV=development
python3 -m flask init-db
python3 -m flask run
```
