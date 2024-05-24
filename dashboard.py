from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage,messagebox
from user_state import get_current_user
import pandas as pd

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\MMCM\COMPSCI 1ST YR\2T\IT101-1 Computer Programming Concepts 1\FINAL PROJECT\project\GUI\Dashboard(Main)\build\assets\frame0")

def show_dashboard():
    user_info = get_current_user()
    user_name = user_info['name']
    user_role = user_info['role']

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def open_books(window):
        window.destroy()
        from book import show_book
        show_book()

    def open_issued(window):
        window.destroy()
        from issued_books import show_issued_books
        show_issued_books()

    def show_help_faq():
        help_text = """Help & FAQ
        
Q: How do I borrow a book from the Library?
A: Go to the 'Books' section to browse for books and click 'Borrow'.

Q: Where do I find my borrowed books?
A: You may find your issued books in the 'Issued/Return' section where you can renew your particular book twice.
    
Q: How long can I borrow a book for?
A: Your initial issuance permits you to borrow for two weeks, if ever you decide to, you can extend your issuance for an additional two weeks by 'Renewing'--a total of one month rented out to you.
    
Q: Why can't I borrow a book?
A: You will be unable to borrow a book if it is not available in stock (borrowed by other users) which you can view in the details by clicking on a book.
    
Q: How do I return a book?
A: You are able to the return a book via the 'Issued/Return' section before or after the due date.
    
For more assistance, contact the Readify staff, Alfred Nodado. Thank you for your patronage!"""

        messagebox.showinfo("Help/FAQ", help_text)

    # Count total books
    books_df = pd.read_excel('books.xlsx')
    total_books = len(books_df.index)

    # Count total users and students
    users_df = pd.read_excel('users.xlsx')
    total_users = len(users_df.index)
    total_students = len(users_df[users_df['Role'] == 'Student'])

    # Count total issued books by the user
    issued_books_df = pd.read_excel('issued.xlsx')
    total_issued_books_by_user = len(issued_books_df[issued_books_df['Username'] == user_name])

    # Initialize Dashboard
    window = Tk()
    # Set the dimensions of the window
    window_width = 900
    window_height = 550

    # Calculate x and y coordinates for the Tk window
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)

    # Set the dimensions and position of the window
    window.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
    window.configure(bg = "#FFFFFF")

    window.title("Readify: MMCM Library Management System")

    # Store images in a list on the window to ensure they persist
    window.images = []

    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 550,
        width = 900,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        225.0,
        550.0,
        fill="#262626",
        outline="")

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    window.images.append(button_image_1)  # Keep a reference
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=show_help_faq,
        relief="flat"
    )
    button_1.place(
        x=47.0,
        y=501.0,
        width=178.0,
        height=31.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    window.images.append(button_image_4)  # Keep a reference
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: open_issued(window),
        relief="flat"
    )
    button_4.place(
        x=47.0,
        y=316.0,
        width=178.0,
        height=31.0
    )

    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    window.images.append(button_image_5)  # Keep a reference
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: open_books(window),
        relief="flat"
    )
    button_5.place(
        x=47.0,
        y=278.0,
        width=178.0,
        height=31.0
    )

    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    window.images.append(button_image_6)  # Keep a reference
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("Dashboard"),
        relief="flat"
    )
    button_6.place(
        x=47.0,
        y=244.0,
        width=178.0,
        height=31.0
    )

    user_name_text_id = canvas.create_text(
        306.0,
        34.0,
        anchor="nw",
        text="",
        fill="#262626",
        font=("JostRoman Regular", 13 * -1)
    )

    user_role_text_id = canvas.create_text(
        306.0,
        53.0,
        anchor="nw",
        text="",
        fill="#262626",
        font=("JostRoman Bold", 13 * -1)
    )

    canvas.itemconfig(user_name_text_id, text=user_name)

    canvas.itemconfig(user_role_text_id, text=user_role)

    canvas.create_text(
        246.0,
        95.0,
        anchor="nw",
        text="Dashboard",
        fill="#262626",
        font=("JostRoman Bold", 30 * -1)
    )

    canvas.create_text(
        246.0,
        133.0,
        anchor="nw",
        text=f"Welcome to the MMCM Readify Library Management System, {user_name}!",
        fill="#262626",
        font=("JostRoman Regular", 16 * -1)
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    window.images.append(image_image_1)
    image_1 = canvas.create_image(
        447.0,273.0,
        image=image_image_1
    )

    canvas.create_text(
        21.0,
        207.0,
        anchor="nw",
        text="Readify: MMCM LMS System",
        fill="#FFFFFF",
        font=("JostRoman Bold", 13 * -1)
    )

    canvas.create_text(
        435.0,
        270.0,
        anchor="nw",
        text="Total\nBooks",
        fill="#FFFFFF",
        font=("JostRoman Bold", 24 * -1)
    )

    canvas.create_text(
        435.0,
        460.0,
        anchor="nw",
        text="Total\nStudents",
        fill="#FFFFFF",
        font=("JostRoman Bold", 24 * -1)
    )

    canvas.create_text(
        722.0,
        464.0,
        anchor="nw",
        text="Total Books\nIssued",
        fill="#FFFFFF",
        font=("JostRoman Bold", 19 * -1)
    )

    canvas.create_text(
        721.0,
        270.0,
        anchor="nw",
        text="Total\nUsers",
        fill="#FFFFFF",
        font=("JostRoman Bold", 24 * -1)
    )

    canvas.create_text(
        449.0,
        202.0,
        anchor="nw",
        text=str(total_books),
        fill="#FFFFFF",
        font=("JostRoman Bold", 64 * -1)
    )

    canvas.create_text(
        470.0,
        391.0,
        anchor="nw",
        text=str(total_students),
        fill="#FFFFFF",
        font=("JostRoman Bold", 64 * -1)
    )

    canvas.create_text(
        756.0,
        391.0,
        anchor="nw",
        text=str(total_issued_books_by_user),
        fill="#FFFFFF",
        font=("JostRoman Bold", 64 * -1)
    )

    canvas.create_text(
        756.0,
        202.0,
        anchor="nw",
        text=str(total_users),
        fill="#FFFFFF",
        font=("JostRoman Bold", 64 * -1)
    )

    canvas.create_text(
        101.0,
        34.0,
        anchor="nw",
        text="Mapúa Malayan \nColleges Mindanao",
        fill="#FFFFFF",
        font=("JostRoman Regular", 13 * -1)
    )
    window.resizable(False, False)
    return window