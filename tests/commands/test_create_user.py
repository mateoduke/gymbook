import pytest

from pytest import MonkeyPatch
from werkzeug.security import generate_password_hash

from flaskr.auth.commands import create_user
from flaskr.auth.models import User


@pytest.fixture
def cli_create_user(runner):
    user = User(
        username = 'testuser1',
        first_name = 'test',
        last_name = 'user1',
        password = generate_password_hash('AAAAAAAAAAAAA')
    )
    user.save()
    return runner


def test_create_user_username_taken(cli_create_user, monkeypatch):
    inputs = ['testuser1', 'test', 'user1', '']
    passwords = ['AAAAAAAAAAAAA', 'AAAAAAAAAAAAA']
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
    monkeypatch.setattr('getpass.getpass', lambda _: passwords.pop(0))
    result = cli_create_user.invoke(cli=create_user)
    assert 'Username: testuser1 already in use' in result.output


def test_create_user_short_password(cli_create_user, monkeypatch):
    inputs = ['testuser2', 'test', 'user2', '']
    passwords = ['AAAAA', 'AAAAA']
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
    monkeypatch.setattr('getpass.getpass', lambda : passwords.pop(0))
    result = cli_create_user.invoke(cli=create_user)
    assert 'Password must be at least 12 characters long' in result.output


def test_create_user_password_mismatch(cli_create_user, monkeypatch):
    inputs = ['testuser2', 'test', 'user2', '']
    passwords = ['AAAAAAAAAAAAA', 'AAAAAAAAAAAAB']
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
    monkeypatch.setattr('getpass.getpass', lambda *args: passwords.pop(0))
    result = cli_create_user.invoke(cli=create_user)
    assert 'Passwords do not match' in result.output


def test_create_user(cli_create_user, monkeypatch):
    inputs = ['testuser2', 'test', 'user2', '']
    passwords = ['AAAAAAAAAAAAA', 'AAAAAAAAAAAAA']
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
    monkeypatch.setattr('getpass.getpass', lambda *args: passwords.pop(0))
    result = cli_create_user.invoke(cli=create_user)
    assert 'New user created successfully' in result.output
