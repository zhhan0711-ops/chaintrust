from fastapi.testclient import TestClient
from app.main import app

def test_analyze_code_returns_structured_report():
    client = TestClient(app)
    response = client.post('/api/v1/analyses', json={'input_type':'code','source_code':'contract A { function x() external { tx.origin; } }'})
    assert response.status_code == 200
    data = response.json()
    assert 'report_hash' in data and 'overall_risk_level' in data['report']

def test_sandbox_change_review_api():
    client=TestClient(app); response=client.post('/api/v1/change-reviews',json={'sandbox':True})
    assert response.status_code==200
    assert response.json()['release_readiness']=='blocked'
