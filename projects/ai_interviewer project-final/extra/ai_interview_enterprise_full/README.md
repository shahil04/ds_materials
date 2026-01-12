
ENTERPRISE AI INTERVIEW SAAS

LOCAL RUN:
1. cd backend
2. pip install -r requirements.txt
3. uvicorn app.main:app --reload

DOCKER:
docker-compose up --build

AWS:
- Push image to ECR
- Run on EC2/ECS
