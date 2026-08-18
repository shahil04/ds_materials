# # pip install boto3

# import boto3 
# import json  

# client = boto3.client("bedrock-runtime", region_name="us-east-1")  

# response = client.invoke_model( 
#     modelId="us.anthropic.claude-haiku-4-5-20251001-v1:0", 
#     body=json.dumps({ 
#         "anthropic_version": "bedrock-2023-05-31", 
#         "max_tokens": 1024, 
#         "messages": [{ 
#             "role": "user", 
#             "content": "Tell me a short story about a robot." 
#         }] 
#     }) 
# )  

# result = json.loads(response["body"].read()) 
# print(result["content"][0]["text"])

from openai import OpenAI  

client = OpenAI(api_key="bedrock-api-key-YmVkcm9jay5hbWF6b25hd3MuY29tLz9BY3Rpb249Q2FsbFdpdGhCZWFyZXJUb2tlbiZYLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFTSUE0V0VTUFJTRllEWkdHRkNEJTJGMjAyNjA4MTYlMkZ1cy1lYXN0LTElMkZiZWRyb2NrJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA4MTZUMTQyNzQ5WiZYLUFtei1FeHBpcmVzPTQzMjAwJlgtQW16LVNlY3VyaXR5LVRva2VuPUlRb0piM0pwWjJsdVgyVmpFR2NhQ1hWekxXVmhjM1F0TVNKSE1FVUNJUUN1R2ZjYUFrVkFGdEVZOEIzd01iejRRNUVGWkN6TnJZUmZsNnhNJTJGbjVZRUFJZ1AlMkZhdEQ0Q1RXNDdydXM0eGc1Rk5oeHMwbTFhJTJGOFFteEtiQjhjeWpMVlU0cXBRTUlNQkFBR2d3NE56SXhPRFUxTmpReU9Ua2lEQ1hveEhKelZ2eGhvelNVTENxQ0EyMkJDZHdLMWJnU1NEMTM0V0xXd0JKUkJQUE92MzFYcEJwRG5acEd0UlUyWHRrbjFGTGdKOEMlMkZjaHpiemtKcnFpTW01UVZocmJMUG5CaXd4NzdJeHdCVUNxUVBuQTNRemdmbzklMkJubk5jR3NHODlNQUYlMkYyb3ZUVDI3emNWQ21uTmFDYURIMjFMaGxIVmtBUEZZQ05wQlJIeGp4TjNpVEUycHFzbGRMeXNIQ0JydnBwTGVJclJsSGhZJTJCNTlWUlBUJTJCVUFnNVJDUDFxbm4yYjd6S2lJSDFmJTJGa3RQYmxBanFiMlJJeSUyQkFqMlpuUTZwcDNlMk5lUUIlMkZTOHFCRzdaV0Fla0dYZGslMkZydUY5RlI4RkxuMm53WlB6Z2dSMmZNalcySGYzS0k2TFkxRXF3SXptTHNZM3JxS3BjTE5qMlBDWENUUU5zRHRXTVk0QnVseGxRYmNWY3hFbEJOeE83byUyRjZrVVptUDZOYTJJZCUyRkVMblBkNkhXMVdMWmZKSkhmYVgzaXpvJTJCYzNHRTBLc0pEaXhlOEhGN1lzMm5KT1NxWm5ISENuZnNiaVE0d05qZTBUQ1RHeFlPNGpYdGdUUWhONFdubjYyclp5UFNXSUlERWFGNldTeWFVWmElMkJvZjhiU2lwZU1oWUIwODhDZlQxbjh5Y0YyNXNCUExBWWpHTzh6NWRLTG1xVVF5TU1yM2hkUUdPdDRDTGdGYmxBT2ltVjBBdHdTcGFuc0tmSDQ0a01rY3QwNGFCJTJCeVFxYk1xcXpSVnhpY1NPenRJbkwlMkZONlAzUzZkNGp3ZldxYXhlaEN0RFRQZG1xNkltckRzaVd4UzNIYktvSEpKcUxiYm9XRmVNOURid05KV2l4aFdMJTJCJTJCMEp6ZFExMCUyQmZJVkt5UmFjYVUwUFZuMjV2UzNGVVl5cjg5enRGZlZzU2kxQzRsJTJGSVB1a2U3dnJkNUhaTFNjVE5XeTVqNWxJeG5CVEFYMGNZdGdGakNIUmNBRzVOencxdHQlMkY1eXRhdUl4VjdKNkdqVSUyQlBLOUN0ZW9FTkJGcFdiJTJGUzFTdiUyRmIyYzgwR0NwOTVpWUdmTERyWGlmY1llSGZmN1klMkIzJTJGaDU1SUVqWEw3MDJqYXVtJTJCd0M2SzMlMkZFaERVNjlNWmJVNENJdm5mQ3drWU93elRkMU15SUNKSGxpMmpoUzJzSExNcyUyRjRCdVNrOUViYkU1dkxqJTJCT0IxVTJWMTBnWDVvbTF3WnhBMkN6N2gySDdiQiUyRjlkUGFHZUtNdmJEVlVwJTJGc1JQeGhrJTJGQ2FTY1FhVHZCSlBCTiUyRnJsZVlmMm1EZDUzbHBlJTJGOEQyOWRCMjJuOFNJOWJvODN4d1klM0QmWC1BbXotU2lnbmF0dXJlPTg2M2NjNzk5NmQ4NzMzYzZkNzRhMzAzYjQ0YjI4ZjhlNTU2Yjc0ZjRlYmU1ZTc3NzFkMzQ4N2Y0ZDJmZTVlNmMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JlZlcnNpb249MQ==")  

response = client.responses.create( 
    model="openai.gpt-oss-120b", 
    input=[ 
        {"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."} 
    ] 
)  

print(response.output_text)