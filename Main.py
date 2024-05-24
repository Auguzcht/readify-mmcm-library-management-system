from tkinter import messagebox
from auth import authenticate_user, create_account
import login_screen
from dashboard import show_dashboard
from admin import show_admin
from user_state import set_current_user

def main():
    def login_attempt():
        username = login_screen.entry_1.get()
        password = login_screen.entry_2.get()
        user_role = authenticate_user(username, password)
        if user_role:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            login_screen.window.destroy()
            set_current_user(username, user_role)
            if user_role == 'Admin':
                # For admin, show the admin panel
                admin_window = show_admin()
                admin_window.mainloop()
            else:
                # For other roles, show the dashboard
                dashboard_window = show_dashboard()
                dashboard_window.mainloop()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    def attempt_create_account():
        username = login_screen.entry_1.get()
        password = login_screen.entry_2.get()
        if create_account(username, password):
            messagebox.showinfo("Account Created", "Your account has been created successfully.")
            login_screen.window.destroy()
            # Assuming by default new accounts are not admins
            set_current_user(username, "Student")
            dashboard_window = show_dashboard()
            dashboard_window.mainloop()
        else:
            messagebox.showerror("Error", "This username already exists. Please choose another.")

    # Configuration of button commands before starting the event loop
    login_screen.button_1.configure(command=login_attempt)
    login_screen.button_2.configure(command=attempt_create_account)

    login_screen.window.mainloop()

if __name__ == "__main__":
    main()