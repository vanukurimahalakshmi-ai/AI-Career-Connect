import pytest
from app import create_app
from app.models import db, User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_dashboard_route(client):
    """Test dashboard index route returns HTTP 200."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Dynamic Performance Dashboard' in response.data

def test_dashboard_stats_api(client):
    """Test dashboard stats API JSON endpoint."""
    response = client.get('/api/dashboard/stats')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'stats' in json_data
    assert 'chart_data' in json_data

def test_interview_room_route(client):
    """Test AI Voice Interview room HTML rendering."""
    response = client.get('/interview')
    assert response.status_code == 200
    assert b'AI Voice Mock Interview Studio' in response.data

def test_interview_start_api(client):
    """Test interview session initiation API."""
    response = client.post('/api/interview/start', json={
        'target_role': 'AI Engineer',
        'topic': 'System Design & Scalability'
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'success'
    assert 'current_question' in json_data
