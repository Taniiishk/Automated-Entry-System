from customtkinter.windows.widgets.ctk_entry import CTkEntry
import customtkinter as ctk
from customtkinter import *
import datetime
import sqlite3
from tkinter.messagebox import showerror, showinfo, askyesno
from tkinter import ttk
from tkinter import StringVar
from PIL import Image
import cv2

try:
    from pyzbar.pyzbar import decode
except Exception:
    decode = None
import numpy as np
import time
import threading


def init_db():
    try:
        con = sqlite3.connect("secured_sys.db")
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS data (
			uniqid TEXT,
			name TEXT,
			phone_no TEXT,
			vehicle_no TEXT,
			type TEXT,
			description TEXT,
			date TEXT,
			time TEXT
		)""")
        con.commit()
        con.close()
    except Exception as e:
        showerror(
            title="Database Error", message=f"Failed to initialize database:\n{e}"
        )


# Initialize DB on startup
init_db()
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


app = CTk()
# desired window size
win_w, win_h = 700, 560
app.resizable(0, 0)
app.title("login")
# center window on screen
app.update_idletasks()
screen_w = app.winfo_screenwidth()
screen_h = app.winfo_screenheight()
pos_x = int((screen_w - win_w) / 2)
pos_y = int((screen_h - win_h) / 2)
app.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")

try:
    side_img_data = Image.open(
        r"C:\Users\tanis\Downloads\customtkinter-examples-master\customtkinter-examples-master\Login\side-img.png"
    )
    side_img = CTkImage(
        dark_image=side_img_data, light_image=side_img_data, size=(350, 560)
    )
    CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")
except:
    pass

frame = CTkFrame(master=app, width=350, height=560, fg_color="transparent")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

CTkLabel(
    master=frame,
    text="Welcome Back!",
    text_color="#aa58dd",
    anchor="w",
    justify="center",
    font=("Arial Bold", 35),
).pack(anchor="w", pady=(50, 5), padx=(35, 0))
CTkLabel(
    master=frame,
    text="  User ID:",
    text_color="#aa58dd",
    anchor="w",
    justify="left",
    font=("Arial Bold", 14),
).pack(anchor="w", pady=(70, 0), padx=(25, 0))
# store entries so we can read their values
user_entry = CTkEntry(
    master=frame,
    width=275,
    fg_color="#2B2B2B",
    border_color="#601E88",
    border_width=1,
    text_color="#FFFFFF",
)
user_entry.pack(anchor="w", padx=(25, 0))

CTkLabel(
    master=frame,
    text="  Password:",
    text_color="#aa58dd",
    anchor="w",
    justify="left",
    font=("Arial Bold", 14),
).pack(anchor="w", pady=(27, 0), padx=(25, 0))
pass_entry = CTkEntry(
    master=frame,
    width=275,
    fg_color="#2B2B2B",
    border_color="#601E88",
    border_width=1,
    text_color="#FFFFFF",
    show="*",
)
pass_entry.pack(anchor="w", padx=(25, 0))

# error / status label (empty by default)
status_label = CTkLabel(
    master=frame,
    text="",
    text_color="#ff6b6b",
    anchor="w",
    justify="left",
    font=("Arial", 11),
)
status_label.pack(anchor="w", padx=(25, 0), pady=(12, 0))


def check_credentials():
    """Simple credential check. Update the expected values as needed."""
    uid = user_entry.get().strip()
    pwd = pass_entry.get().strip()

    # example hardcoded credentials (change to your auth logic)
    expected_user = "admin"
    expected_pass = "0000"

    if uid == expected_user and pwd == expected_pass:
        status_label.configure(text="Login successful", text_color="#58dd88")
        app.destroy()
        gui()
    else:
        status_label.configure(text="Wrong user id or password", text_color="#ff6b6b")


CTkButton(
    master=frame,
    text="Login",
    fg_color="#aa58dd",
    hover_color="#E44982",
    font=("Arial Bold", 12),
    text_color="#ffffff",
    width=275,
    command=check_credentials,
).pack(anchor="w", pady=(20, 0), padx=(25, 0))


def gui():
    root = CTk()
    root.update_idletasks()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    root.geometry(f"{screen_w}x{screen_h}+0+0")
    root.resizable(1, 1)
    root.title("Main Application")

    lframe = CTkFrame(master=root, width=250, height=screen_h, fg_color="#2A8C55")
    lframe.pack_propagate(0)
    lframe.pack(side="left", fill="y")

    logo_img_data = Image.open(r"C:\Users\tanis\Desktop\entry sys\logo.png")
    logo_img = CTkImage(
        dark_image=logo_img_data, light_image=logo_img_data, size=(105.68, 115.42)
    )
    CTkLabel(master=lframe, text="", image=logo_img).pack(
        pady=(120, 0), anchor="center"
    )

    def close_w():
        root.destroy()

    right_frame = None

    def main_win():
        print("main window")

        uniqid = StringVar()
        name = StringVar()
        phone_no = StringVar()
        vehicle_no = StringVar()
        # type=StringVar()
        description = StringVar()

        def data1():
            X = datetime.datetime.now()
            dd = X.strftime("%A,%d,%b,%Y")
            tt = X.strftime("%X")
            try:
                con = sqlite3.connect("secured_sys.db")
                cur = con.cursor()
                query = "INSERT INTO data VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                cur.execute(
                    query,
                    (
                        uniqid.get(),
                        name.get(),
                        phone_no.get(),
                        vehicle_no.get(),
                        type_entry.get(),
                        description.get(),
                        dd,
                        tt,
                    ),
                )
                con.commit()
                con.close()
                update_metrics()
                showinfo(title="INFORMATION", message="Data inserted.")
                clear_form()
            except Exception as err:
                print(f"Error in data1: {err}")  # Print to console for debugging
                showerror(
                    title="Application Error", message=f"An error occurred:\n{err}"
                )

        nonlocal right_frame

        # destroy previous right frame if present
        if right_frame is not None:
            try:
                right_frame.destroy()
            except Exception:
                pass

        main_framee = CTkFrame(
            master=root,
            width=screen_w - 750,
            height=screen_h,
            border_width=2,
            border_color="black",
        )
        main_framee.pack(side="right", fill="both", expand=True)
        right_frame = main_framee
        CTkLabel(
            master=main_framee, text="RU ORGANIZATION LIMITED", font=("Arial Bold", 50)
        ).pack(pady=50)
        CTkLabel(master=main_framee, text="Welcome", font=("Arial Bold", 40)).place(
            rely=0.14, relx=0.43
        )

        metric1 = CTkFrame(master=main_framee, fg_color="#2A8C55", width=200, height=60)
        metric1.place(rely=0.25, relx=0.17)
        CTkLabel(
            metric1, text="Total Entries", text_color="white", font=("Arial Bold", 14)
        ).place(relx=0.5, rely=0.3, anchor="center")
        total_count_label = CTkLabel(
            metric1, text="0", text_color="white", font=("Arial Bold", 20)
        )
        total_count_label.place(relx=0.5, rely=0.7, anchor="center")

        metric2 = CTkFrame(master=main_framee, fg_color="#2A8C55", width=200, height=60)
        metric2.place(rely=0.25, relx=0.42)
        CTkLabel(
            metric2, text="Entries Today", text_color="white", font=("Arial Bold", 14)
        ).place(relx=0.5, rely=0.3, anchor="center")
        today_count_label = CTkLabel(
            metric2, text="0", text_color="white", font=("Arial Bold", 20)
        )
        today_count_label.place(relx=0.5, rely=0.7, anchor="center")

        metric3 = CTkFrame(master=main_framee, fg_color="#2A8C55", width=200, height=60)
        metric3.place(rely=0.25, relx=0.67)
        CTkLabel(
            metric3, text="Date", text_color="white", font=("Arial Bold", 14)
        ).place(relx=0.5, rely=0.3, anchor="center")
        current_date_label = CTkLabel(
            metric3, text="--", text_color="white", font=("Arial Bold", 15)
        )
        current_date_label.place(relx=0.5, rely=0.7, anchor="center")

        def update_metrics():
            try:
                con = sqlite3.connect("secured_sys.db")
                cur = con.cursor()

                # Total
                cur.execute("SELECT COUNT(*) FROM data")
                total = cur.fetchone()[0]
                total_count_label.configure(text=str(total))

                # Today
                now = datetime.datetime.now()
                dd_str = now.strftime("%A,%d,%b,%Y")
                cur.execute("SELECT COUNT(*) FROM data WHERE date=?", (dd_str,))
                today_cnt = cur.fetchone()[0]
                today_count_label.configure(text=str(today_cnt))

                current_date_label.configure(text=now.strftime("%d %b %Y"))

                con.close()
            except Exception as e:
                print(f"Error updating metrics: {e}")

        # Initial update
        update_metrics()

        inframe = CTkFrame(master=main_framee, fg_color="#1C1B1B", corner_radius=10)
        inframe.place(relx=0.04, rely=0.35, relwidth=0.92, relheight=0.63)

        label_font = ("Arial", 18)
        entry_font = ("Arial", 16)

        # Unique ID
        CTkLabel(
            master=inframe, text="Unique ID", text_color="#CCCCCC", font=label_font
        ).place(relx=0.10, rely=0.15, anchor="w")
        uniqid_entry = CTkEntry(
            master=inframe,
            fg_color="#1a1a1a",
            border_color="#2A8C55",
            border_width=2,
            text_color="#FFFFFF",
            font=entry_font,
            height=35,
            textvariable=uniqid,
        )
        uniqid_entry.place(relx=0.25, rely=0.12, relwidth=0.40)

        # Name
        CTkLabel(
            master=inframe, text="Name", text_color="#CCCCCC", font=label_font
        ).place(relx=0.10, rely=0.30, anchor="w")
        name_entry = CTkEntry(
            master=inframe,
            fg_color="#1a1a1a",
            border_color="#2A8C55",
            border_width=2,
            text_color="#FFFFFF",
            font=entry_font,
            height=35,
            textvariable=name,
        )
        name_entry.place(relx=0.25, rely=0.27, relwidth=0.40)

        # Vehicle No.
        CTkLabel(
            master=inframe, text="Phone No ", text_color="#CCCCCC", font=label_font
        ).place(relx=0.10, rely=0.45, anchor="w")
        phone_entry = CTkEntry(
            master=inframe,
            fg_color="#1a1a1a",
            border_color="#2A8C55",
            border_width=2,
            text_color="#FFFFFF",
            font=entry_font,
            height=35,
            textvariable=phone_no,
        )
        phone_entry.place(relx=0.25, rely=0.42, relwidth=0.40)

        # Phone No.
        CTkLabel(
            master=inframe, text="Vehicle No.", text_color="#CCCCCC", font=label_font
        ).place(relx=0.10, rely=0.60, anchor="w")
        vehicle_entry = CTkEntry(
            master=inframe,
            fg_color="#1a1a1a",
            border_color="#2A8C55",
            border_width=2,
            text_color="#FFFFFF",
            font=entry_font,
            height=35,
            textvariable=vehicle_no,
        )
        vehicle_entry.place(relx=0.25, rely=0.57, relwidth=0.40)

        # Room No.
        CTkLabel(
            master=inframe, text="Type", text_color="#CCCCCC", font=label_font
        ).place(relx=0.10, rely=0.75, anchor="w")
        type_entry = CTkComboBox(
            master=inframe,
            width=125,
            values=["Visit", "Bike", "Car", "delivery", "other"],
            button_color="#2A8C55",
            border_color="#2A8C55",
            border_width=2,
            button_hover_color="#207244",
            dropdown_hover_color="#207244",
            dropdown_fg_color="#2A8C55",
            dropdown_text_color="#fff",
        )
        type_entry.place(relx=0.25, rely=0.72, relwidth=0.40)

        # Owner Name
        CTkLabel(
            master=inframe, text="Description", text_color="#CCCCCC", font=label_font
        ).place(relx=0.10, rely=0.90, anchor="w")
        des_entry = CTkEntry(
            master=inframe,
            fg_color="#1a1a1a",
            border_color="#2A8C55",
            border_width=2,
            text_color="#FFFFFF",
            font=entry_font,
            height=35,
            textvariable=description,
        )
        des_entry.place(relx=0.25, rely=0.87, relwidth=0.40)

        # Buttons on the right side using place()
        def clear_form():
            uniqid_entry.delete(0, "end")
            name_entry.delete(0, "end")
            vehicle_entry.delete(0, "end")
            phone_entry.delete(0, "end")
            des_entry.delete(0, "end")
            type_entry.set("")

        # CTkButton(master=inframe, text="Insert Data", font=("Arial Bold", 18), fg_color="#2A8C55", hover_color="#207244", text_color="#FFFFFF", width=180,height=40,command=data1).place(relx=0.88, rely=0.40, anchor="e")
        CTkButton(
            master=inframe,
            text="Insert Data",
            font=("Arial Bold", 18),
            fg_color="#2A8C55",
            hover_color="#207244",
            text_color="#FFFFFF",
            width=180,
            height=40,
            command=data1,
        ).place(relx=0.88, rely=0.40, anchor="e")

        CTkButton(
            master=inframe,
            text="Clear Form",
            font=("Arial Bold", 18),
            fg_color="#2A8C55",
            hover_color="#207244",
            text_color="#FFFFFF",
            width=180,
            height=40,
            command=clear_form,
        ).place(relx=0.88, rely=0.53, anchor="e")
        # CTkButton(master=inframe, text="View Data", font=("Arial Bold", 18), fg_color="#2A8C55", hover_color="#207244", text_color="#FFFFFF", width=180,height=40).place(relx=0.88, rely=0.62, anchor="e")

    # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def search_data():
        print("search data")

        nonlocal right_frame

        if right_frame is not None:
            try:
                right_frame.destroy()
            except Exception:
                pass

        rframe = CTkFrame(
            master=root,
            width=screen_w - 750,
            height=screen_h,
            border_width=2,
            border_color="black",
        )
        rframe.pack(side="right", fill="both", expand=True)
        right_frame = rframe
        CTkLabel(
            master=rframe, text="RU ORGANIZATION LIMITED", font=("Arial Bold", 50)
        ).pack(pady=50)
        CTkLabel(
            master=rframe,
            text="Search Data",
            font=("Arial Bold", 30),
            text_color="#D4CFCF",
        ).place(rely=0.18, relx=0.41)

        label_font = ("Arial", 18)
        entry_font = ("Arial", 16)

        metric1 = CTkFrame(master=rframe, fg_color="#2A8C55", width=1000, height=60)
        metric1.place(rely=0.25, relx=0.1)

        CTkLabel(
            master=metric1, text="Enter Unique ID or Name ", font=("Arial Bold", 20)
        ).place(relx=0.05, rely=0.25)
        search_entry = CTkEntry(
            master=metric1,
            fg_color="#EFF4F1",
            border_color="#030303",
            border_width=2,
            text_color="#000000",
            font=entry_font,
            height=35,
        )
        search_entry.place(relx=0.32, rely=0.24, relwidth=0.40)

        def fetch_data():
            search_term = search_entry.get()
            if not search_term:
                showerror("Error", "Please enter a Unique ID or Name to search.")
                return

            try:
                con = sqlite3.connect("secured_sys.db")
                cur = con.cursor()
                cur.execute(
                    "SELECT * FROM data WHERE uniqid=? OR name=?",
                    (search_term, search_term),
                )
                row = cur.fetchone()
                con.close()

                if row:
                    # Clear existing
                    uniqid_entry.delete(0, END)
                    name_entry.delete(0, END)
                    phone_entry.delete(0, END)
                    vehicle_entry.delete(0, END)
                    des_entry.delete(0, END)
                    type_entry.delete(0, END)
                    date_entry.delete(0, END)
                    time_entry.delete(0, END)

                    # Insert new data
                    # row: 0=uniqid, 1=name, 2=phone, 3=vehicle, 4=type, 5=desc, 6=date, 7=time
                    uniqid_entry.insert(0, row[0])
                    name_entry.insert(0, row[1])
                    phone_entry.insert(0, row[2])  # phone_no from DB
                    vehicle_entry.insert(0, row[3])  # vehicle_no from DB

                    type_entry.insert(0, row[4])
                    des_entry.insert(0, row[5])
                    date_entry.insert(0, row[6])
                    time_entry.insert(0, row[7])

                else:
                    showinfo("Not Found", "No record found with that ID or Name.")

            except Exception as e:
                showerror(
                    "Database Error", f"An error occurred while fetching data:\n{e}"
                )

        serch_button = CTkButton(
            master=metric1,
            text="Search",
            font=("Arial Bold", 19),
            fg_color="#FBFFFD",
            hover_color="#D4D8D6",
            text_color="#060606",
            width=150,
            height=33,
            command=fetch_data,
        ).place(relx=0.90, rely=0.55, anchor="e")

        inframe = CTkFrame(master=rframe, fg_color="#1C1B1B", corner_radius=10)
        inframe.place(relx=0.04, rely=0.35, relwidth=0.92, relheight=0.63)

        # Unique ID
        CTkLabel(
            master=inframe, text="Unique ID", text_color="#CCCCCC", font=label_font
        ).place(relx=0.08, rely=0.15, anchor="w")
        uniqid_entry = CTkEntry(
            master=inframe,
            fg_color="#1a1a1a",
            border_color="#2A8C55",
            border_width=2,
            text_color="#FFFFFF",
            font=entry_font,
            height=35,
        )
        uniqid_entry.place(relx=0.30, rely=0.12, relwidth=0.40)

        # Name
        CTkLabel(
            master=inframe, text="Name", text_color="#CCCCCC", font=label_font
        ).place(relx=0.08, rely=0.30, anchor="w")
        name_entry = CTkEntry(
            master=inframe,
            fg_color="#1a1a1a",
            border_color="#2A8C55",
            border_width=2,
            text_color="#FFFFFF",
            font=entry_font,
            height=35,
        )
        name_entry.place(relx=0.30, rely=0.27, relwidth=0.40)

        # Vehicle No.
        CTkLabel(
            master=inframe, text="Vehicle No.", text_color="#CCCCCC", font=label_font
        ).place(relx=0.08, rely=0.45, anchor="w")
        phone_entry = CTkEntry(
            master=inframe,
            fg_color="#1a1a1a",
            border_color="#2A8C55",
            border_width=2,
            text_color="#FFFFFF",
            font=entry_font,
            height=35,
        )
        phone_entry.place(relx=0.30, rely=0.42, relwidth=0.40)

        # Phone No.
        CTkLabel(
            master=inframe, text="Phone No.", text_color="#CCCCCC", font=label_font
        ).place(relx=0.08, rely=0.60, anchor="w")
        vehicle_entry = CTkEntry(
            master=inframe,
            fg_color="#1a1a1a",
            border_color="#2A8C55",
            border_width=2,
            text_color="#FFFFFF",
            font=entry_font,
            height=35,
        )
        vehicle_entry.place(relx=0.30, rely=0.57, relwidth=0.40)

        # Room No.
        CTkLabel(
            master=inframe, text="Room No.", text_color="#CCCCCC", font=label_font
        ).place(relx=0.08, rely=0.75, anchor="w")
        type_entry = CTkEntry(
            master=inframe,
            fg_color="#1a1a1a",
            border_color="#2A8C55",
            border_width=2,
            text_color="#FFFFFF",
            font=entry_font,
            height=35,
        )
        type_entry.place(relx=0.30, rely=0.72, relwidth=0.40)

        # Owner Name
        CTkLabel(
            master=inframe, text="Owner Name", text_color="#CCCCCC", font=label_font
        ).place(relx=0.08, rely=0.90, anchor="w")
        des_entry = CTkEntry(
            master=inframe,
            fg_color="#1a1a1a",
            border_color="#2A8C55",
            border_width=2,
            text_color="#FFFFFF",
            font=entry_font,
            height=35,
        )
        des_entry.place(relx=0.30, rely=0.87, relwidth=0.40)

        # Date
        date_entry = CTkEntry(
            master=inframe,
            fg_color="#1C1B1B",
            text_color="#FFFFFF",
            font=("Arial Bold", 16),
        )
        date_entry.place(relx=0.75, rely=0.12, relwidth=0.16)

        # Time
        time_entry = CTkEntry(
            master=inframe,
            fg_color="#1C1B1B",
            text_color="#FFFFFF",
            font=("Arial Bold", 16),
        )
        time_entry.place(relx=0.75, rely=0.20, relwidth=0.16)

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def update_win():

        nonlocal right_frame

        if right_frame is not None:
            try:
                right_frame.destroy()
            except Exception:
                pass

        rframe = CTkFrame(
            master=root,
            width=screen_w - 750,
            height=screen_h,
            border_width=2,
            border_color="black",
        )
        rframe.pack(side="right", fill="both", expand=True)
        right_frame = rframe
        CTkLabel(
            master=rframe, text="RU ORGANIZATION LIMITED", font=("Arial Bold", 50)
        ).pack(pady=50)
        CTkLabel(
            master=rframe,
            text="Modify Data",
            font=("Arial Bold", 30),
            text_color="#D4CFCF",
        ).place(rely=0.18, relx=0.41)

        label_font = ("Arial", 18)
        entry_font = ("Arial", 16)

        metric1 = CTkFrame(master=rframe, fg_color="#2A8C55", width=1000, height=60)
        metric1.place(rely=0.25, relx=0.1)

        CTkLabel(
            master=metric1, text="Enter Unique ID or Name ", font=("Arial Bold", 20)
        ).place(relx=0.05, rely=0.25)
        search_entry = CTkEntry(
            master=metric1,
            fg_color="#EFF4F1",
            border_color="#030303",
            border_width=2,
            text_color="#000000",
            font=entry_font,
            height=35,
        )
        search_entry.place(relx=0.32, rely=0.24, relwidth=0.40)

        searched_uniqid = None

        def fetch_data():
            nonlocal searched_uniqid

            search_term = search_entry.get()
            if not search_term:
                showerror("Error", "Please enter a Unique ID or Name to search.")
                return

            try:
                con = sqlite3.connect("secured_sys.db")
                cur = con.cursor()
                cur.execute(
                    "SELECT * FROM data WHERE uniqid=? OR name=?",
                    (search_term, search_term),
                )
                row = cur.fetchone()
                con.close()

                if row:
                    searched_uniqid = row[0]  # Store the original unique ID
                    # Clear existing

                    uniqid_entry.delete(0, END)
                    name_entry.delete(0, END)
                    phone_entry.delete(0, END)
                    vehicle_entry.delete(0, END)
                    des_entry.delete(0, END)
                    type_entry.delete(0, END)
                    date_entry.delete(0, END)
                    time_entry.delete(0, END)

                    # Insert new data

                    uniqid_entry.insert(0, row[0])
                    name_entry.insert(0, row[1])
                    phone_entry.insert(0, row[2])  # phone_no from DB
                    vehicle_entry.insert(0, row[3])  # vehicle_no from DB

                    type_entry.insert(0, row[4])
                    des_entry.insert(0, row[5])
                    date_entry.insert(0, row[6])
                    time_entry.insert(0, row[7])

                else:
                    showinfo("Not Found", "No record found with that ID or Name.")

            except Exception as e:
                showerror(
                    "Database Error", f"An error occurred while fetching data:\n{e}"
                )

        serch_button = CTkButton(
            master=metric1,
            text="Enter",
            font=("Arial Bold", 19),
            fg_color="#FBFFFD",
            hover_color="#D4D8D6",
            text_color="#060606",
            width=150,
            height=33,
            command=fetch_data,
        ).place(relx=0.90, rely=0.55, anchor="e")

        inframe = CTkFrame(master=rframe, fg_color="#1C1B1B", corner_radius=10)
        inframe.place(relx=0.04, rely=0.35, relwidth=0.92, relheight=0.63)

        # Unique ID
        CTkLabel(
            master=inframe, text="Unique ID", text_color="#CCCCCC", font=label_font
        ).place(relx=0.08, rely=0.15, anchor="w")
        uniqid_entry = CTkEntry(
            master=inframe,
            fg_color="#1a1a1a",
            border_color="#2A8C55",
            border_width=2,
            text_color="#FFFFFF",
            font=entry_font,
            height=35,
        )
        uniqid_entry.place(relx=0.30, rely=0.12, relwidth=0.40)

        # Name
        CTkLabel(
            master=inframe, text="Name", text_color="#CCCCCC", font=label_font
        ).place(relx=0.08, rely=0.30, anchor="w")
        name_entry = CTkEntry(
            master=inframe,
            fg_color="#1a1a1a",
            border_color="#2A8C55",
            border_width=2,
            text_color="#FFFFFF",
            font=entry_font,
            height=35,
        )
        name_entry.place(relx=0.30, rely=0.27, relwidth=0.40)

        # Vehicle No.
        CTkLabel(
            master=inframe, text="Vehicle No.", text_color="#CCCCCC", font=label_font
        ).place(relx=0.08, rely=0.45, anchor="w")
        phone_entry = CTkEntry(
            master=inframe,
            fg_color="#1a1a1a",
            border_color="#2A8C55",
            border_width=2,
            text_color="#FFFFFF",
            font=entry_font,
            height=35,
        )
        phone_entry.place(relx=0.30, rely=0.42, relwidth=0.40)

        # Phone No.
        CTkLabel(
            master=inframe, text="Phone No.", text_color="#CCCCCC", font=label_font
        ).place(relx=0.08, rely=0.60, anchor="w")
        vehicle_entry = CTkEntry(
            master=inframe,
            fg_color="#1a1a1a",
            border_color="#2A8C55",
            border_width=2,
            text_color="#FFFFFF",
            font=entry_font,
            height=35,
        )
        vehicle_entry.place(relx=0.30, rely=0.57, relwidth=0.40)

        # Room No.
        CTkLabel(
            master=inframe, text="Room No.", text_color="#CCCCCC", font=label_font
        ).place(relx=0.08, rely=0.75, anchor="w")
        type_entry = CTkEntry(
            master=inframe,
            fg_color="#1a1a1a",
            border_color="#2A8C55",
            border_width=2,
            text_color="#FFFFFF",
            font=entry_font,
            height=35,
        )
        type_entry.place(relx=0.30, rely=0.72, relwidth=0.40)

        # Owner Name
        CTkLabel(
            master=inframe, text="Owner Name", text_color="#CCCCCC", font=label_font
        ).place(relx=0.08, rely=0.90, anchor="w")
        des_entry = CTkEntry(
            master=inframe,
            fg_color="#1a1a1a",
            border_color="#2A8C55",
            border_width=2,
            text_color="#FFFFFF",
            font=entry_font,
            height=35,
        )
        des_entry.place(relx=0.30, rely=0.87, relwidth=0.40)

        # Date
        date_entry = CTkEntry(
            master=inframe,
            fg_color="#1C1B1B",
            text_color="#FFFFFF",
            font=("Arial Bold", 16),
        )
        date_entry.place(relx=0.75, rely=0.12, relwidth=0.16)

        # Time
        time_entry = CTkEntry(
            master=inframe,
            fg_color="#1C1B1B",
            text_color="#FFFFFF",
            font=("Arial Bold", 16),
        )
        time_entry.place(relx=0.75, rely=0.20, relwidth=0.16)

        def clear_form():
            uniqid_entry.delete(0, "end")
            name_entry.delete(0, "end")
            vehicle_entry.delete(0, "end")
            phone_entry.delete(0, "end")
            des_entry.delete(0, "end")
            type_entry.delete(0, "end")

        def update_data():
            nonlocal searched_uniqid
            if not searched_uniqid:
                showerror("Error", "Please search for a record first.")
                return

            if not askyesno(
                "Confirm Update", "Are you sure you want to update this record?"
            ):
                return

            try:
                con = sqlite3.connect("secured_sys.db")
                cur = con.cursor()

                query = """UPDATE data 
						   SET uniqid=?, name=?, phone_no=?, vehicle_no=?, type=?, description=? 
						   WHERE uniqid=?"""

                cur.execute(
                    query,
                    (
                        uniqid_entry.get(),
                        name_entry.get(),
                        vehicle_entry.get(),
                        phone_entry.get(),
                        type_entry.get(),
                        des_entry.get(),
                        searched_uniqid,
                    ),
                )
                con.commit()
                con.close()

                searched_uniqid = uniqid_entry.get()

                showinfo("Success", "Data updated successfully.")
                clear_form()

            except Exception as e:
                showerror("Database Error", f"Failed to update data:\n{e}")

        def delete_data():
            nonlocal searched_uniqid
            if not searched_uniqid:
                showerror("Error", "Please search for a record first.")
                return

            if not askyesno(
                "Confirm Delete",
                "Are you sure you want to PERMANENTLY delete this record?",
            ):
                return

            try:
                con = sqlite3.connect("secured_sys.db")
                cur = con.cursor()
                cur.execute("DELETE FROM data WHERE uniqid=?", (searched_uniqid,))
                con.commit()
                con.close()

                showinfo("Deleted", "Data deleted successfully.")
                clear_form()
                searched_uniqid = None  # Reset

            except Exception as e:
                showerror("Database Error", f"Failed to delete data:\n{e}")

        CTkButton(
            master=inframe,
            text="Update Data",
            font=("Arial Bold", 18),
            fg_color="#2A8C55",
            hover_color="#207244",
            text_color="#FFFFFF",
            width=180,
            height=40,
            command=update_data,
        ).place(relx=0.90, rely=0.40, anchor="e")
        # CTkButton(master=inframe, text="Delete Data", font=("Arial Bold", 18), fg_color="#2A8C55", hover_color="#207244", text_color="#FFFFFF", width=180,height=40, command=delete_data).place(relx=0.90, rely=0.53, anchor="e")
        CTkButton(
            master=inframe,
            text="Clear Form",
            font=("Arial Bold", 18),
            fg_color="#2A8C55",
            hover_color="#207244",
            text_color="#FFFFFF",
            width=180,
            height=40,
            command=clear_form,
        ).place(relx=0.90, rely=0.66, anchor="e")

    def viwe_data():

        nonlocal right_frame

        if right_frame is not None:
            try:
                right_frame.destroy()
            except Exception:
                pass

        rframe = CTkFrame(
            master=root,
            width=screen_w - 750,
            height=screen_h,
            border_width=2,
            border_color="black",
        )
        rframe.pack(side="right", fill="both", expand=True)
        right_frame = rframe

        CTkLabel(
            master=rframe, text="RU ORGANIZATION LIMITED", font=("Arial Bold", 50)
        ).pack(pady=20)
        CTkLabel(master=rframe, text="View Data Records", font=("Arial Bold", 30)).pack(
            pady=10
        )

        # Filter Frame
        filter1 = CTkFrame(master=rframe, fg_color="#EFF4F1", width=750, height=40)
        filter1.pack(fill="x", padx=60, pady=10)

        CTkLabel(
            master=filter1,
            text="Filter by Type:",
            font=("Arial", 16),
            text_color="black",
        ).pack(side="left", padx=20, pady=20)

        filter_type_var = StringVar(value="All")
        type_filter = CTkComboBox(
            master=filter1,
            width=350,
            values=["All", "Visit", "Bike", "Car", "delivery", "other"],
            variable=filter_type_var,
            state="readonly",
        )
        type_filter.pack(side="left", padx=10, pady=20)

        def apply_filter():

            selected_type = type_filter.get()

            # Construct Query
            query = "SELECT * FROM data"
            params = []

            if selected_type != "All":
                query += " WHERE type=?"
                params.append(selected_type)

            try:
                con = sqlite3.connect("secured_sys.db")
                cur = con.cursor()
                cur.execute(query, params)
                rows = cur.fetchall()
                con.close()

                for item in tree.get_children():
                    tree.delete(item)

                # Insert new data
                for row in rows:
                    tree.insert("", "end", values=row)

            except Exception as e:
                showerror("Database Error", f"Failed to fetch data:\n{e}")

        CTkButton(
            master=filter1,
            text="Apply Filter",
            font=("Arial Bold", 14),
            command=apply_filter,
        ).pack(side="left", padx=20, pady=20)

        # Treeview Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 12), rowheight=30)
        style.configure("Treeview.Heading", font=("Arial Bold", 13))

        # Treeview Frame
        tree_frame = ctk.CTkFrame(master=rframe)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll_y.pack(side="right", fill="y")

        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")

        # Treeview
        columns = (
            "uniqid",
            "name",
            "phone",
            "vehicle",
            "type",
            "description",
            "date",
            "time",
        )
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
        )

        tree_scroll_y.config(command=tree.yview)
        tree_scroll_x.config(command=tree.xview)

        # Headings
        tree.heading("uniqid", text="Unique ID")
        tree.heading("name", text="Name")
        tree.heading("phone", text="Phone No")
        tree.heading("vehicle", text="Vehicle No")
        tree.heading("type", text="Type")
        tree.heading("description", text="Description")
        tree.heading("date", text="Date")
        tree.heading("time", text="Time")

        # Column config
        tree.column("uniqid", width=100, anchor="center")
        tree.column("name", width=150, anchor="w")
        tree.column("phone", width=120, anchor="center")
        tree.column("vehicle", width=120, anchor="center")
        tree.column("type", width=100, anchor="center")
        tree.column("description", width=200, anchor="w")
        tree.column("date", width=100, anchor="center")
        tree.column("time", width=100, anchor="center")

        tree.pack(fill="both", expand=True)

        apply_filter()

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def view_student_data():
        nonlocal right_frame

        if right_frame is not None:
            try:
                right_frame.destroy()
            except Exception:
                pass

        rframe = CTkFrame(
            master=root,
            width=screen_w - 750,
            height=screen_h,
            border_width=2,
            border_color="black",
        )
        rframe.pack(side="right", fill="both", expand=True)
        right_frame = rframe

        CTkLabel(
            master=rframe, text="RU ORGANIZATION LIMITED", font=("Arial Bold", 50)
        ).pack(pady=20)
        CTkLabel(
            master=rframe, text="Student Entry Logs", font=("Arial Bold", 30)
        ).pack(pady=10)

        # Treeview Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 12), rowheight=30)
        style.configure("Treeview.Heading", font=("Arial Bold", 13))

        # Treeview Frame
        tree_frame = ctk.CTkFrame(master=rframe)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll_y.pack(side="right", fill="y")

        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")

        # Treeview

        columns = ("sr_no", "student_name", "class", "scholar_no", "time", "date")
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
        )

        tree_scroll_y.config(command=tree.yview)
        tree_scroll_x.config(command=tree.xview)

        # Headings
        tree.heading("sr_no", text="Sr No")
        tree.heading("student_name", text="Student Name")
        tree.heading("class", text="Class")
        tree.heading("scholar_no", text="Scholar No")
        tree.heading("time", text="Time")
        tree.heading("date", text="Date")

        # Column config
        tree.column("sr_no", width=50, anchor="center")
        tree.column("student_name", width=200, anchor="w")
        tree.column("class", width=100, anchor="center")
        tree.column("scholar_no", width=150, anchor="center")
        tree.column("time", width=100, anchor="center")
        tree.column("date", width=100, anchor="center")

        tree.pack(fill="both", expand=True)

        # Fetch Data
        try:
            con = sqlite3.connect("students.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM student_entry ORDER BY time ASC")

            rows = cur.fetchall()
            con.close()

            for i, row in enumerate(rows, start=1):
                display_row = (i,) + row[1:]
                tree.insert("", "end", values=display_row)

        except Exception as e:
            showerror("Database Error", f"Failed to fetch student data:\n{e}")

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def dashboard():
        nonlocal right_frame
        if right_frame is not None:
            try:
                right_frame.destroy()
            except Exception:
                pass

        dframe = CTkFrame(
            master=root, width=screen_w - 750, height=screen_h, fg_color="#101010"
        )
        dframe.pack(side="right", fill="both", expand=True)
        right_frame = dframe

        # Title
        CTkLabel(
            master=dframe,
            text="RU ORGANIZATION LIMITED",
            font=("Roboto Medium", 70),
            text_color="#FFFFFF",
        ).place(relx=0.13, rely=0.05)
        CTkLabel(
            master=dframe,
            text="WELCOME",
            font=("Roboto Medium", 45),
            text_color="#FFFFFF",
        ).place(relx=0.40, rely=0.15)
        CTkLabel(
            master=dframe,
            text="Dashboard Overview",
            font=("Roboto", 30),
            text_color="#A0A0A0",
        ).place(relx=0.09, rely=0.29)

        # Card Styles
        card_color = "#1E1E1E"
        accent_color = "#2A8C55"
        title_font = ("Arial Bold", 17)
        value_font = ("Arial Bold", 42)

        # Metric Card 1: Total Entries
        m1_card = CTkFrame(
            master=dframe,
            fg_color=card_color,
            corner_radius=15,
            border_width=2,
            border_color="#333333",
        )
        m1_card.place(relx=0.09, rely=0.35, relwidth=0.22, relheight=0.16)

        CTkLabel(
            m1_card, text="TOTAL ENTRIES", text_color="#A09F9F", font=title_font
        ).place(relx=0.5, rely=0.25, anchor="center")
        lbl_total = CTkLabel(
            m1_card, text="0", text_color=accent_color, font=value_font
        )
        lbl_total.place(relx=0.5, rely=0.60, anchor="center")

        # Metric Card 2: Entries Today
        m2_card = CTkFrame(
            master=dframe,
            fg_color=card_color,
            corner_radius=15,
            border_width=2,
            border_color="#333333",
        )
        m2_card.place(relx=0.39, rely=0.35, relwidth=0.22, relheight=0.16)

        CTkLabel(
            m2_card, text="ENTRIES TODAY", text_color="#A09F9F", font=title_font
        ).place(relx=0.5, rely=0.25, anchor="center")
        lbl_today = CTkLabel(
            m2_card, text="0", text_color=accent_color, font=value_font
        )
        lbl_today.place(relx=0.5, rely=0.60, anchor="center")

        # Metric Card 3: Date
        m3_card = CTkFrame(
            master=dframe,
            fg_color=card_color,
            corner_radius=15,
            border_width=2,
            border_color="#333333",
        )
        m3_card.place(relx=0.69, rely=0.35, relwidth=0.22, relheight=0.16)

        CTkLabel(m3_card, text="DATE", text_color="#A09F9F", font=title_font).place(
            relx=0.5, rely=0.25, anchor="center"
        )
        lbl_date = CTkLabel(
            m3_card, text="--", text_color=accent_color, font=("Arial Bold", 28)
        )
        lbl_date.place(relx=0.5, rely=0.60, anchor="center")

        def update_dash_metrics():
            try:
                con = sqlite3.connect("secured_sys.db")
                cur = con.cursor()

                # Total
                cur.execute("SELECT COUNT(*) FROM data")
                total = cur.fetchone()[0]
                lbl_total.configure(text=f"{total:,}")

                # Today
                now = datetime.datetime.now()
                dd_str = now.strftime("%A,%d,%b,%Y")
                cur.execute("SELECT COUNT(*) FROM data WHERE date=?", (dd_str,))
                today_cnt = cur.fetchone()[0]
                lbl_today.configure(text=f"{today_cnt:,}")

                # Date
                lbl_date.configure(text=now.strftime("%d %b, %Y").upper())

                con.close()
            except Exception as e:
                print(f"Error updating dashboard: {e}")

        update_dash_metrics()

        # Quick Actions
        CTkLabel(
            master=dframe,
            text="Quick Actions",
            font=("Roboto Medium", 20),
            text_color="#FFFFFF",
        ).place(relx=0.10, rely=0.59)

        btn_font = ("Arial Bold", 20)
        btn_fg = "#2A8C55"
        btn_hover = "#207244"

        # 1. New Entry
        CTkButton(
            master=dframe,
            text="NEW ENTRY",
            font=btn_font,
            fg_color=btn_fg,
            hover_color=btn_hover,
            text_color="white",
            corner_radius=10,
            command=main_win,
        ).place(relx=0.10, rely=0.66, relwidth=0.33, relheight=0.08)

        # 2. Scan ID
        CTkButton(
            master=dframe,
            text="SCAN ID",
            font=btn_font,
            fg_color=btn_fg,
            hover_color=btn_hover,
            text_color="white",
            corner_radius=10,
            command=start_scanner_check,
        ).place(relx=0.58, rely=0.66, relwidth=0.33, relheight=0.08)

        # 3. View Entry Logs
        CTkButton(
            master=dframe,
            text="VIEW ENTRY LOGS",
            font=btn_font,
            fg_color="#3A3A3A",
            hover_color="#505050",
            text_color="white",
            corner_radius=10,
            border_color="#2A8C55",
            border_width=2,
            command=view_student_data,
        ).place(relx=0.10, rely=0.78, relwidth=0.81, relheight=0.09)

    def start_scanner_check():
	if decode is None:
		showerror("Error", "Barcode scanner requires pyzbar library with ZBar DLL.")
		return
		return

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            showerror("Error", "Could not open camera.")
            return

        win_name = "Scan Barcode (Press 'q' to quit)"
        cv2.namedWindow(win_name)

        last_scanned_data = None
        scan_cooldown = 0

        feedback_text = ""
        feedback_color = (0, 0, 0)
        feedback_timer = 0

        while True:
            success, frame = cap.read()
            if not success:
                break

            current_time = time.time()

            decoded_objects = decode(frame)
            for obj in decoded_objects:
                scanned_code = obj.data.decode("utf-8")

                # Visual Box
                points = obj.polygon
                if len(points) == 4:
                    pts = np.array(points, np.int32)
                    pts = pts.reshape((-1, 1, 2))
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 3)
                else:
                    x, y, w, h = obj.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

                if (scanned_code != last_scanned_data) or (
                    current_time - scan_cooldown > 2.0
                ):
                    last_scanned_data = scanned_code
                    scan_cooldown = current_time

                    # Check DB
                    try:
                        con = sqlite3.connect("students.db")
                        cur = con.cursor()
                        cur.execute(
                            "SELECT * FROM Student_Data WHERE Scholar_No=?",
                            (scanned_code,),
                        )
                        row = cur.fetchone()

                        if row:
                            # row: (Sr_No, Student_Name, Father_Name, Class, Scholar_No)
                            feedback_text = f"VERIFIED: {row[1]}"  # Show Name
                            feedback_color = (0, 255, 0)  # Green

                            # Log entry
                            try:
                                now_entry = datetime.datetime.now()
                                date_str = now_entry.strftime(
                                    "%d-%b-%Y"
                                )  # Format matching user pref/other parts if needed, but standard is fine. User asked for date, time.
                                time_str = now_entry.strftime("%H:%M:%S")

                                ins_query = "INSERT INTO student_entry (student_name, class, scholar_no, time, date) VALUES (?, ?, ?, ?, ?)"
                                cur.execute(
                                    ins_query,
                                    (row[1], row[3], row[4], time_str, date_str),
                                )
                                con.commit()
                            except Exception as log_err:
                                print(f"Logging Error: {log_err}")

                        else:
                            feedback_text = "INVALID / NOT FOUND"
                            feedback_color = (0, 0, 255)  # Red

                        con.close()

                        feedback_timer = current_time  # Reset timer

                    except Exception as e:
                        print(e)
                        feedback_text = "DB ERROR"
                        feedback_color = (0, 165, 255)  # Orange

            if (current_time - feedback_timer < 1.5) and feedback_text:
                # Background rectangle for text
                cv2.rectangle(frame, (0, 0), (640, 60), feedback_color, -1)
                cv2.putText(
                    frame,
                    feedback_text,
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (255, 255, 255),
                    2,
                )

            cv2.imshow(win_name, frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    CTkButton(
        master=lframe,
        text="Dashboard",
        fg_color="#F6F7F6",
        border_width=2,
        border_color="#1A1616",
        text_color="#000000",
        font=("Arial Bold", 17),
        hover_color="#A1A4A2",
        anchor="center",
        command=dashboard,
        width=145,
        height=35,
    ).place(rely=0.45, relx=0.15)
    CTkButton(
        master=lframe,
        text="View Data",
        fg_color="#F6F7F6",
        border_width=2,
        border_color="#1A1616",
        text_color="#000000",
        font=("Arial Bold", 17),
        hover_color="#A1A4A2",
        anchor="center",
        command=viwe_data,
        width=145,
        height=35,
    ).place(rely=0.56, relx=0.15)
    CTkButton(
        master=lframe,
        text="Search Data",
        fg_color="#F6F7F6",
        border_width=2,
        border_color="#1A1616",
        text_color="#000000",
        font=("Arial Bold", 17),
        hover_color="#A1A4A2",
        anchor="center",
        command=search_data,
        width=145,
        height=35,
    ).place(rely=0.66, relx=0.15)
    CTkButton(
        master=lframe,
        text="Modify Data",
        fg_color="#F6F7F6",
        border_width=2,
        border_color="#1A1616",
        text_color="#000000",
        font=("Arial Bold", 17),
        hover_color="#A1A4A2",
        anchor="center",
        command=update_win,
        width=145,
        height=35,
    ).place(rely=0.77, relx=0.15)
    CTkButton(
        master=lframe,
        text="Close",
        fg_color="#F6F7F6",
        border_width=2,
        border_color="#1A1616",
        text_color="#000000",
        font=("Arial Bold", 17),
        hover_color="#A1A4A2",
        anchor="center",
        command=close_w,
        width=145,
        height=35,
    ).place(rely=0.88, relx=0.15)

    # show dashboard on startup
    dashboard()

    root.mainloop()


app.mainloop()
