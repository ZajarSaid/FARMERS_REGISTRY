# FARMERS_REGISTRY
Hello ! my name is Zacharia Said i'm a junior developer
currently working on a farmers Registry system as it has to be elaborated below.......


This is a project dedicated to collect farmers information about their ownership and the total output in a specific period of cultivation also the project aims at delivering a specified range of all market crop prices across all the regions of Tanzania

## Table of Contents

- [Installation](#installation)
- [Making Migrations](#making-migrations)
- [Dependencies](packages)

 ## Installation Steps
Clone the repository:

git clone https://github.com/ZajarSaid/FARMERS_REGISTRY
cd FARMERS_REGISTRY

 Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

## Steps for making migrations:
1. Make migrations for farmer model:
python manage.py makemigrations farmer
python manage.py migrate farmer

2. Make migrations for crop and region models:
python manage.py makemigrations crop region
python manage.py migrate crop region

3. Make migrations for the farm model:
python manage.py makemigrations farm
python manage.py migrate farm

4. Make migrations for regional prices:
python manage.py makemigrations regional_prices
python manage.py migrate regional_prices


### Prerequisites

Ensure you have Python 3.10 installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
Ensure you consider the congiguration steps of Custom User model

### Dependencies

The project uses the following packages:

refer Pipfile
