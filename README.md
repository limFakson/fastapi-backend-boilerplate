# FastAPI Backend Starter

A scalable backend starter template built with **FastAPI**.
This project provides a clean architecture to help you build maintainable and production-ready APIs.

---

## Features

* FastAPI backend framework
* Structured project architecture
* API versioning
* Environment configuration
* SQLAlchemy database setup
* Health check endpoint
* Ready for authentication and scaling

---

## Project Structure

```
fastapi-backend/
│
|
│
├── core/
│   └── config.py
│
├── api/
│    ├── router.py
│    └── endpoints/
│         └── health.py
│
├── models/
├── schemas/
├── services/
|── db/
    └── session.py
│
├── tests/
├── .env
├── requirements.txt
├── main.py
└── README.md
```

---

## Installation

### 1. Clone the repository

```
git clone https://github.com/limFakson/fastapi-backend-boilerplate.git
cd fastapi-backend
```

### 2. Create virtual environment

```
python -m venv venv
```

Activate it:

Mac / Linux

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory.

Example:

```
APP_NAME=FastAPI Backend
DEBUG=True
DATABASE_URL=sqlite:///./test.db
```

---

## Running the Server

Start the development server:

```
python run.py
```

Server will run at:

```
http://localhost:8000
```

---

## API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

```
http://localhost:8000/docs
```

ReDoc:

```
http://localhost:8000/redoc
```

---

## Example Endpoint

Health check:

```
GET /api/v1/health
```

Response:

```
{
  "status": "ok",
  "message": "API is healthy"
}
```

---

## Running Tests

```
pytest
```

---

## Future Improvements

This starter can be extended with:

* JWT authentication
* PostgreSQL database
* Alembic migrations
* Redis caching
* Background jobs
* Docker containerization
* CI/CD pipelines
* Rate limiting
* Role-based access control

---

## Built With

* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn

---

## License

MIT License

---

## Contributing

Contributions are welcome.
Please open an issue or submit a pull request.
# fastapi-backend-boilerplate
