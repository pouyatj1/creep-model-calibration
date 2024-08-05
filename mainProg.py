# Import necessary libraries
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from creepFitting import creepFit
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np

# Function to handle file selection
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)

# Function to convert plt fig to array
def fig_to_array(fig):
    # Draw the figure on the canvas
    canvas = FigureCanvas(fig)
    canvas.draw()
    
    # Get the RGBA buffer from the figure
    buf = canvas.buffer_rgba()
    
    # Convert to a NumPy array
    image = np.asarray(buf)
    
    return image

# Function to handle processing
def process_data():
    # Read inputs
    file_path = entry_file.get()
    num_set1 = entry_num1.get()
    num_set2 = entry_num2.get()
    option = var_option.get()
    
    # Read Excel file
    df = pd.read_excel(file_path,header=None)
    
    # Process data (user-defined function)
    results, imgPlt = creepFit(df, num_set1, num_set2, option)
    img = fig_to_array(imgPlt)

    
    # Display results and image
    label_result1.config(text=f"C1: {results[0]}")
    label_result2.config(text=f"C2: {results[1]}")
    label_result3.config(text=f"C3: {results[2]}")
    label_result4.config(text=f"C4: {results[3]}")
    
    # Display image
    root.fig = plt.figure()
    plt.imshow(img)
    canvas = FigureCanvasTkAgg(root.fig, master=frame_image)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Function to save the displayed image
def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    root.fig.savefig(file_path)

# Function to handle window close event
def on_closing():
    root.quit()
    root.destroy()

# Setup Tkinter window
root = tk.Tk()
root.title("Creep Calibration")
root.protocol("WM_DELETE_WINDOW", on_closing)

# Create UI elements
label_file = tk.Label(root, text="Select Excel File:")
entry_file = tk.Entry(root, width=50)
button_file = tk.Button(root, text="Browse", command=select_file)

label_num1 = tk.Label(root, text="Input the applied constant stress for each dataset seperated by ',' :",justify='left')
entry_num1 = tk.Entry(root)
entry_num1.insert(0,"5,10,15,20,5,10")

# The temperature input can be changed to be the same format as stress
label_num2 = tk.Label(root, text="Input the temperatures considered for each dataset seperated by ',' :",justify='left')
entry_num2 = tk.Entry(root)
entry_num2.insert( 0,"23,23,23,23,40,40")

var_option = tk.StringVar(value="default")
label_option = tk.Label(root, text="Choose the calibration model:")
radio_default = tk.Radiobutton(root, text="Default", variable=var_option, value="Curve_fit (default)")
radio_lmfit = tk.Radiobutton(root, text="LMFit", variable=var_option, value="LMFIT")

button_process = tk.Button(root, text="Process", command=process_data)

label_result1 = tk.Label(root, text="C1: ")
label_result2 = tk.Label(root, text="C2: ")
label_result3 = tk.Label(root, text="C3: ")
label_result4 = tk.Label(root, text="C4: ")

frame_image = tk.Frame(root)
button_save = tk.Button(root, text="Save Image", command=save_image)

# Place UI elements on the window
label_file.grid(row=0, column=0, padx=10, pady=5)
entry_file.grid(row=0, column=1, padx=10, pady=5)
button_file.grid(row=0, column=2, padx=10, pady=5)

label_num1.grid(row=1, column=0, padx=10, pady=5)
entry_num1.grid(row=1, column=1, padx=10, pady=5)

label_num2.grid(row=2, column=0, padx=10, pady=5)
entry_num2.grid(row=2, column=1, padx=10, pady=5)


label_option.grid(row=4, column=0, padx=10, pady=5)
radio_default.grid(row=4, column=1, padx=10, pady=5)
radio_lmfit.grid(row=4, column=2, padx=10, pady=5)

button_process.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

label_result1.grid(row=6, column=0, columnspan=3, padx=10, pady=5)
label_result2.grid(row=7, column=0, columnspan=3, padx=10, pady=5)
label_result3.grid(row=8, column=0, columnspan=3, padx=10, pady=5)
label_result4.grid(row=9, column=0, columnspan=3, padx=10, pady=5)

frame_image.grid(row=0, column=3, rowspan=10, padx=10, pady=10)
button_save.grid(row=10, column=0, columnspan=3, padx=10, pady=10)

# Main loop
root.mainloop()
