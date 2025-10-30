
# CS With Shahil - Landing Page (Flask + MySQL)

## Overview
Simple responsive landing page for a technical institute "CS With Shahil".
Features:
- Hero section, course cards
- Enquiry form (Name, Email, Mobile) saved to MySQL
- Sidebar menu (desktop/mobile)
- Floating WhatsApp icon, Google Review button, chatbot icon
- Flask backend to receive enquiries and store in MySQL

## Setup (local)
1. Create a Python virtual env:
   ```bash
   python -m venv venv
   source venv/bin/activate   # mac/linux
   venv\Scripts\activate    # windows
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Create MySQL database and table using `schema.sql` or run the commands manually.
   Update `config.py` with your MySQL credentials.
4. Run the app:
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   flask run
   ```
   On Windows (PowerShell):
   ```powershell
   $env:FLASK_APP='app.py'; $env:FLASK_ENV='development'; flask run
   ```
5. Open http://127.0.0.1:5000

## Notes
- The project uses `mysql-connector-python`. You can switch to other connectors if preferred.
- Replace placeholder links in `templates/index.html` (WhatsApp phone, Google review URL).
