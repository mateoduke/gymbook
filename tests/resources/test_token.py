from datetime import timedelta
from flask import current_app
from flaskr.auth.models import User, Token
from werkzeug.security import generate_password_hash


def test_token_resource(client):
    user1 = User(
        username = 'testuser1',
        first_name = 'test',
        last_name = 'user1',
        password = generate_password_hash('AAAAAAAAAAAAA'),
        admin = True
    )
    user1.save()
    token1 = Token(user=user1)
    token1.save()
    user2 = User(
        username = 'testuser2',
        first_name = 'test',
        last_name = 'user2',
        password = generate_password_hash('AAAAAAAAAAAAA'),
    )
    user2.save()
    token2 = Token(user=user2)
    token2.save()


    def test_get():

        endpoint = '/api/v2/auth/tokens/1'

        # test using an unauthorized user token
        client.environ_base['HTTP_AUTHORIZATION'] = f'Token {token2.key}'
        response = client.get(endpoint)
        assert response.status_code == 403

        # test using an authorized user token
        client.environ_base['HTTP_AUTHORIZATION'] = f'Token {token1.key}'
        response = client.get(endpoint)
        assert response.status_code == 200

    test_get()


def test_token_list_resource(client):
    user1 = User(
        username = 'testuser1',
        first_name = 'test',
        last_name = 'user1',
        password = generate_password_hash('AAAAAAAAAAAAA'),
        admin = True
    )
    user1.save()
    token1 = Token(user=user1)
    token1.save()
    user2 = User(
        username = 'testuser2',
        first_name = 'test',
        last_name = 'user2',
        password = generate_password_hash('AAAAAAAAAAAAA'),
    )
    user2.save()
    token2 = Token(user=user2)
    token2.save()


    def test_get():

        endpoint = '/api/v2/auth/tokens'

        # test using an unauthorized user token
        client.environ_base['HTTP_AUTHORIZATION'] = f'Token {token2.key}'
        response = client.get(endpoint)
        assert response.status_code == 403

        # test using an authorized user token
        client.environ_base['HTTP_AUTHORIZATION'] = f'Token {token1.key}'
        response = client.get(endpoint)
        assert response.status_code == 200

    test_get()
