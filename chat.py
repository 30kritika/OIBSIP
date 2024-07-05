import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import json
import os
from PIL import Image, ImageTk
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Setup database connection
conn = sqlite3.connect('chat.db')
cursor = conn.cursor()

# Create users and messages tables
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room TEXT NOT NULL,
    username TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)''')

conn.commit()

# Encryption helper functions
def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ct_bytes

def decrypt_message(encrypted_message, key):
    iv = encrypted_message[:16]
    ct = encrypted_message[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size).decode()

# Main Application
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")

        self.key = b'Sixteen byte key'  # Use a secure method to handle the encryption key

        self.login_screen()

    def login_screen(self):
        self.clear_screen()

        self.username_label = tk.Label(self.root, text="Username")
        self.username_label.pack()

        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Password")
        self.password_label.pack()

        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(self.root, text="Register", command=self.register_screen)
        self.register_button.pack()

    def register_screen(self):
        self.clear_screen()

        self.new_username_label = tk.Label(self.root, text="New Username")
        self.new_username_label.pack()

        self.new_username_entry = tk.Entry(self.root)
        self.new_username_entry.pack()

        self.new_password_label = tk.Label(self.root, text="New Password")
        self.new_password_label.pack()

        self.new_password_entry = tk.Entry(self.root, show="*")
        self.new_password_entry.pack()

        self.register_button = tk.Button(self.root, text="Register", command=self.register)
        self.register_button.pack()

        self.back_button = tk.Button(self.root, text="Back", command=self.login_screen)
        self.back_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            self.chat_screen(username)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

        messagebox.showinfo("Success", "Registration successful")
        self.login_screen()

    def chat_screen(self, username):
        self.clear_screen()

        self.username = username

        self.room_label = tk.Label(self.root, text="Chat Room")
        self.room_label.pack()

        self.room_entry = tk.Entry(self.root)
        self.room_entry.pack()

        self.join_button = tk.Button(self.root, text="Join", command=self.join_room)
        self.join_button.pack()

        self.message_list = tk.Listbox(self.root)
        self.message_list.pack(expand=True, fill=tk.BOTH)

        self.message_entry = tk.Entry(self.root)
        self.message_entry.pack(fill=tk.X, expand=True)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack()

    def join_room(self):
        self.room = self.room_entry.get()
        self.load_messages()

    def load_messages(self):
        self.message_list.delete(0, tk.END)
        cursor.execute("SELECT * FROM messages WHERE room = ?", (self.room,))
        messages = cursor.fetchall()

        for message in messages:
            self.message_list.insert(tk.END, f"{message[2]}: {message[3]}")

    def send_message(self):
        message = self.message_entry.get()
        encrypted_message = encrypt_message(message, self.key)

        cursor.execute("INSERT INTO messages (room, username, message) VALUES (?, ?, ?)", (self.room, self.username, encrypted_message))
        conn.commit()

        self.message_list.insert(tk.END, f"{self.username}: {message}")
        self.message_entry.delete(0, tk.END)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
