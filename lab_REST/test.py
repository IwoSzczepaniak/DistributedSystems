import requests

poll_id = "1"  # Replace with the actual poll ID

response = requests.get(f"http://127.0.0.1:8000/polls/{poll_id}/results/")
print(response.json())
