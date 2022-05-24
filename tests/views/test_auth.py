from datetime import timedelta
from flask import current_app
from flaskr.auth.models import User, Token
from werkzeug.security import generate_password_hash

def test_login(client):
    endpoint = '/api/v2/auth/login'
    user = User(
        username = 'testuser1',
        first_name = 'test',
        last_name = 'user1',
        password = generate_password_hash('AAAAAAAAAAAAA')
    )
    user.save()
    token = Token(user=user)
    token.save()

    def test_login_valid_credentials():
        body = {
            'username': 'testuser1',
            'password': 'AAAAAAAAAAAAA'
        }
        response = client.post(
            endpoint,
            json = body
        )
        assert response.status_code == 201

        # Test case where token has expired
        assert token.has_expired == False

        token.created_at = token.created_at - timedelta(hours = current_app.config['LOGIN_TIMEOUT_HOURS'] + 1)
        token.save()
        assert token.has_expired == True
        response = client.post(
            endpoint,
            json = body
        )
        assert response.status_code == 201


    def test_login_no_credentials():
        body = {
            'username': '',
            'password': ''
        }
        response = client.post(
            endpoint,
            json = body
        )
        assert response.status_code == 404
        response = client.post(
            endpoint,
        )
        assert response.status_code == 400

    def test_login_invalid_password():
        body = {
            'username': 'testuser1',
            'password': 'ABABABABBABA'
        }
        response = client.post(
            endpoint,
            json = body
        )
        assert response.status_code == 404
        response = client.post(
            endpoint,
        )
        assert response.status_code == 400

    test_login_valid_credentials()
    test_login_no_credentials()
    test_login_invalid_password()


def test_logout(client):
    endpoint = '/api/v2/auth/logout'
    user = User(
        username = 'testuser1',
        first_name = 'test',
        last_name = 'user1',
        password = 'password'
    )
    user.save()
    token = Token(user=user)
    token.save()

    client.environ_base['HTTP_AUTHORIZATION'] = f'Token {token.key}'
    response = client.post(endpoint)
    assert response.status_code == 201

def test_routes(client):
    endpoint = '/api/v2/auth/'
    response = client.get(endpoint)
    assert response.status_code == 200
