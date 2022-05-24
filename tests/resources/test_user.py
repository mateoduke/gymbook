from datetime import timedelta
from flask import current_app
from flaskr.auth.models import User, Token
from werkzeug.security import generate_password_hash

def test_user_resourse(client):
    endpoint = '/api/v2/auth/users/1'
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

    def test_get_user_as_admin():
        endpoint = '/api/v2/auth/users/1'
        client.environ_base['HTTP_AUTHORIZATION'] = f'Token {token1.key}'
        response = client.get(endpoint)
        assert response.status_code == 200


    def test_get_user_not_as_admin():
        client.environ_base['HTTP_AUTHORIZATION'] = f'Token {token2.key}'
        response = client.get(endpoint)
        assert response.status_code == 403


    def test_get_user_dne():
        endpoint = '/api/v2/auth/users/100'
        client.environ_base['HTTP_AUTHORIZATION'] = f'Token {token1.key}'
        response = client.get(endpoint)
        assert response.status_code == 404

    test_get_user_as_admin()
    test_get_user_not_as_admin()
    test_get_user_dne()


def test_user_list_resource(client):
    endpoint = '/api/v2/auth/users'
    user1 = User( # admin user
        username = 'testuser1',
        first_name = 'test',
        last_name = 'user1',
        password = generate_password_hash('AAAAAAAAAAAAA'),
        admin = True
    )
    user1.save()
    token1 = Token(user=user1)
    token1.save()
    user2 = User( # normal user
        username = 'testuser2',
        first_name = 'test',
        last_name = 'user2',
        password = generate_password_hash('AAAAAAAAAAAAA'),
    )
    user2.save()
    token2 = Token(user=user2)
    token2.save()

    def test_get():
        client.environ_base['HTTP_AUTHORIZATION'] = f'Token {token1.key}'
        response = client.get(endpoint)
        assert response.status_code == 200
        client.environ_base['HTTP_AUTHORIZATION'] = f'Token {token2.key}'
        response = client.get(endpoint)
        assert response.status_code == 403


    def test_post_no_body():
        response = client.post(endpoint)
        assert response.status_code == 500


    def test_post():
        """Tests creating a new user"""
        body = {
            "username": "test3",
            "first_name": "test",
            "last_name": "user3",
            "password": "BBBBBBBBBBBBB",
            "admin": True
        }
        # test attempting to create an admin without being an admin
        client.environ_base['HTTP_AUTHORIZATION'] = f'Token {token2.key}'
        response = client.post(endpoint,
                               json =body)
        assert response.status_code == 403

        # test attempting to create an admin as an admin
        client.environ_base['HTTP_AUTHORIZATION'] = f'Token {token1.key}'
        response = client.post(endpoint,
                               json =body)
        assert response.status_code == 201

        # test attempting to create an admin with a bad token
        client.environ_base['HTTP_AUTHORIZATION'] = 'badtoken'
        response = client.post(endpoint,
                               json =body)
        assert response.status_code == 403

        #test attempting to create a user with a bad password
        client.environ_base['HTTP_AUTHORIZATION'] = f'Token {token1.key}'
        body['password'] = 'A'
        response = client.post(endpoint,
                               json =body)
        assert response.status_code == 400


    test_get()
    test_post_no_body()
    test_post()
