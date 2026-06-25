import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Entry Data")
root.resizable(False, False)

window_width = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width - window_width ) // 2
center_y = int(screen_height / 2 - 600 / 2)
root.geometry(f"+{center_x}+{center_y}")

# Font setting
font_setting = ("Verdana", 20)

# Add a label and entry for Name
tk.Label(root, text="Name:", font=font_setting).grid(row=0, column=0, padx=10, pady=5, sticky="e")
name_entry = tk.Entry(root, font=font_setting)
name_entry.grid(row=0, column=1, padx=10, pady=5)

# Add a label and entry for Address
tk.Label(root, text="Address:", font=font_setting).grid(row=1, column=0, padx=10, pady=5, sticky="e")
address_entry = tk.Entry(root, font=font_setting)
address_entry.grid(row=1, column=1, padx=10, pady=5)

# Add a label and entry for Email
tk.Label(root, text="Email:", font=font_setting).grid(row=2, column=0, padx=10, pady=5, sticky="e")
email_entry = tk.Entry(root, font=font_setting)
email_entry.grid(row=2, column=1, padx=10, pady=5)

# Add a label and entry for Phone number
tk.Label(root, text="Phone number:", font=font_setting).grid(row=3, column=0, padx=10, pady=5, sticky="e")
phone_entry = tk.Entry(root, font=font_setting)
phone_entry.grid(row=3, column=1, padx=10, pady=5)

# Function to handle submit def submit_data():
name = name_entry.get() 
address=address_entry.get() 
email = email_entry.get()
print("Submitted Info:") 
print (f"Name: {name}")
print (f"Address: {address}") 
print (f"Email: {email}")
# Clear the entries
name_entry.delete(0, tk.END) 
address_entry.delete(0, tk.END) 
email_entry.delete(0, tk.END)
# Submit button
submit_button = tk.Button (root, text="Submit", command=submit_data) 
submit_button.grid(row=3, column=0, columnspan=2, pady=10)



# Run the main loop
root.mainloop()