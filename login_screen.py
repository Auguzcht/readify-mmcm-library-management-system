from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\MMCM\COMPSCI 1ST YR\2T\IT101-1 Computer Programming Concepts 1\FINAL PROJECT\project\GUI\Login\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Initialize Login
window = Tk()
# Set the dimensions of the window
window_width = 300
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

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 550,
    width = 300,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    150.0,
    276.0,
    image=image_image_1
)
canvas.create_text(
    15.0,
    174.0,
    anchor="nw",
    text="Hey There!",
    fill="#262626",
    font=("JostRoman Bold", 25 * -1)
)
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_1.place(
    x=28.0,
    y=433.0,
    width=246.0,
    height=35.0
)
image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    150.0,
    333.0,
    image=image_image_2
)
canvas.create_text(
    142.0,
    476.0,
    anchor="nw",
    text="Or",
    fill="#262626",
    font=("JostRoman Regular", 13 * -1)
)
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_2.place(
    x=28.0,
    y=501.0,
    width=247.0,
    height=35.0
)
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    165.0,
    300.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=67.0,
    y=287.0,
    width=196.0,
    height=20.0
)
entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    165.0,
    374.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
entry_2.place(
    x=67.0,
    y=360.0,
    width=196.0,
    height=20.0
)

canvas.create_rectangle(
    43.0,
    483.0,
    133.0,
    484.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    163.0,
    483.0,
    253.0,
    484.0,
    fill="#000000",
    outline="")

canvas.create_text(
    15.0,
    211.0,
    anchor="nw",
    text="Welcome back. You are just one step away\nfrom your feed.",
    fill="#000000",
    font=("JostRoman Regular", 13 * -1)
)

canvas.create_text(
    28.0,
    253.0,
    anchor="nw",
    text="Username",
    fill="#000000",
    font=("JostRoman Regular", 13 * -1)
)

canvas.create_text(
    28.0,
    328.0,
    anchor="nw",
    text="Password",
    fill="#000000",
    font=("JostRoman Regular", 13 * -1)
)
window.resizable(False, False)