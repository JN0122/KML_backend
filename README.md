![image](https://github.com/JN0122/KML_backend/assets/38890130/6cb01233-f015-41c4-afb5-73b775081601)

# Fuelly

Backend application to manage fuel deliveries to gas stations for a university project.

## Swagger

[localhost:8000/docs](localhost:8000/docs)

## Installation
Application requires **Python >=3.12** to run.

Clone the repository and cd into it
```bash
git clone https://github.com/JN0122/KML_backend
cd KML_backend
```
Create venv in repository
```bash
python -m venv venv
pip install -r requirements.txt
```
Activate venv on windows
```bash
.\venv\Scripts\Activate.ps1
```
Install requirements
```bash
pip install -r requirements.txt
```
Run fastapi development mode
```bash
fastapi dev main.py
```

## Running dev

```bash
fastapi dev main.py
```

## Running production

```bash
fastapi run main.py
```

## Seeding database

```bash
fastapi dev main.py
curl -X 'GET' 'http://localhost:8000/db/seed' -H 'accept: application/json'
```
