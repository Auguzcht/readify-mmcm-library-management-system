# Secured authentication

import pandas as pd

users_file = 'users.xlsx'

def authenticate_user(username, password):
    users_df = pd.read_excel(users_file, engine='openpyxl')
    user = users_df[(users_df['Username'] == username) & (users_df['Password'] == password)]
    if not user.empty:
        return user.iloc[0]['Role']
    return None

def create_account(username, password):
    # Load the existing users data
    users_df = pd.read_excel(users_file)

    # Check if the username already exists
    if username in users_df['Username'].values:
        return False  # Username already exists

    # Add the new account with the role "Student"
    new_user = pd.DataFrame({
        'Username': [username],
        'Password': [password],
        'Role': ['Student']
    })
    users_df = pd.concat([users_df, new_user], ignore_index=True)

    # Save the updated DataFrame back to the Excel file
    with pd.ExcelWriter(users_file, engine='openpyxl', mode='w') as writer:
        users_df.to_excel(writer, index=False)

    return True  # Account created successfully