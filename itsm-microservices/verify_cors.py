from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
response = client.options(
    '/api/v1/auth/login',
    headers={
        'Origin': 'http://localhost:3000',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'content-type',
    },
)
print('status', response.status_code)
print('headers', dict(response.headers))
print('body', response.text)
