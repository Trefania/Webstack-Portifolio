import pytest
from app import app, db
from models.user import User


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_register(client):
    response = client.post(
        '/register', data={'username': 'john', 'password': 'pass123'})
    assert response.status_code == 200
    assert b'User registered successfully' in response.data


def test_signin(client):
    # Create a test user
    user = User(username='john', password='pass123')
    db.session.add(user)
    db.session.commit()

    # Test login with valid credentials
    response = client.post(
        '/login', data={'username': 'john', 'password': 'pass123'})
    assert response.status_code == 200
    assert b'Login successful' in response.data

    # Test login with invalid credentials
    response = client.post(
        '/login', data={'username': 'john', 'password': 'wrongpassword'})
    assert response.status_code == 200
    assert b'Invalid credentials' in response.data


def test_home(client):
    # Create a test user
    user = User(username='john', password='pass123')
    db.session.add(user)
    db.session.commit()

    # Log in the user
    client.post('/login', data={'username': 'john', 'password': 'pass123'})

    # Test accessing the protected route
    response = client.get('/protected')
    assert response.status_code == 200
    assert b'Welcome, authenticated user!' in response.data
