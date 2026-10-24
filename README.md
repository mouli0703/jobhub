![CI](https://github.com/mouli0703/jobhub/actions/workflows/ci.yml/badge.svg)
# JobHub

A modular monolith for running automation jobs. I am migrating it step by step into microservices as a learning lab.

## Run locally
pip install -r requirements-dev.txt
uvicorn app.main:app --reload

## Run in Docker
docker build -t jobhub:0.1 .
docker run --rm -p 8000:8000 jobhub:0.1

## Architecture rule
Modules talk to each other only through service functions, never through each other's internals.

## Roadmap
Week 1: monolith skeleton and Docker. Next: database, auth, CI, cloud deploy, safe releases, then splitting into services.


## Run with Docker Compose (app + Postgres)
docker compose up --build

## Run tests
python -m pytest

## API
POST /users/register, POST /users/login, GET /users/me
GET/POST /jobs/, GET/PATCH/DELETE /jobs/{id} (login required, owner only)

## Design notes
- Jobs stores owner_id as a plain integer (no foreign key to users), so the module can be extracted later.
- Tables are created at startup. Week 6 replaces this with proper migrations.
## CI
Every push runs Ruff, the tests and a Docker build (GitHub Actions).

## Configuration
ENVIRONMENT, SECRET_KEY, DATABASE_URL and ACCESS_TOKEN_EXPIRE_MINUTES come from environment variables. See .env.example.