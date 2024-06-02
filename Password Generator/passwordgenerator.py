import random
import string
import tkinter as tk
import pyperclip

class PasswordGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Password Generator")
        master.geometry("400x350")
        master.resizable(False, False)
        master.configure(bg="#f0f0f0")

        self.password_history = []

        self.frame = tk.Frame(master, padx=20, pady=20, bg="#f0f0f0")
        self.frame.pack(expand=True)

        tk.Label(self.frame, text="Password Length:", bg="#f0f0f0", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
        self.length_entry = tk.Entry(self.frame, width=10, font=("Arial", 12))
        self.length_entry.grid(row=0, column=1, pady=5, sticky="w")

        self.options = [
            (tk.BooleanVar(), "Include Uppercase"),
            (tk.BooleanVar(), "Include Numbers"),
            (tk.BooleanVar(), "Include Symbols")
        ]

        for i, (var, text) in enumerate(self.options, start=1):
            tk.Checkbutton(self.frame, text=text, variable=var, bg="#f0f0f0", font=("Arial", 12), anchor="w").grid(row=i, column=0, columnspan=2, sticky="w")

        self.generate_button = tk.Button(self.frame, text="Generate Password", command=self.generate, bg="#4caf50", fg="white", font=("Arial", 12, "bold"))
        self.generate_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="w")

        self.result_label = tk.Label(self.frame, text="", wraplength=300, justify="center", font=("Arial", 14, "bold"), bg="#f0f0f0")
        self.result_label.grid(row=5, column=0, columnspan=2, sticky="w")

        self.copy_button = tk.Button(self.frame, text="Copy to Clipboard", command=self.copy_to_clipboard, bg="#2196f3", fg="white", font=("Arial", 12, "bold"))
        self.copy_button.grid(row=6, column=0, columnspan=2, pady=5, sticky="w")

        self.history_label = tk.Label(self.frame, text="Password History:", font=("Arial", 12, "bold"), bg="#f0f0f0")
        self.history_label.grid(row=7, column=0, columnspan=2, sticky="w")

        self.history_text = tk.Text(self.frame, width=30, height=6, wrap="word", font=("Arial", 12), bg="#ffffff")
        self.history_text.grid(row=8, column=0, columnspan=2, sticky="w")

        master.bind('<Return>', self.generate)

    def generate_password(self, length, *options):
        character_set = string.ascii_lowercase
        for var, chars in zip(options, (string.ascii_uppercase, string.digits, string.punctuation)):
            if var.get():
                character_set += chars

        password = ''.join(random.choice(character_set) for _ in range(length))
        return password

    def generate(self, event=None):
        try:
            length = int(self.length_entry.get())
            if length < 1:
                raise ValueError("Password length must be at least 1")
            password = self.generate_password(length, *map(lambda x: x[0], self.options))
            self.result_label.config(text=password)
        except ValueError as e:
            from tkinter import messagebox
            messagebox.showerror("Invalid Input", str(e))

    def copy_to_clipboard(self):
        password = self.result_label.cget("text")
        pyperclip.copy(password)
        self.password_history.append(password)
        self.update_history_text()
        from tkinter import messagebox
        messagebox.showinfo("Copied", "Password copied to clipboard!")

    def update_history_text(self):
        self.history_text.delete(1.0, tk.END)
        for password in self.password_history:
            self.history_text.insert(tk.END, password + "\n")

root = tk.Tk()
app = PasswordGenerator(root)
root.mainloop()