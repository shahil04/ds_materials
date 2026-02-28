
# URL Shortener – Docker + Flask + MySQL

## Run locally
docker-compose up --build

Open:
http://localhost:5000

## Create table (first run)
docker exec -it url_shortener_docker_full-db-1 mysql -u admin -p
Password: root

CREATE TABLE urls (
  id INT AUTO_INCREMENT PRIMARY KEY,
  short_code VARCHAR(10) UNIQUE,
  long_url TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  click_count INT DEFAULT 0
);
