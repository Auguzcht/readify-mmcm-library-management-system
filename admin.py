from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, ttk, simpledialog, messagebox
import pandas as pd

books_file = 'books.xlsx'

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\MMCM\COMPSCI 1ST YR\2T\IT101-1 Computer Programming Concepts 1\FINAL PROJECT\project\GUI\Admin\build\assets\frame0")

def show_admin():
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def read_books():
        """Read the books from the Excel file into a pandas DataFrame."""
        return pd.read_excel(books_file)

    def populate_book_list():
        """Populate the Treeview with book data."""
        for item in book_list.get_children():
            book_list.delete(item)  # Clear existing entries

        books_df = read_books()  # Assuming read_books returns a DataFrame of book data
        for index, row in books_df.iterrows():
            book_list.insert("", "end", values=(row["ISBN"], row["Title"], row["Author"], row["Year"],row["Total Quantity"], row["Available Quantity"],row["Status"]))

    def add_book(book_details):
        """Add a new book to the Excel file."""
        try:
            books_df = pd.read_excel(books_file, engine='openpyxl')

            # Ensure all ISBN values are treated as strings to prevent type mismatch issues.
            books_df['ISBN'] = books_df['ISBN'].astype(str)

            # Ensure the new book's ISBN is a string for comparison
            new_isbn_str = str(book_details['ISBN'])

            # Check if the new book's ISBN already exists
            if new_isbn_str in books_df['ISBN'].values:
                messagebox.showerror("Error", "A book with this ISBN already exists. Please use a unique ISBN for new books.")
                return

            # Append the new book as it has a unique ISBN
            new_book_df = pd.DataFrame([book_details])  # Create a DataFrame for the new book details
            books_df = pd.concat([books_df, new_book_df], ignore_index=True)  # Use concat for adding new row

            # Save the updated DataFrame back to the Excel file
            books_df.to_excel(books_file, index=False, engine='openpyxl')

            populate_book_list()  # Refresh the book list in the GUI
            messagebox.showinfo("Success", "New book added successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {e}")

    def on_add_book():
        # Step 1: Collect input from the user
        isbn = simpledialog.askstring("Input", "Enter Book ISBN", parent=window)
        title = simpledialog.askstring("Input", "Enter Book Title", parent=window)
        author = simpledialog.askstring("Input", "Enter Book Author", parent=window)
        year = simpledialog.askstring("Input", "Enter Book Year", parent=window)
        total_quantity = simpledialog.askinteger("Input", "Enter Total Quantity", parent=window, minvalue=0)
        available_quantity = simpledialog.askinteger("Input", "Enter Available Quantity", parent=window, minvalue=0,
                                                     maxvalue=total_quantity if total_quantity else 0)

        # Step 2: Create the dictionary
        if all([isbn, title, author, year, total_quantity is not None,
                available_quantity is not None]):  # Ensure all fields are filled
            book_details = {
                'ISBN': isbn,
                'Title': title,
                'Author': author,
                'Year': year,
                'Total Quantity': total_quantity,
                'Available Quantity': available_quantity,
                'Status': "Available" if available_quantity > 0 else "Not Available"
            }

            # Step 3: Call the function with the dictionary
            add_book(book_details)
            populate_book_list()
        else:
            messagebox.showerror("Error", "All fields are required!")

    def get_selected_book():
        """Get the details of the currently selected book."""
        selected_items = book_list.selection()  # Get selected items
        if selected_items:  # If anything is selected
            selected_item = book_list.item(selected_items[0])  # Assume single selection
            return selected_item['values']  # Return the book details
        return None

    def on_delete_book():
        """Placeholder function for deleting a selected book."""
        selected_book = get_selected_book()
        if selected_book:
            # Assuming the first value (ISBN) uniquely identifies the book
            isbn = selected_book[0]
            books_df = read_books()
            books_df = books_df[books_df['ISBN'] != isbn]
            books_df.to_excel(books_file, index=False)
            populate_book_list()
            messagebox.showinfo("Success", "Book deleted successfully")
        else:
            messagebox.showerror("Error", "Please select a book to delete")


    def update_book(original_isbn, updated_book_details):
        """Update details of an existing book."""
        try:
            # Read the books into a DataFrame
            books_df = pd.read_excel(books_file, engine='openpyxl')

            # Ensure ISBNs are strings for comparison
            books_df['ISBN'] = books_df['ISBN'].astype(str)

            # Check if the original ISBN exists
            if original_isbn not in books_df['ISBN'].values:
                messagebox.showerror("Error", "Book to update not found. Please ensure you're editing an existing book.")
                return

            # Prevent changing to an existing ISBN
            if ('ISBN' in updated_book_details and updated_book_details['ISBN'] != original_isbn and
                    updated_book_details['ISBN'] in books_df['ISBN'].values):
                messagebox.showerror("Error",
                                     "Another book with the same ISBN already exists. Please use a different ISBN.")
                return

            # Update the book details
            book_index = books_df.index[books_df['ISBN'] == original_isbn].tolist()
            for index in book_index:
                for key, value in updated_book_details.items():
                    books_df.loc[index, key] = value

            # Save the updated DataFrame back to the Excel file
            books_df.to_excel(books_file, index=False, engine='openpyxl')

            # Refresh the book list in the GUI
            populate_book_list()
            messagebox.showinfo("Success", "Book updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update book: {e}")


    def on_edit_selected():
        selected_book = get_selected_book()
        if selected_book:
            # Extract the original details
            original_isbn = str(selected_book[0])  # Ensuring ISBN is treated as string

            # Ask for new details
            new_isbn = simpledialog.askstring("Input", "Edit Book ISBN (original: " + original_isbn + ")", parent=window,
                                              initialvalue=original_isbn)
            new_title = simpledialog.askstring("Input", "Edit Book Title", parent=window, initialvalue=selected_book[1])
            new_author = simpledialog.askstring("Input", "Edit Book Author", parent=window, initialvalue=selected_book[2])
            new_year = simpledialog.askstring("Input", "Edit Book Year", parent=window, initialvalue=selected_book[3])
            new_total_quantity = simpledialog.askinteger("Input", "Edit Total Quantity", parent=window, minvalue=0,
                                                         initialvalue=selected_book[4])
            new_available_quantity = simpledialog.askinteger("Input", "Edit Available Quantity", parent=window, minvalue=0,
                                                             maxvalue=new_total_quantity, initialvalue=selected_book[5])

            try:
                new_year = int(new_year)  # Explicitly cast to integer
            except ValueError:
                messagebox.showerror("Error", "Year must be a number.")
                return

            # Ensure all fields are filled before proceeding
            if all([new_isbn, new_title, new_author, new_year, new_total_quantity is not None,
                    new_available_quantity is not None]):
                updated_book_details = {
                    'ISBN': new_isbn,
                    'Title': new_title,
                    'Author': new_author,
                    'Year': new_year,
                    'Total Quantity': new_total_quantity,
                    'Available Quantity': new_available_quantity,
                    # Determine status based on available quantity
                    'Status': "Available" if new_available_quantity > 0 else "Not Available"
                }

                # Call the update function with the original ISBN and the updated book details
                update_book(original_isbn, updated_book_details)
            else:
                messagebox.showerror("Error", "All fields are required!")
        else:
            messagebox.showerror("Error", "Please select a book to edit.")


    def on_save_changes():
        """Placeholder function for saving changes."""
        messagebox.showinfo("Info", "Changes are saved.")
        # Save any changes made to the book details to the Excel file and refresh the book list

    def borrow_book(isbn):
        """Decrement available quantity by 1 for a borrowed book."""
        books_df = pd.read_excel(books_file)
        book_row = books_df.loc[books_df['ISBN'] == isbn]
        if not book_row.empty and book_row.iloc[0]['Available Quantity'] > 0:
            index = book_row.index[0]
            books_df.at[index, 'Available Quantity'] -= 1
            books_df.at[index, 'Status'] = "Available" if books_df.at[index, 'Available Quantity'] > 0 else "Not Available"
            books_df.to_excel(books_file, index=False)
            populate_book_list()

    def return_book(isbn):
        """Increment available quantity by 1 for a returned book."""
        books_df = pd.read_excel(books_file)
        book_row = books_df.loc[books_df['ISBN'] == isbn]
        if not book_row.empty:
            index = book_row.index[0]
            books_df.at[index, 'Available Quantity'] += 1
            books_df.at[index, 'Status'] = "Available"
            books_df.to_excel(books_file, index=False)
            populate_book_list()

    def update_book_quantity():
        selected_book = get_selected_book()
        if selected_book:
            isbn = selected_book[0]  # Assuming the first value is the ISBN
            # Fetch current values for total and available quantities
            books_df = pd.read_excel(books_file)
            current_row = books_df.loc[books_df['ISBN'] == isbn]
            if not current_row.empty:
                current_total = current_row.iloc[0]['Total Quantity']
                current_available = current_row.iloc[0]['Available Quantity']
                # Ask for new quantities
                new_total_quantity = simpledialog.askinteger("Update Total Quantity", "Enter new total quantity:", parent=window, initialvalue=current_total)
                if new_total_quantity is None:  # User cancelled the dialog
                    return
                new_available_quantity = simpledialog.askinteger("Update Available Quantity", "Enter new available quantity (must not exceed total quantity):", parent=window, initialvalue=current_available, minvalue=0, maxvalue=new_total_quantity)
                if new_available_quantity is None:  # User cancelled the dialog
                    return
                # Update the DataFrame
                index = current_row.index[0]
                books_df.at[index, 'Total Quantity'] = new_total_quantity
                books_df.at[index, 'Available Quantity'] = new_available_quantity
                books_df.at[index, 'Status'] = "Available" if new_available_quantity > 0 else "Not Available"
                # Save changes back to the Excel file
                books_df.to_excel(books_file, index=False)
                populate_book_list()
                messagebox.showinfo("Success", "Book quantity updated successfully.")
            else:
                messagebox.showerror("Error", "Selected book not found in the database.")
        else:
            messagebox.showerror("Error", "Please select a book to update its quantity.")

    # Admin Panel
    window = Tk()
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
        259.0,
        18.0,
        anchor="nw",
        text="Readify Admin Panel",
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

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        619.0,
        164.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        619.0,
        376.0,
        image=image_image_3
    )

    canvas.create_text(
        209.0,
        78.0,
        anchor="nw",
        text="Book List",
        fill="#FFFFFF",
        font=("JostRoman Bold", 20 * -1)
    )

    canvas.create_text(
        567.0,
        263.0,
        anchor="nw",
        text="Book Details",
        fill="#262626",
        font=("JostRoman Bold", 20 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=on_add_book,
        relief="flat"
    )

    button_1.place(
        x=515.0,
        y=92.0,
        width=100.48309326171875,
        height=44.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=on_delete_book,
        relief="flat"
    )

    button_2.place(
        x=622.5169067382812,
        y=92.0,
        width=100.48309326171875,
        height=44.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=on_edit_selected,
        relief="flat"
    )

    button_3.place(
        x=534.0,
        y=145.0,
        width=162.0,
        height=41.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=on_save_changes,
        relief="flat"
    )

    button_4.place(
        x=534.0,
        y=196.0,
        width=162.0,
        height=41.0
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        40.0,
        33.0,
        image=image_image_4
    )

    # Initialize the Treeview
    book_list = ttk.Treeview(window, columns=("ISBN", "Title", "Author", "Year", "Total Quantity","Available Quantity","Status"), show="headings", height=10)
    book_list.place(x=30, y=105, width=440, height=370)

    # Define the column headings
    book_list.heading("ISBN", text="ISBN")
    book_list.heading("Title", text="Title")
    book_list.heading("Author", text="Author")
    book_list.heading("Year", text="Year")
    book_list.heading("Total Quantity", text="Total")
    book_list.heading("Available Quantity", text="Available")
    book_list.heading("Status", text="Status")

    # Define column widths and alignment
    book_list.column("ISBN", anchor="center", width=50)
    book_list.column("Title", anchor="w", width=50)
    book_list.column("Author", anchor="w", width=50)
    book_list.column("Year", anchor="center", width=50)
    book_list.column("Total Quantity", anchor="center", width=50)
    book_list.column("Available Quantity", anchor="center", width=50)
    book_list.column("Status", anchor="center", width=50)

    # Populate the Treeview with book data
    populate_book_list()

    def display_book_details(event):
        """Display the details of the selected book in the GUI."""
        # Clear existing details
        for label in detail_labels.values():
            label.config(text='')

        # Fetch the selected book
        selected_book = get_selected_book()
        if selected_book:
            # Update the detail labels with the selected book's details
            details = ['ISBN', 'Title', 'Author', 'Year', 'Total Quantity', 'Available Quantity', 'Status']
            max_length = 20  # Max characters to display
            for detail, label in zip(details, detail_labels.values()):
                idx = details.index(detail)
                text = selected_book[idx]
                # If the text is longer than the max_length, truncate and add "..."
                if isinstance(text, str) and len(text) > max_length:
                    text = text[:max_length - 3] + "..."
                label.config(text=f"{detail}: {text}")

    # Assuming you have a dictionary of labels for displaying book details
    detail_labels = {
        'isbn': ttk.Label(window, text='ISBN:', font=('JostRoman Bold', 13)),
        'title': ttk.Label(window, text='Title:', font=('JostRoman Bold', 13)),
        'author': ttk.Label(window, text='Author:', font=('JostRoman Bold', 13)),
        'year': ttk.Label(window, text='Year:', font=('JostRoman Bold', 13)),
        'total_quantity': ttk.Label(window, text='Total Quantity:', font=('JostRoman Bold', 13)),
        'available_quantity': ttk.Label(window, text='Available Quantity:', font=('JostRoman Bold', 13)),
        'status': ttk.Label(window, text='Status:', font=('JostRoman Bold', 13))
    }

    # Place the labels on the GUI
    y_pos = 290
    for label in detail_labels.values():
        label.place(x=510, y=y_pos)
        y_pos += 27

    # Bind the selection event of the Treeview to update the book details
    book_list.bind('<<TreeviewSelect>>', display_book_details)

    window.resizable(width=False, height=False)
    window.mainloop()

if __name__ == "__main__":
    show_admin()