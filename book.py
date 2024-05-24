from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, ttk, messagebox, Scrollbar, VERTICAL
from PIL import Image, ImageTk
import pandas as pd
import random
from datetime import datetime, timedelta
from user_state import get_current_user

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\MMCM\COMPSCI 1ST YR\2T\IT101-1 Computer Programming Concepts 1\FINAL PROJECT\project\GUI\Books\build\assets\frame0")

def show_book():
    # Placeholder for the currently selected book's ISBN
    selected_book_isbn = [None]

    book_labels = []  # List to keep track of all book labels

    def return_dashboard(window):
        window.destroy()  # Close the current book window
        from dashboard import show_dashboard
        show_dashboard()  # Open the dashboard window

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    # Load books from Excel file
    def load_books():
        return pd.read_excel('books.xlsx')

    # Convert PIL Image to PhotoImage
    def pil_to_photoimage(pil_image):
        return ImageTk.PhotoImage(pil_image)

    def update_book_quantity(isbn, decrement=True):
        books_df = load_books()
        book_row = books_df.loc[books_df['ISBN'] == isbn]
        if not book_row.empty:
            index = book_row.index[0]
            if decrement:
                new_available = book_row.at[index, 'Available Quantity'] - 1
                books_df.at[index, 'Available Quantity'] = new_available
                books_df.at[index, 'Status'] = "Not Available" if new_available <= 0 else "Available"
            books_df.to_excel('books.xlsx', index=False)

    def borrow_book():
        global selected_book_isbn
        if selected_book_isbn is None:
            messagebox.showerror("Error", "Please select a book first.")
            return

        books_df = load_books()
        selected_book_row = books_df.loc[books_df['ISBN'] == selected_book_isbn]
        if selected_book_row.empty:
            messagebox.showerror("Error", "Book not found.")
            return

        selected_book = selected_book_row.iloc[0]
        if selected_book['Available Quantity'] > 0:
            confirm = messagebox.askyesno("Confirm Borrow", f"Do you want to borrow '{selected_book['Title']}'?")
            if confirm:
                update_book_quantity(selected_book_isbn)
                # Append book borrowing information to issued.xlsx
                issue_date = datetime.now().strftime('%Y-%m-%d')
                due_date = (datetime.now() + timedelta(weeks=2)).strftime('%Y-%m-%d')
                user_name = get_current_user()['name']  # Assuming this function exists and returns user info
                new_record = pd.DataFrame({
                    'Username': [user_name],
                    'ISBN': [selected_book['ISBN']],
                    'Title': [selected_book['Title']],
                    'Author': [selected_book['Author']],
                    'Year': [selected_book['Year']],
                    'Issue Date': [issue_date],
                    'Due Date': [due_date],
                    'Renewals': [1]
                })
                try:
                    issued_books_df = pd.read_excel('issued.xlsx')
                    issued_books_df = pd.concat([issued_books_df, new_record], ignore_index=True)
                except FileNotFoundError:
                    issued_books_df = new_record
                issued_books_df.to_excel('issued.xlsx', index=False)

                messagebox.showinfo("Borrowed", f"You have borrowed '{selected_book['Title']}'.")
                # Refresh the books list and details
                display_book_details(selected_book_isbn)  # Pass the ISBN of the book to directly show updated details
        else:
            messagebox.showerror("Unavailable", "This book is currently not available for borrowing.")

    def on_book_click(event, isbn, label):
        global selected_book_isbn
        selected_book_isbn = isbn
        for lbl in book_labels:
            lbl.config(background="#FFFFFF", foreground="#262626")  # Adjust colors as needed
        # Highlight the selected label by changing its background color
        label.config(background="#262626",
                     foreground="#FFFFFF")  # Adjust colors as needed
        display_book_details(isbn)

    # Placeholder image for books
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
            'isbn': f"ISBN: {selected_book['ISBN']}",
            'title': f"Title: {selected_book['Title']}",
            'author': f"Author: {selected_book['Author']}",
            'year': f"Year: {selected_book['Year']}",
            'available_quantity': f"Available Quantity: {selected_book['Available Quantity']}",
            'status': f"Status: {selected_book['Status']}"
        }

        for detail, text in detail_texts.items():
            # Truncate the text if it's longer than max_length
            display_text = (text[:max_length - 3] + '...') if len(text) > max_length else text
            detail_labels[detail].config(text=display_text)

    # Books Window
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
        text="Readify Student Library",
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
        text="Book List",
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
        command=borrow_book,
        relief="flat"
    )
    button_1.place(
        x=538.0,
        y=98.0,
        width=163.0,
        height=56.0
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        40.0,
        33.0,
        image=image_image_3
    )

    canvas.create_rectangle(
        759.0,
        37.0,
        859.0,
        137.0,
        fill="#FFFFFF",
        outline="")

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: return_dashboard(window),
        relief="flat"
    )
    button_2.place(
        x=687.0,
        y=7.0,
        width=50.0,
        height=50.0
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        619.0,
        376.0,
        image=image_image_4
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

    # Load books and populate the list
    books_df = load_books()
    for index, row in books_df.iterrows():
        book_isbn = row['ISBN']
        book_title = row['Title']
        placeholder_photo = get_random_placeholder()
        book_label = ttk.Label(books_list_frame, image=placeholder_photo, text=f"{book_title[:30]}\t\t\t",
                               compound="left", anchor="w", font=('Arial', 12, 'bold'))
        book_label.pack(fill="x", pady=2)
        book_label.bind("<Button-1>", lambda event, isbn=book_isbn, lbl=book_label: on_book_click(event, isbn, lbl))
        book_label.image = placeholder_photo
        book_labels.append(book_label)  # Add the label to the list

    detail_labels = {
        'isbn': ttk.Label(window, text='ISBN:', font=('JostRoman Bold', 13)),
        'title': ttk.Label(window, text='Title:', font=('JostRoman Bold', 13)),
        'author': ttk.Label(window, text='Author:', font=('JostRoman Bold', 13)),
        'year': ttk.Label(window, text='Year:', font=('JostRoman Bold', 13)),
        'available_quantity': ttk.Label(window, text='Available Quantity:', font=('JostRoman Bold', 13)),
        'status': ttk.Label(window, text='Status:', font=('JostRoman Bold', 13))
    }

    y_pos = 300
    for label in detail_labels.values():
        label.place(x=510, y=y_pos)
        y_pos += 29

    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    show_book()