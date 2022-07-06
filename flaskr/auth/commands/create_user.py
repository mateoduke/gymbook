import getpass

from ..models import User
from ..schemas import UserSchema
from flaskr.auth import auth_bp



@auth_bp.cli.command('create_user')
def create_user():
    """Interactive commandline function for creating a user"""

    username = input('Please enter username: ')
    if User.query.filter_by(username=username).count() > 0:
        print(f'Username: {username} already in use')
        return False

    password = getpass.getpass()
    if len(password) < 12:
        print('Password must be at least 12 characters long')
        return False

    password_confirmation = getpass.getpass('Password [Re-Enter]:')
    if password_confirmation != password:
        print('Passwords do not match')
        return False


    first_name = input('Please enter first name: ')
    last_name = input('Please enter last name: ')
    admin = input('Admin: [Leave blank for no]: ') != ''

    user_json = {
        'username': username,
        'password': password,
        'first_name': first_name,
        'last_name': last_name,
        'admin': admin
    }
    user_context = UserSchema().load(user_json)

    user_context['instance'].save()
    print('New user created successfully')
    return True
