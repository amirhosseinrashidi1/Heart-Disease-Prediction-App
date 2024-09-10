import tkinter as tk
from tkinter import messagebox, PhotoImage
import numpy as np
import pickle
import json
import csv
import os

# Load the model
def load_model():
    return pickle.load(open('heart_disease_model.pkl', 'rb'))

# Load the factors from JSON file
def load_factors():
    with open('factors.json', 'r') as file:
        data = json.load(file)
        return data['factors']

# Save patient record to CSV
def save_record(name, features, prediction):
    headers = [factor['name'] for factor in factors]
    file_exists = os.path.isfile('people.csv')
    with open('people.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write header if file does not exist
        if not file_exists:
            writer.writerow(headers + ['Prediction'])
        # Write the patient's record
        writer.writerow([name] + features[0].tolist() + [prediction])

# Predict disease
def predict_disease():
    try:
        # Get input data from the form
        name = entry_name.get()  # Get the patient's name
        features = [float(entry_age.get())]  # Start with age for simplicity

        # Append other features based on factors
        for factor in factors[2:]:  # Skip the first two which are name and age
            if factor['type'] == 'number':
                features.append(float(entries[factor['name']].get()))
            elif factor['type'] == 'radio':
                features.append(int(vars[factor['name']].get()))
        
        final_features = [np.array(features)]
        
        # Load the model
        model = load_model()
        
        # Make prediction
        prediction = model.predict(final_features)[0]
        
        # Generate the appropriate message
        if prediction == 1:
            result = f"Patient Name: {name}\nUnfortunately, you are predicted to have heart disease. Please consult a doctor."
        else:
            result = f"Patient Name: {name}\nCongratulations! You are healthy."
        
        # Display the result
        messagebox.showinfo("Prediction Result", result)
        
        # Save record to CSV
        save_record(name, final_features, prediction)
    
    except ValueError:
        messagebox.showerror("Error", "Please enter valid values.")

def clear_form():
    # Clear all entry fields and reset variables
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    for factor in factors:
        if factor['type'] == 'radio':
            vars[factor['name']].set(0)
        else:
            entries[factor['name']].delete(0, tk.END)

def on_entry_click(event):
    if event.widget.get() == "Required - Please enter in English":
        event.widget.delete(0, tk.END)  # Delete the placeholder text
        event.widget.config(fg='black')  # Set the text color to black

def on_focus_out(event):
    if event.widget.get() == '':
        event.widget.insert(0, "Required - Please enter in English")
        event.widget.config(fg='grey')  # Set the text color to grey

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"

def focus_prev_widget(event):
    event.widget.tk_focusPrev().focus()
    return "break"

def create_tooltip(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry(f"+{widget.winfo_rootx() + widget.winfo_width()}+{widget.winfo_rooty() + widget.winfo_height()}")
    label = tk.Label(tooltip, text=text, background="lightyellow", relief="solid", borderwidth=1)
    label.pack()

def on_enter(event, text):
    create_tooltip(event.widget, text)

def on_leave(event):
    for widget in event.widget.winfo_children():
        widget.destroy()

# Create the Tkinter interface
root = tk.Tk()
root.title("Heart Disease Prediction")

# Set fixed dimensions for the window
root.geometry("1000x900")  # Increased size for better fit
root.resizable(False, False)  # Disable resizing

# Colors based on logo theme
bg_color = "#f0f4f8"  # Light greyish-blue background color
form_bg_color = "#d0e3f0"  # Slightly darker background for form area
text_color = "#333333"  # Dark grey text color
button_color = "#0044cc"  # Dark blue button color
button_text_color = "#ffffff"  # White text on button

# Set background color for the entire window
root.configure(bg=bg_color)

# Create a frame for the title and logo
header_frame = tk.Frame(root, height=150, bg=bg_color)
header_frame.grid(row=0, column=0, columnspan=2, sticky='ew')

# Load and resize the image
logo = PhotoImage(file='heart.png').subsample(16, 16)  # Adjust subsample factor to resize the image

# Add title and logo to the header frame on the left side
tk.Label(header_frame, image=logo, bg=bg_color).pack(side=tk.LEFT, padx=10)
tk.Label(header_frame, text="Heart Disease Prediction", font=('Helvetica', 30), bg=bg_color, fg=text_color).pack(side=tk.LEFT, padx=10)  # Font size set to 30

# Load factors from JSON
factors = load_factors()

# Create a frame for the form
form_frame = tk.Frame(root, padx=20, pady=20, bg=form_bg_color)
form_frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

# Labels and input fields with additional factors
font_label = ('Helvetica', 12)
font_button = ('Helvetica', 14)

# Define input field size
input_width = 50  # Increased width for better readability
input_height = 2  # Increased height to display placeholder text

# Dictionaries to hold entry fields and variables
entries = {}
vars = {}

# Function to create input fields with placeholder text
def create_input_field(row, label_text, factor):
    tk.Label(form_frame, text=label_text, font=font_label, bg=form_bg_color, fg=text_color, anchor='w').grid(row=row, column=0, padx=10, pady=5, sticky='w')  # Align text to the left
    entry = tk.Entry(form_frame, width=input_width, font=('Helvetica', 12), fg='grey', bd=2, relief='solid')
    entry.insert(0, "Required - Please enter in English")
    entry.bind('<FocusIn>', on_entry_click)
    entry.bind('<FocusOut>', on_focus_out)
    entry.bind('<Tab>', focus_next_widget)  # Handle Tab key
    entry.bind('<Return>', focus_next_widget)  # Handle Enter key
    entry.grid(row=row, column=1, padx=10, pady=5, sticky='w')  # Align entry to the left
    if 'tooltip' in factor:
        entry.bind('<Enter>', lambda e, t=factor['tooltip']: on_enter(e, t))
        entry.bind('<Leave>', on_leave)
    entries[factor['name']] = entry

# Function to create radio buttons with variables
def create_radio_buttons(row, label_text, options, var, factor):
    tk.Label(form_frame, text=label_text, font=font_label, bg=form_bg_color, fg=text_color, anchor='w').grid(row=row, column=0, padx=10, pady=5, sticky='w')  # Align text to the left
    for i, (text, value) in enumerate(options.items()):
        rb = tk.Radiobutton(form_frame, text=text, variable=var, value=value, bg=form_bg_color, fg=text_color, font=font_label)
        rb.grid(row=row, column=1+i, padx=5, pady=5, sticky='w')
        if 'tooltip' in factor:
            rb.bind('<Enter>', lambda e, t=factor['tooltip']: on_enter(e, t))
            rb.bind('<Leave>', on_leave)

# Create input fields and radio buttons based on JSON
for index, factor in enumerate(factors):
    if factor['type'] == 'text' or factor['type'] == 'number':
        create_input_field(index, factor['name'] + ":", factor)
    elif factor['type'] == 'radio':
        var = tk.IntVar()
        vars[factor['name']] = var
        create_radio_buttons(index, factor['name'] + ":", factor['options'], var, factor)

# Buttons for prediction and clearing the form
tk.Button(form_frame, text="Predict", command=predict_disease, font=font_button, bg=button_color, fg=button_text_color).grid(row=len(factors), column=0, padx=10, pady=10, sticky='w')
tk.Button(form_frame, text="Clear", command=clear_form, font=font_button, bg="#cc0000", fg=button_text_color).grid(row=len(factors), column=1, padx=10, pady=10, sticky='w')

# Configure grid row and column weights to expand properly
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
form_frame.grid_rowconfigure(len(factors), weight=1)
form_frame.grid_columnconfigure(0, weight=1)
form_frame.grid_columnconfigure(1, weight=1)

# Run the Tkinter event loop
root.mainloop()
