docker-compose build
docker-compose up -d

docker compose up airflow-init


docker run -d -p 8080:8080 apache/airflow:latest webserver


docker logs <container_name_or_id>


# 1. Stop everything and completely delete the broken volumes
docker compose down --volumes --remove-orphans

# 2. Force a clean database initialization
docker compose up airflow-init
