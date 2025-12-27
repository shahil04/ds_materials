
# URL Shortener – Flask Project

## Setup
1. Create MySQL database and table:
```
CREATE DATABASE url_db;
USE url_db;
CREATE TABLE urls (
  id INT AUTO_INCREMENT PRIMARY KEY,
  short_code VARCHAR(10) UNIQUE,
  long_url TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  click_count INT DEFAULT 0
);
```

2. Update DB credentials in app.py

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run app:
```
python app.py
```

Visit http://localhost:5000
