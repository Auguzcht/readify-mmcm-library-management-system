from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, ttk, messagebox, Scrollbar, VERTICAL
from PIL import Image, ImageTk
import pandas as pd
import random
from user_state import get_current_user
from datetime import datetime, timedelta

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\MMCM\COMPSCI 1ST YR\2T\IT101-1 Computer Programming Concepts 1\FINAL PROJECT\project\GUI\Issued Books\build\assets\frame0")

def show_issued_books():
    def return_dashboard(window):
        window.destroy()  # Close the current book window
        from dashboard import show_dashboard
        show_dashboard()

    # Placeholder for the currently selected book's ISBN
    selected_book_isbn = None

    book_labels = []  # List to keep track of all book labels

    ISSUED_BOOKS_FILE = 'issued.xlsx'

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def load_books():
        all_books_df = pd.read_excel(ISSUED_BOOKS_FILE)
        current_user = get_current_user()['name']
        return all_books_df[all_books_df['Username'] == current_user]

    # Convert PIL Image to PhotoImage
    def pil_to_photoimage(pil_image):
        return ImageTk.PhotoImage(pil_image)

    def get_random_placeholder():
        placeholders = ['book1.png', 'book2.png', 'book3.png', 'book4.png', 'book5.png']
        selected_placeholder = random.choice(placeholders)
        pil_image = Image.open(relative_to_assets(selected_placeholder)).resize((65, 65))
        return pil_to_photoimage(pil_image)

    def display_book_details(isbn):
        books_df = load_books()
        selected_book = books_df.loc[books_df['ISBN'] == isbn].iloc[0]

        max_length = 30  # Max characters to display
        detail_texts = {
            'ISBN': f"ISBN: {selected_book['ISBN']}",
            'Title': f"Title: {selected_book['Title']}",
            'Author': f"Author: {selected_book['Author']}",
            'Year': f"Year: {selected_book['Year']}",
            'Issue Date': f"Issue Date: {selected_book['Issue Date']}",
            'Due Date': f"Due Date: {selected_book['Due Date']}",
            'Status': f"Status: {selected_book['Status']}"
        }

        for detail, text in detail_texts.items():
            # Truncate the text if it's longer than max_length
            display_text = (text[:max_length - 3] + '...') if len(text) > max_length else text
            detail_labels[detail].config(text=display_text)

    def on_book_click(event, isbn, label):
        global selected_book_isbn
        selected_book_isbn = isbn
        if label.winfo_exists():  # Check if the label still exists
            for lbl in book_labels:
                if lbl.winfo_exists():  # Ensure each label in the loop exists before configuring
                    lbl.config(background="#FFFFFF", foreground="#262626")
            label.config(background="#262626", foreground="#FFFFFF")
        display_book_details(isbn)

    def renew_book():
        global selected_book_isbn
        if selected_book_isbn is None:
            messagebox.showerror("Error", "Please select a book first.")
            return

        books_df = pd.read_excel(ISSUED_BOOKS_FILE)
        book_row = books_df.loc[books_df['ISBN'] == selected_book_isbn]

        if not book_row.empty:
            index = book_row.index[0]
            renewals = book_row.at[index, 'Renewals']
            print(f"Current renewals: {renewals}")
            if renewals < 3:  # Change made here to allow up to 3 renewals
                current_due_date = datetime.strptime(book_row.at[index, 'Due Date'], '%Y-%m-%d')
                new_due_date = current_due_date + timedelta(weeks=1)

                books_df.at[index, 'Due Date'] = new_due_date.strftime('%Y-%m-%d')
                books_df.at[index, 'Renewals'] += 1

                books_df.to_excel(ISSUED_BOOKS_FILE, index=False)
                messagebox.showinfo("Renewed", "The book has been successfully renewed.")
            else:
                messagebox.showwarning("Renewal Limit Reached", "This book cannot be renewed any further.")
        load_and_display_books()
        display_book_details(selected_book_isbn)

    def update_book_status():
        books_df = pd.read_excel(ISSUED_BOOKS_FILE)
        for index, row in books_df.iterrows():
            due_date = datetime.strptime(row['Due Date'], '%Y-%m-%d')
            if due_date < datetime.now():
                books_df.at[index, 'Status'] = 'Overdue'
            else:
                books_df.at[index, 'Status'] = 'Issued'
        books_df.to_excel(ISSUED_BOOKS_FILE, index=False)

    def return_book():
        global selected_book_isbn
        if selected_book_isbn is None:
            messagebox.showerror("Error", "Please select a book first.")
            return

        issued_df = pd.read_excel(ISSUED_BOOKS_FILE)
        # Use selected_book_isbn instead of isbn
        issued_df = issued_df[issued_df['ISBN'] != selected_book_isbn]
        issued_df.to_excel(ISSUED_BOOKS_FILE, index=False)

        books_df = pd.read_excel('books.xlsx')
        book_row_index = books_df[books_df['ISBN'] == selected_book_isbn].index
        if not book_row_index.empty:
            books_df.at[book_row_index[0], 'Available Quantity'] += 1
            books_df.at[book_row_index[0], 'Status'] = 'Available'
            books_df.to_excel('books.xlsx', index=False)

        messagebox.showinfo("Return", "The book has been returned successfully.")
        load_and_display_books()

    # Initiate Issued Books
    window = Tk()
    # Set the dimensions of the window
    window_width = 750
    window_height = 500

    # Calculate x and y coordinates for the Tk window
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)

    # Set the dimensions and position of the window
    window.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
    window.configure(bg = "#FFFFFF")

    window.title("Readify: MMCM Library Management System")

    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 500,
        width = 750,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        750.0,
        64.0,
        fill="#262626",
        outline="")

    canvas.create_text(
        81.0,
        18.0,
        anchor="nw",
        text="Readify Student Issued Books",
        fill="#FFFFFF",
        font=("JostRoman Bold", 25 * -1)
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        249.0,
        283.0,
        image=image_image_1
    )

    canvas.create_text(
        209.0,
        78.0,
        anchor="nw",
        text="My Book List",
        fill="#FFFFFF",
        font=("JostRoman Bold", 20 * -1)
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        619.0,
        164.0,
        image=image_image_2
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=renew_book,
        relief="flat"
    )
    button_1.place(
        x=538.0,
        y=95.0,
        width=162.0,
        height=41.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=return_book,
        relief="flat"
    )
    button_2.place(
        x=538.0,
        y=194.0,
        width=162.0,
        height=42.0
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        619.0,
        175.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        40.0,
        33.0,
        image=image_image_4
    )

    canvas.create_rectangle(
        759.0,
        37.0,
        859.0,
        137.0,
        fill="#FFFFFF",
        outline="")

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: return_dashboard(window),
        relief="flat"
    )
    button_3.place(
        x=687.0,
        y=7.0,
        width=50.0,
        height=50.0
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        619.0,
        376.0,
        image=image_image_5
    )

    canvas.create_text(
        567.0,
        263.0,
        anchor="nw",
        text="Book Details",
        fill="#262626",
        font=("JostRoman Bold", 20 * -1)
    )

    # Add a frame for the books list
    books_frame = ttk.Frame(window)
    books_frame.place(x=30, y=105, width=440, height=370)

    # Create a Canvas inside the frame for drawing the list
    books_canvas = Canvas(books_frame, bg="#FFFFFF")
    books_canvas.pack(side="left", fill="both", expand=True)

    # Add a Scrollbar
    scrollbar = Scrollbar(books_frame, orient=VERTICAL, command=books_canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the canvas
    books_canvas.configure(yscrollcommand=scrollbar.set)
    books_canvas.bind('<Configure>', lambda e: books_canvas.configure(scrollregion=books_canvas.bbox("all")))

    # Add another frame inside the canvas for the items
    books_list_frame = ttk.Frame(books_canvas)
    books_canvas.create_window((0, 0), window=books_list_frame, anchor="nw")

    update_book_status()

    def load_and_display_books():
        books_df = load_books()

        for widget in books_list_frame.winfo_children():
            widget.destroy()

        for index, row in books_df.iterrows():
            book_isbn = row['ISBN']
            book_title = row['Title']
            placeholder_photo = get_random_placeholder()
            book_label = ttk.Label(books_list_frame, image=placeholder_photo,
                                   text=f"{book_title[:30]}\t\t\t\t\t", compound="left", anchor="w",
                                   font=('Arial', 12, 'bold'))
            book_label.pack(fill="x", pady=2)
            # Pass both the isbn and the label itself to the on_book_click function
            book_label.bind("<Button-1>", lambda event, isbn=book_isbn, lbl=book_label: on_book_click(event, isbn, lbl))
            book_label.image = placeholder_photo
            book_labels.append(book_label)

    load_and_display_books()

    # Initialize detail labels
    detail_labels = {}
    y_pos = 290
    for detail in ['ISBN', 'Title', 'Author', 'Year', 'Issue Date', 'Due Date', 'Status']:
        detail_labels[detail] = ttk.Label(window, text=f"{detail}: ", font=('JostRoman Bold', 13))
        detail_labels[detail].place(x=510, y=y_pos)
        y_pos += 28

    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    show_issued_books()