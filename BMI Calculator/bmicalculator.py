import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

def calculate_bmi(event=None):
    try:
        name, weight, height = entry_name.get().strip(), float(entry_weight.get()), float(entry_height.get())
        if not name or weight <= 0 or height <= 0:
            raise ValueError("Please enter a valid name, weight, and height.")
        bmi = round(weight / (height ** 2), 2)
        category = ("Underweight" if bmi < 18.5 else "Normal weight" if bmi < 24.9 else 
                    "Overweight" if bmi < 29.9 else "Obese")
        messagebox.showinfo("BMI Result", f"Name: {name}\nBMI: {bmi}\nCategory: {category}")
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("400x300")
root.configure(bg="#f7f7f7")

tk.Label(root, text="Name", bg="#f7f7f7", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
entry_name = tk.Entry(root, font=("Arial", 12))
entry_name.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Weight (kg)", bg="#f7f7f7", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
entry_weight = tk.Entry(root, font=("Arial", 12))
entry_weight.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Height (m)", bg="#f7f7f7", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
entry_height = tk.Entry(root, font=("Arial", 12))
entry_height.grid(row=2, column=1, padx=10, pady=10)

tk.Button(root, text="Calculate BMI", command=calculate_bmi, bg="#87cefa", font=("Arial", 12)).grid(row=3, column=0, columnspan=2, padx=10, pady=20)

root.bind('<Return>', calculate_bmi)
root.mainloop()
