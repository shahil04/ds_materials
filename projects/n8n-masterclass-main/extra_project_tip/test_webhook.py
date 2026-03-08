import requests


user_message = "Can you tell me about black holes in 3-4 lines"

request_message = {"message": user_message}

url = "http://localhost:5678/webhook-test/3d4fdb4d-5f85-4694-ad8e-0ce573ed53ee"

response = requests.post(url, json=request_message)

print(response.status_code)

print(response.json()[0]["output"])