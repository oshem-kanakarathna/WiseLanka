"""Deployment-specific health and configured-origin checks."""
import importlib
from fastapi.testclient import TestClient
from backend.app.api import main


def test_health_endpoint():
    with TestClient(main.app) as client:
        assert client.get('/health').json() == {'status': 'ok'}


def test_configured_frontend_origin(monkeypatch):
    with monkeypatch.context() as config:
        config.setenv('WISELANKA_CORS_ORIGINS', 'https://wiselanka.example.test')
        configured = importlib.reload(main)
        with TestClient(configured.app) as client:
            headers = {'Origin': 'https://wiselanka.example.test', 'Access-Control-Request-Method': 'POST', 'Access-Control-Request-Headers': 'content-type'}
            response = client.options('/assistant/guidance', headers=headers)
            assert response.status_code == 200
            assert response.headers['access-control-allow-origin'] == headers['Origin']
            headers['Origin'] = 'https://unrelated.example.test'
            assert client.options('/assistant/guidance', headers=headers).status_code == 400
    importlib.reload(main)
