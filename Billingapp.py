from tkinter import *
import random
import sqlite3
from tkinter import messagebox

root = Tk()
root.title('Billing slip')
root.geometry('1280x720')
bg_color = "#5369B1"

#======variables======
c_Name = StringVar()
c_Phone = StringVar()
Item = StringVar()
Rate = IntVar()
Quantity = IntVar()
bill_no = StringVar()
x = random.randint(100, 9999)
bill_no.set(str(x))

global l
l = []

#========Database Setup==========
def setup_db():
    # Create a database connection and setup tables if they don't exist
    conn = sqlite3.connect('billing.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS customers 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bills
                 (bill_no TEXT PRIMARY KEY, customer_id INTEGER, total_amount REAL, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS items
                 (item_id INTEGER PRIMARY KEY AUTOINCREMENT, bill_no TEXT, item_name TEXT, quantity INTEGER, price REAL)''')
    conn.commit()
    conn.close()

setup_db()

#===========functions====

def welcome():
    textarea.delete(1.0, END)
    textarea.insert(END, "\t Welcome to Retails")
    textarea.insert(END, f'\n\n Bill number :\t\t{bill_no.get()}')
    textarea.insert(END, f'\n Customer Name :\t\t{c_Name.get()}')
    textarea.insert(END, f'\n phone number:\t\t{c_Phone.get()}\n')
    textarea.insert(END, f"\n======================================")
    textarea.insert(END, f'\n Product\t\t Qty\t\tPrice')
    textarea.insert(END, f"\n======================================\n")
    textarea.configure(font='arial 15 bold')

def additem():
    n = Rate.get()
    m = Quantity.get() * n
    l.append(m)
    if Item.get() == '':
        messagebox.showerror('Error', 'Please Enter the item')
    else:
        textarea.insert(END, f'{Item.get()}\t\t{Quantity.get()}\t\t{m}\n')

def gbill():
    if c_Name.get() == '' or c_Phone.get() == '':
        messagebox.showerror('Error', 'Customer Details are must')
    else:
        text = textarea.get(10.0, (10.0 + float(len(l))))
        welcome()
        textarea.insert(END, text)
        textarea.insert(END, f"\n======================================\n")
        total_amount = sum(l)
        textarea.insert(END, f"Total Paybill Amount :\t\t\t{total_amount}")
        textarea.insert(END, f"\n======================================")
        savebill(c_Name.get(), c_Phone.get(), total_amount)

def savebill(customer_name, customer_phone, total_amount):
    op = messagebox.askyesno('Save bill', 'Do you want to save the bill?')
    if op > 0:
        # Insert customer details into the database
        conn = sqlite3.connect('billing.db')
        c = conn.cursor()
        c.execute('INSERT INTO customers (name, phone) VALUES (?, ?)', (customer_name, customer_phone))
        conn.commit()
        
        # Get the customer ID
        customer_id = c.lastrowid
        bill_no_str = bill_no.get()

        # Insert bill into bills table
        c.execute('INSERT INTO bills (bill_no, customer_id, total_amount) VALUES (?, ?, ?)', 
                  (bill_no_str, customer_id, total_amount))
        conn.commit()

        # Insert items into items table
        for i in range(len(l)):
            item_name = Item.get()
            quantity = Quantity.get()
            price = Rate.get()
            c.execute('INSERT INTO items (bill_no, item_name, quantity, price) VALUES (?, ?, ?, ?)', 
                      (bill_no_str, item_name, quantity, price))
            conn.commit()
        
        conn.close()

        # Save the bill to a file
        bill_details = textarea.get(1.0, END)
        with open("bills/" + str(bill_no.get()) + ".txt", 'w') as f1:
            f1.write(bill_details)
        
        messagebox.showinfo('Save', f'Bill no :{bill_no.get()} saved successfully')
    else:
        return

def clear():
    c_Name.set('')
    c_Phone.set('')
    Item.set('')
    Rate.set(0)
    Quantity.set(0)
    welcome()

def exit_app():
    op = messagebox.askyesno('Exit', 'Do you really want to exit?')
    if op == True:
        root.quit()

#=========Top Section====

title = Label(root, text='Billing Application', bg=bg_color, fg='white', font=('times new roman', 25, 'bold'), relief=GROOVE, bd=12)
title.pack(fill=X)

#===Customer details======
Frame1 = LabelFrame(root, text='Customer Details', font=('times new roman', 18, 'bold'), relief=GROOVE, bd=10, bg=bg_color, fg='gold')
Frame1.place(x=0, y=80, relwidth=1)

cname_lbl = Label(Frame1, text='Customer name', font=('times new roman', 18, 'bold'), bg=bg_color, fg='white')
cname_lbl.grid(row=0, column=0, padx=10, pady=5)
cname_text = Entry(Frame1, width=15, font='arial 15 bold', relief=SUNKEN, textvariable=c_Name)
cname_text.grid(row=0, column=1, padx=10, pady=5)

cnumber_lbl = Label(Frame1, text='Contact No', font=('times new roman', 18, 'bold'), bg=bg_color, fg='white')
cnumber_lbl.grid(row=0, column=2, padx=10, pady=5)
cnumber_text = Entry(Frame1, width=15, font='arial 15 bold', relief=SUNKEN, textvariable=c_Phone)
cnumber_text.grid(row=0, column=3, padx=10, pady=5)

#=======Product details======
Frame2 = LabelFrame(root, text='Product Details', font=('times new roman', 18, 'bold'), relief=GROOVE, bd=10, bg=bg_color, fg='gold')
Frame2.place(x=20, y=180, width=630, height=520)

pitem = Label(Frame2, text='Product Name', font=('times new roman', 18, 'bold'), bd=10, bg=bg_color, fg='white')
pitem.grid(row=0, column=0, padx=30, pady=20)
pitem_text = Entry(Frame2, width=20, font='arial 15 bold', textvariable=Item)
pitem_text.grid(row=0, column=1, padx=30, pady=20)

prate = Label(Frame2, text='Product Price', font=('times new roman', 18, 'bold'), bd=10, bg=bg_color, fg='white')
prate.grid(row=1, column=0, padx=30, pady=20)
prate_text = Entry(Frame2, width=20, font='arial 15 bold', textvariable=Rate)
prate_text.grid(row=1, column=1, padx=30, pady=20)

pquantity = Label(Frame2, text='Product Quantity', font=('times new roman', 18, 'bold'), bd=10, bg=bg_color, fg='white')
pquantity.grid(row=2, column=0, padx=30, pady=20)
pquantity_text = Entry(Frame2, width=20, font='arial 15 bold', textvariable=Quantity)
pquantity_text.grid(row=2, column=1, padx=30, pady=20)

#======Buttons====

add_btn = Button(Frame2, text='Add Item', font='arial 15 bold', padx=5, pady=10, bg='#F4A460', width=15, command=additem)
add_btn.grid(row=3, column=0, padx=10, pady=30)

print_btn = Button(Frame2, text='Print Bill', font='arial 15 bold', padx=5, pady=10, bg='#F4A460', width=15, command=gbill)
print_btn.grid(row=3, column=1, padx=10, pady=30)

clear_btn = Button(Frame2, text='Clear', font='arial 15 bold', padx=5, pady=10, bg='#F4A460', width=15, command=clear)
clear_btn.grid(row=4, column=0, padx=10, pady=25)

exit_btn = Button(Frame2, text='Exit', font='arial 15 bold', padx=5, pady=10, bg='#F4A460', width=15, command=exit_app)
exit_btn.grid(row=4, column=1, padx=10, pady=25)

#========Bill area====

Frame3 = Frame(root, relief=GROOVE, bd=10)
Frame3.place(x=700, y=180, width=500, height=520)

bill_title = Label(Frame3, text='Bill Area', font='arial 15 bold', relief=GROOVE, bd=7).pack(fill=X)
Scroll_y = Scrollbar(Frame3, orient=VERTICAL)
textarea = Text(Frame3, yscrollcommand=Scroll_y.set)
Scroll_y.pack(side=RIGHT, fill=Y)
Scroll_y.config(command=textarea.yview)
textarea.pack()
welcome()

root.mainloop()
