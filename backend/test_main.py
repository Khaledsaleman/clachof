from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to TCOC API"}

def test_get_user_me_unauthorized():
    # Should fail without auth header or with invalid one
    response = client.get("/users/me")
    # FastAPI returns 403 or 422 if Security(security) is missing header entirely
    # Depending on how HTTPBearer is used.
    assert response.status_code in [401, 403, 422]
