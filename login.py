# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 09:39:18 2023

@author: Thomas Vouk
"""
import tkinter as tk
from tkinter import messagebox
import psycopg2
import sys

def database_connection():
    def login(username,password,database="InfraTrans"):
        try:
            # Replace 'your_database', 'your_user', 'your_password', and 'your_host' with your actual PostgreSQL credentials
            connection = psycopg2.connect(
                database=database,
                user=username,
                password=password,
                host="193.171.80.144",
                port="5432"
            )
            cursor = connection.cursor()
    
            # Replace 'users' with your actual table name and 'username' and 'password' with your actual column names
            query = "SELECT * FROM public.country; "
            cursor.execute(query)
    
            # Fetch the result
            result = cursor.fetchone()
            
            
            if result:
                messagebox.showinfo(f"Login Successful", f"Welcome {username}!")
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
    
            # Close the cursor and connection
            cursor.close()
            root.destroy()
            #connection.close()
            print("Login succsesfull!")
            
            return connection
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return connection
            
    
    
    def on_login_button_click():
        
        entered_username = username_entry.get()
        entered_password = password_entry.get()
        entered_database = database_entry.get()
        if entered_database !='oemof':
            entered_database="InfraTrans"
        
        login(entered_username, entered_password,entered_database)
    
    
    # Tkinter setup
    root = tk.Tk()
    root.geometry('650x300')
    root.title("Database login")
    
    # Username Label and Entry
    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()
    
    # Password Label and Entry
    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()
    
    
    #Database Label and Entry
    tk.Label(root, text="Database").pack()
    database_entry = tk.Entry(root)
    database_entry.pack()
    
    
    # Login Button
    login_button = tk.Button(root, text="Login", command=on_login_button_click)
    login_button.pack()
    
    # Run the Tkinter main loop
    root.mainloop()
    
    return 


def main():
    database_connection()


if __name__ == '__main__':

    sys.exit(main())