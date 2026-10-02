



import os
import requests
import time

api_key = os.getenv("SECRET_API_KEY")
url = "https://api.openai.com/v1/chat/completions"

message = input("Enter your message: ")

try:
  response = requests.post(url, api_key=api_key, json={
      "model": "gpt-4o-mini",
      "messages": [
          {"role": "system", "content": "You are a helpful assistant.",},
          {"role": "user", "content": message}
      ]
  })

except Exception as error:
    print(f"An error occurred while making the request: {error}")
    while True:
       time.sleep(1)
       