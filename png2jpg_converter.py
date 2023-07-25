import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ttkthemes import ThemedStyle
from PIL import Image
import os
import time
import math
import webbrowser

def resize_images(input_folder, output_folder, quality, dimensions):
    try:
        png_files = [file for file in os.listdir(input_folder) if file.lower().endswith(".png")]

        if not png_files:
            print(f"No PNG images found in the folder {input_folder}.")
            return

        print(f"{len(png_files)} PNG images are found in the folder {input_folder}...")

        start_time = time.time()

        for file in png_files:
            png_path = os.path.join(input_folder, file)

            img = Image.open(png_path)
            img.load()

            # Resize the image
            img.thumbnail(dimensions)

            jpg_filename = os.path.splitext(file)[0] + ".jpg"
            jpg_path = os.path.join(output_folder, jpg_filename)

            background = Image.new("RGB", dimensions, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # 3 is the alpha channel

            # Save the resized JPG image with the specified quality
            background.save(jpg_path, "JPEG", subsampling=0, quality=quality)
            print(f"Conversion of {file} Complete ...")

        finish_time = time.time()
        duration = math.floor(finish_time - start_time)
        print("Time Taken:", duration, "seconds")
    except Exception as e:
        print("An error occurred:", e)

def browse_folder(entry_widget):
    folder_path = filedialog.askdirectory()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, folder_path)

def start_conversion():
    png_folder = entry_png_folder.get()
    jpg_folder = entry_jpg_folder.get()
    quality = entry_quality.get()
    width = entry_width.get()
    height = entry_height.get()

    if not png_folder:
        update_status("Please Select the PNG folder", "red")
        return
    
    if not jpg_folder:
        update_status("No JPG output folder is provided. Output folder will be created inside the PNG folder", "red")
        jpg_folder = os.path.join(png_folder, "jpg_folder")
        if not os.path.exists(jpg_folder):
            os.makedirs(jpg_folder)

    if not quality:
        update_status("Please input the percentage of quality (1-100)", "red")
        return
    
    if not width:
        update_status("Please specify the width of the image", "red")

        return
    
    if not height:
        update_status("Please specify the height of the image", "red")
        return

    update_status("Conversion in progress...", "red")
    root.update_idletasks()  # Update the status bar immediately

    try:
        quality = int(quality)
        width = int(width)
        height = int(height)
        dimensions = (width, height)

        png_files = [file for file in os.listdir(png_folder) if file.lower().endswith(".png")]

        if not png_files:
            update_status("No PNG images found in the folder", "red")
            return

        total_files = len(png_files)
        for i, file in enumerate(png_files, start=1):
            update_status(f"Processing file {i} of {total_files}...", "red")

            root.update_idletasks()  # Update the status bar immediately

            png_path = os.path.join(png_folder, file)
            img = Image.open(png_path)
            img.load()

            jpg_filename = os.path.splitext(file)[0] + ".jpg"
            jpg_path = os.path.join(jpg_folder, jpg_filename)

            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
            background.save(jpg_path, "JPEG", subsampling=0, quality=quality)

        update_status("Conversion completed successfully.", "green")

    except Exception as e:
        update_status(f"Error: {str(e)}", "red")

# Function to update the status bar
def update_status(message, color="black"):
    status_bar.config(text=message, foreground=color)

# Function to open Links
def open_github():
    webbrowser.open("https://github.com/winsomedesignsautomation", new=2)

def open_zazzle():
    webbrowser.open("https://www.zazzle.com/store/winsome_designs", new=2)

def open_teepublic():
    webbrowser.open("http://tee.pub/lic/WqbFp3hRWTg", new=2)


# Create the main Tkinter window
root = tk.Tk()
root.title("PNG2JPG Image Converter")

# Apply the Equilux theme from ttkthemes
style = ThemedStyle(root)
style.set_theme("xpnative")  # Change the theme here ("equilux" is just an example)

# Center the window on the screen
window_width = 450
window_height = 380
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create a frame to hold the grid
frame = ttk.Frame(root, padding=20)
frame.pack(expand=True, anchor="n")

# Create the UI components
label_png_folder = ttk.Label(frame, text="PNG Folder:")
entry_png_folder = ttk.Entry(frame, width=30)
button_browse_png = ttk.Button(frame, text="Browse", command=lambda: browse_folder(entry_png_folder))

label_jpg_folder = ttk.Label(frame, text="JPG Folder:")
entry_jpg_folder = ttk.Entry(frame, width=30)
button_browse_jpg = ttk.Button(frame, text="Browse", command=lambda: browse_folder(entry_jpg_folder))

label_quality = ttk.Label(frame, text="JPG Quality (1-100):")
entry_quality = ttk.Entry(frame, width=10)

label_dimensions = ttk.Label(frame, text="Image Dimensions:")
label_width = ttk.Label(frame, text="Width:")
entry_width = ttk.Entry(frame, width=10)
label_height = ttk.Label(frame, text="Height:")
entry_height = ttk.Entry(frame, width=10)

button_start_conversion = ttk.Button(frame, text="Start Conversion", command=start_conversion)

status_bar = ttk.Label(frame, text="", anchor=tk.N, style="status.TLabel")

# Grid layout for the UI components
label_png_folder.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_png_folder.grid(row=0, column=1, padx=5, pady=5, sticky="w")
button_browse_png.grid(row=0, column=2, padx=5, pady=5, sticky="w")

label_jpg_folder.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_jpg_folder.grid(row=1, column=1, padx=5, pady=5, sticky="w")
button_browse_jpg.grid(row=1, column=2, padx=5, pady=5, sticky="w")

label_quality.grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_quality.grid(row=2, column=1, padx=5, pady=5, sticky="w")

label_dimensions.grid(row=3, column=0, padx=5, pady=5, sticky="w")

label_width.grid(row=4, column=0, padx=5, pady=5, sticky="w")
entry_width.grid(row=4, column=1, padx=5, pady=5, sticky="w")

label_height.grid(row=5, column=0, padx=5, pady=5, sticky="w")
entry_height.grid(row=5, column=1, padx=5, pady=5, sticky="w")

button_start_conversion.grid(row=6, column=0, columnspan=5, padx=5, pady=10, sticky="ew")

# Status bar
status_bar.grid(row=7, column=0, columnspan=5, padx=5, pady=5, sticky="ew")

# Footer link
footer = ttk.Label(frame, text="© 2023 Winsome Designs Automation", foreground="blue", anchor=tk.N)
footer.grid(row=8, column=0, columnspan=5, padx=5, pady=5, sticky="ew")

# .pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.N)

# Social buttons
social_frame = ttk.Frame(frame)
social_frame.grid(row=9, column=0, columnspan=5, padx=5, pady=5, sticky="n")

github = ttk.Button(social_frame, text="GitHub", command=open_github)
zazzle_store = ttk.Button(social_frame, text="Zazzle Store", command=open_zazzle)
teepublic_store = ttk.Button(social_frame, text="Teepublic Store", command=open_teepublic)

github.pack(padx=5, pady=5, side=tk.LEFT)
zazzle_store.pack(padx=5, pady=5, side=tk.LEFT)
teepublic_store.pack(padx=5, pady=5, side=tk.LEFT)

# Start the Tkinter main loop
root.mainloop()