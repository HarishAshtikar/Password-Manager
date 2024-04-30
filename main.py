from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import pymongo
import json

cluster = pymongo.MongoClient("mongodb+srv://sgh4r1sh:open7681$@cluster0.qf1azii.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = cluster["PasswordManager"]
collection = db["Passwords"]

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    newdata = {
        website:
        {
        "email": email,
        "password":password
        }
    }

    if len(website) != 0 and len(email) != 0 and len(password) != 0:
        collection.insert_one(newdata)
        website_entry.delete(0, END)
        password_entry.delete(0, END)

    else:
        messagebox.showinfo(title="oops", message="Please don't leave any field empty.")

# ---------------------------- FIND PASSWORD ------------------------------- #
def find():
    website = website_entry.get()
    email = email_entry.get()

    if len(website!=0):
        res = collection.find_one({"website":website, "email":email})
        password = res["password"]
        password_entry.insert(0, password)

    else:
        messagebox.showinfo(title="oops", message="Please don't leave any field empty.")
        
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100,100, image = logo)
canvas.grid(row=0,column = 1)

#labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email / Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

#Entries
website_entry = Entry(width=57)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus() #Imeadeatly places cursor in this entry field when program is run
email_entry = Entry(width=38)
email_entry.grid(row=2, column=1, columnspan=1)
email_entry.insert(0, "harish.ashtikar@gmail.com")
password_entry = Entry(width=38)
password_entry.grid(row=3, column=1)

#Buttons
generate_password = Button(text="Generate Password", command=generate_password)
generate_password.grid(row=3, column=2)
add_button = Button(text="Add", width=48, command=save)
add_button.grid(row=4, column=1, columnspan=2)
search_button = Button(text="Search Password", command=find)
search_button.grid(row=2, column=2)

window.mainloop()