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