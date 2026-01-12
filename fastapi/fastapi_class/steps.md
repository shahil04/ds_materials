uvicorn app:app --reload --port 8080
uvicorn aap:app --reload --host 127.0.0.1 --port 8080

python -m uvicorn app:app --reload --host 127.0.0.1 --port 8080
python -m pip install fastapi uvicorn

netstat -ano | findstr :8000
taskkill /PID 12345 /F
