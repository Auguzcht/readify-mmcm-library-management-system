# Controls the centralized data

current_user = {
    'name': None,
    'role': None
}

def set_current_user(name, role):
    global current_user
    current_user['name'] = name
    current_user['role'] = role

def get_current_user():
    return current_user


