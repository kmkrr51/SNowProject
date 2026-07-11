from fastapi.testclient import TestClient
from src.main import app

c = TestClient(app)
r = c.options('/api/v1/auth/login', headers={'Origin':'http://localhost:3000','Access-Control-Request-Method':'POST','Access-Control-Request-Headers':'content-type'})
print('status', r.status_code)
print('allow-origin', r.headers.get('access-control-allow-origin'))
print('allow-methods', r.headers.get('access-control-allow-methods'))
print('allow-headers', r.headers.get('access-control-allow-headers'))
