import requests

poll_id = "1"  # Replace with the actual poll ID
option = "Python"  # Replace with the chosen option

response = requests.post(f"http://127.0.0.1:8000/polls/{poll_id}/vote/?option={option}")
print(response.json())
