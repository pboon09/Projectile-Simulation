import tkinter as tk
from PIL import Image, ImageTk

def update_coordinates(event):
    # Update the label text to show the current coordinates as the mouse moves
    coordinate_label.config(text=f"Coordinates: ({event.x}, {event.y})")

def click_coordinates(event):
    # Print the coordinates when the image is clicked
    print(f"Clicked at: ({event.x}, {event.y})")

def resize_image(image, max_width, max_height):
    # Maintain aspect ratio of image
    original_width, original_height = image.size
    ratio = min(max_width/original_width, max_height/original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    return resized_image

root = tk.Tk()
root.title("Dynamic Image Coordinate Viewer")

# Define larger dimensions for your image to make it bigger
max_width = 1200  # Increase width as needed
max_height = 2133.33  # Adjust height accordingly to maintain the 9:16 aspect ratio

# Load your image
image = Image.open("Picture\GUI_Page\LandingPage.png")  # Make sure to provide the correct path here
resized_image = resize_image(image, max_width, max_height)
photo = ImageTk.PhotoImage(resized_image)

# Create a label to display the image
image_label = tk.Label(root, image=photo)
image_label.pack()

# Create a label to display coordinates
coordinate_label = tk.Label(root, text="Coordinates: (x, y)", font=("Arial", 12))
coordinate_label.pack()

# Bind the mouse move event to the image label for updating coordinates
image_label.bind("<Motion>", update_coordinates)

# Bind the mouse click event to the image label for printing coordinates
image_label.bind("<Button-1>", click_coordinates)

root.mainloop()
