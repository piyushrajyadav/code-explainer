import requests
import json

response = requests.post('http://localhost:8000/explain/', json={
    'code': 'print("Hello World")',
    'language': 'python',
    'analysis_method': 'nlp',
    'model_name': 'gemini-1.5-flash'
})

print('Status:', response.status_code)
print('Response keys:', list(response.json().keys()))
print('Full Response:')
print(json.dumps(response.json(), indent=2))
