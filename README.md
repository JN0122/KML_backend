![image](https://github.com/JN0122/KML_backend/assets/38890130/6cb01233-f015-41c4-afb5-73b775081601)

# Fuelly

Backend application to manage fuel deliveries to gas stations for a university project.

## Swagger

[localhost:8000/docs](localhost:8000/docs)

## Installation

```bash
cd KML_backend
python -m venv .
pip install -r requirements.txt
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
