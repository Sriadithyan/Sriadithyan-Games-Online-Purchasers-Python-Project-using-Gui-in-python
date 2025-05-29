import sqlite3

def connect_db():
    conn = sqlite3.connect("games_store.db")
    cursor = conn.cursor()

    # Create users table with email & mobile
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        mobile TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Create games table with prices in INR
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        game_name TEXT PRIMARY KEY,
        price INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def register_user(email, mobile, password):
    try:
        conn = sqlite3.connect("games_store.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, mobile, password) VALUES (?, ?, ?)", (email, mobile, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def validate_user(email, password):
    conn = sqlite3.connect("games_store.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    result = cursor.fetchone()
    conn.close()
    return result


import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from database import connect_db, register_user, validate_user

connect_db()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Store - Login/Register")
        self.root.geometry("800x600")

        # Load background image
        self.bg_img = Image.open("C:/Users/sriad/Downloads/Rog.png").resize((1600, 1400))
        self.bg_photo = ImageTk.PhotoImage(self.bg_img)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame = tk.Frame(self.root, bg="white", bd=5,width=500,height=350)
        self.frame.pack(pady=200)

        self.init_login_ui()

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def init_login_ui(self):
        self.clear_frame()
        tk.Label(self.frame, text="Login Form", font=("Helvetica", 24, "bold"), fg="#ff5733", bg="white").pack(pady=20)

        tk.Label(self.frame, text="Email", font=("Helvetica", 14), fg="#444444", bg="white").pack(pady=5)
        self.email_entry = tk.Entry(self.frame, font=("Helvetica", 14))
        self.email_entry.pack(pady=5)

        tk.Label(self.frame, text="Password", font=("Helvetica", 14), fg="#444444", bg="white").pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show="*", font=("Helvetica", 14))
        self.password_entry.pack(pady=5)

        tk.Button(self.frame, text="Login", bg="#4CAF50", fg="white", font=("Helvetica", 14),
                  command=self.login_user).pack(pady=10)
        tk.Button(self.frame, text="Register", bg="#2196F3", fg="white", font=("Helvetica", 14),
                  command=self.init_register_ui).pack(pady=5)

    def init_register_ui(self):
        self.clear_frame()
        tk.Label(self.frame, text="Register", font=("Helvetica", 24, "bold"), fg="#ff6600", bg="white").pack(pady=20)

        tk.Label(self.frame, text="Email", font=("Arial", 14), fg="#333333", bg="white").pack()
        self.reg_email = tk.Entry(self.frame, font=("Arial", 12))
        self.reg_email.pack(pady=5)

        tk.Label(self.frame, text="Mobile Number", font=("Arial", 14), fg="#333333", bg="white").pack()
        self.reg_mobile = tk.Entry(self.frame, font=("Arial", 12))
        self.reg_mobile.pack(pady=5)

        tk.Label(self.frame, text="Password", font=("Arial", 14), fg="#333333", bg="white").pack()
        self.reg_pass = tk.Entry(self.frame, show="*", font=("Arial", 12))
        self.reg_pass.pack(pady=5)

        tk.Button(self.frame, text="Create Account", bg="#ff9900", fg="white", font=("Arial", 14),
                  command=self.register_user).pack(pady=10)
        tk.Button(self.frame, text="Back to Login", bg="#cccccc", fg="black", font=("Arial", 12),
                  command=self.init_login_ui).pack(pady=5)

    def login_user(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if validate_user(email, password):
            self.logged_in_user = email
            self.load_store_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")

    def register_user(self):
        email = self.reg_email.get()
        mobile = self.reg_mobile.get()
        password = self.reg_pass.get()

        if register_user(email, mobile, password):
            messagebox.showinfo("Success", "Account created successfully!")
            self.init_login_ui()
        else:
            messagebox.showerror("Error", "Email already exists.")

    def load_store_dashboard(self):
        """Display the game store after login with prices."""
        self.clear_frame()

        tk.Label(self.frame, text=f"Welcome, {self.logged_in_user}", font=("Helvetica", 20, "bold"), fg="#1e90ff",
                 bg="white").pack(pady=20)

        # List of available games with cost in INR
        self.games = {
            "GTA 5 Online":5675,
            "Call of Duty": 4999,
            "FIFA 25": 3999,
            "Cyberpunk 2077": 2999,
            "Minecraft": 1999,
            "Elden Ring": 4499
        }

        self.selected_game = tk.StringVar(value=list(self.games.keys())[0])  # Default selection
        tk.Label(self.frame, text="Select a Game:", font=("Helvetica", 14), bg="white").pack(pady=5)

        game_menu = tk.OptionMenu(self.frame, self.selected_game, *self.games.keys())
        game_menu.pack(pady=5)

        # Display game price dynamically
        def update_price(*args):
            game = self.selected_game.get()
            self.price_label.config(text=f"Price: ₹{self.games[game]}")

        self.selected_game.trace("w", update_price)
        self.price_label = tk.Label(self.frame, text=f"Price: ₹{self.games[list(self.games.keys())[0]]}",
                                    font=("Helvetica", 14), bg="white")
        self.price_label.pack(pady=5)

        tk.Button(self.frame, text="Buy Now", bg="#32cd32", fg="white", font=("Arial", 14),
                  command=self.purchase_game).pack(pady=10)
        tk.Button(self.frame, text="Logout", bg="#ff6347", fg="white", font=("Arial", 14),
                  command=self.init_login_ui).pack(pady=5)

    def purchase_game(self):
        game = self.selected_game.get()
        messagebox.showinfo("Purchase Successful", f"Thank you for purchasing {game} for ₹{self.games[game]}!")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()