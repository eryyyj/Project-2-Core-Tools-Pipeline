# Project-2-Core-Tools-Pipeline
This repository is about my compliance on week 2 deliverables

Run to initialize the database in your local machine
docker run --name bootcamp-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=bootcamp \
  -p 5432:5432 \
  -d postgres:latest