import sys
sys.path.insert(0, 'Simulation Calculation')
from CalculateProgram import *

import os
import json
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

# Main application class
class App(tk.Tk):
    def __init__(self, config_path):
        super().__init__()
        self.title("GRA163 Group 3 Simulation")

        # Load configuration from a JSON file
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        # Load and resize images for each page
        self.images = [
            self.load_image(self.config["images"]["page_one"]["main"]),
            self.load_image(self.config["images"]["page_two"]["main"]),
            self.load_image(self.config["images"]["page_three"]["main"])
        ]

        # Initialize frames for each page
        self.frames = {}
        for i, page in enumerate([PageOne, PageTwo, PageThree]):
            frame = page(self, self.images[i], i, self.config)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(0)

    # Function to display the specified frame
    def show_frame(self, page_number):
        frame = self.frames[page_number]
        frame.tkraise()

    # Function to load and resize an image
    def load_image(self, path):
        image = Image.open(path)
        resized_image = self.resize_image(image, 1200, 2133)
        return ImageTk.PhotoImage(resized_image)

    # Function to resize an image to fit within specified dimensions
    def resize_image(self, image, max_width, max_height):
        ratio = min(max_width / image.width, max_height / image.height)
        new_size = (int(image.width * ratio), int(image.height * ratio))
        return image.resize(new_size, Image.LANCZOS)

# Base class for each page in the application
class Page(tk.Frame):
    def __init__(self, master, image, page_number, config):
        super().__init__(master)
        self.config = config
        self.page_number = page_number
        self.label = tk.Label(self, image=image)
        self.label.image = image  # Keep a reference!
        self.label.pack()
        self.create_widgets()

    def create_widgets(self):
        pass

    # Utility to set cursor style
    def set_cursor(self, cursor_style):
        self.label.config(cursor=cursor_style)

    # Check if the cursor is in any button area and update cursor style
    def update_cursor(self, event, button_coords):
        for x1, y1, x2, y2 in button_coords:
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.set_cursor("hand2")
                return
        self.set_cursor("")

# Class for the first page of the application
class PageOne(Page):
    def __init__(self, master, image, page_number, config):
        super().__init__(master, image, page_number, config)
        self.load_and_display_additional_image()

    def create_widgets(self):
        super().create_widgets()

        # Load button coordinates from config
        button_coords = [button['coords'] for button in self.config['buttons']['page_one']]

        # Load text areas from config
        self.text_areas = [text_area['coords'] for text_area in self.config['text_areas']['page_one']]

        # Create Label widgets for each area
        self.text_labels = []
        for x1, y1, x2, y2 in self.text_areas:
            label = tk.Label(self, font=("Helvetica", 18, "bold"), bg='#D9D9D9', fg='black',
                             text='', anchor='center')
            label.place(x=x1, y=y1, width=x2-x1, height=y2-y1)
            self.text_labels.append(label)

        # Load text box areas from config
        text_box_areas = {box['name']: box['coords'] for box in self.config['text_boxes']['page_one']}

        # Create Text Box widgets for each area
        self.text_boxes = {}
        for key, (x1, y1, x2, y2) in text_box_areas.items():
            text_box = tk.Entry(self, font=("Helvetica", 18, "bold"), bg='#D9D9D9', fg='black',
                                justify='center', borderwidth=0, highlightthickness=0)
            text_box.place(x=x1, y=y1, width=x2-x1, height=y2-y1)
            self.text_boxes[key] = text_box

        # Add warning labels for X_Target and Y_Target with a white background
        self.warning_label_z = tk.Label(self, font=("Helvetica", 8), fg='red', bg='white', text='', anchor='w')
        self.warning_label_z.place(x=220, y=500, width=270, height=25)

        self.warning_label_y = tk.Label(self, font=("Helvetica", 8), fg='red', bg='white', text='', anchor='w')
        self.warning_label_y.place(x=220, y=577, width=270, height=25)

        # Bind click and motion events
        self.label.bind("<Button-1>", lambda event: self.check_click(event, button_coords))
        self.label.bind("<Motion>", lambda event: self.update_cursor(event, button_coords))

    # Load and display additional images on the page
    def load_and_display_additional_image(self):
        img_path_first = self.config["images"]["page_one"]["additional_1"]
        self.place_image(img_path_first, (30, 85), (787, 332), 30, 'photo', 'canvas')

        img_path_second = self.config["images"]["page_one"]["additional_2"]
        self.place_image(img_path_second, (842, 85), (331, 331), 30, 'photo_second', 'canvas_second')

    # Helper function to place an image on the page
    def place_image(self, img_path, position, size, radius, photo_attr_name, canvas_attr_name):
        img = Image.open(img_path).convert("RGBA")
        img_resized = img.resize(size, Image.LANCZOS)

        if radius:
            img_resized = self.round_corners(img_resized, radius)

        setattr(self, photo_attr_name, ImageTk.PhotoImage(img_resized))

        setattr(self, canvas_attr_name, tk.Canvas(self, width=size[0], height=size[1], bg='white', highlightthickness=0))
        canvas = getattr(self, canvas_attr_name)
        canvas.place(x=position[0], y=position[1])
        canvas.create_image(0, 0, anchor='nw', image=getattr(self, photo_attr_name))

    # Helper function to round the corners of an image
    def round_corners(self, image, radius):
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)

        rounded_image = Image.new('RGBA', image.size)
        rounded_image.paste(image, (0, 0), mask=mask)

        return rounded_image

    # Check if a button was clicked and perform the corresponding action
    def check_click(self, event, coords):
        for i, (x1, y1, x2, y2) in enumerate(coords):
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                if i == 0:  # Calculate
                    self.perform_calculate()
                elif i == 1:  # Reset
                    self.perform_reset()
                elif i == 2:  # Manual
                    self.master.show_frame(1)
                break

    # Perform calculation based on user input
    def perform_calculate(self):
        z_target_text = self.text_boxes['Z_Target'].get()
        y_target_text = self.text_boxes['Y_Target'].get()

        self.warning_label_z.config(text='')
        self.warning_label_y.config(text='')

        valid_z = self.validate_input(z_target_text)
        valid_y = self.validate_input(y_target_text)

        if valid_z is not True:
            self.perform_reset()
            self.warning_label_z.config(text=valid_z)
            return
        if valid_y is not True:
            self.perform_reset()
            self.warning_label_y.config(text=valid_y)
            return

        if valid_z and valid_y:
            Pitch, Yaw, TargetInside = Calculate(float(z_target_text), float(y_target_text))

            if not TargetInside:
                self.warning_label_z.config(text="Target is not inside the triangle.")
                self.warning_label_y.config(text="Target is not inside the triangle.")
                return
            
            self.text_labels[0].config(text=f"{Pitch:.2f}")
            self.text_labels[1].config(text=f"{Yaw:.2f}")

            self.update_image('photo', 'canvas', 'Picture/Trajectory.png', (30, 85), (787, 332), 30)
            self.update_image('photo_second', 'canvas_second', 'Picture/Target.png', (842, 85), (331, 331), 30)

    # Reset the input and output fields
    def perform_reset(self):
        for label in self.text_labels:
            label.config(text='')
        for text_box in self.text_boxes.values():
            text_box.delete(0, 'end')
        self.warning_label_z.config(text='')
        self.warning_label_y.config(text='')

        self.update_image('photo', 'canvas', 'Picture/EmptyTarjectory.png', (30, 85), (787, 332), 30)
        self.update_image('photo_second', 'canvas_second', 'Picture/EmptyTarget.png', (842, 85), (331, 331), 30)

    # Update the displayed image
    def update_image(self, photo_attr_name, canvas_attr_name, img_path, position, size, radius):
        full_path = os.path.abspath(img_path)
        img = Image.open(full_path).convert("RGBA")
        img_resized = self.round_corners(img.resize(size, Image.LANCZOS), radius)
        setattr(self, photo_attr_name, ImageTk.PhotoImage(img_resized))
        canvas = getattr(self, canvas_attr_name)
        canvas.create_image(0, 0, anchor='nw', image=getattr(self, photo_attr_name))

    # Validate user input
    def validate_input(self, text):
        if text.strip() == "":
            return "Please input a number."
        try:
            float(text)
            return True
        except ValueError:
            return "Only numbers are allowed."

# Class for the second page of the application
class PageTwo(Page):
    def create_widgets(self):
        button_coords = [button['coords'] for button in self.config['buttons']['page_two']]
        self.label.bind("<Button-1>", lambda event: self.check_click(event, button_coords))
        self.label.bind("<Motion>", lambda event: self.update_cursor(event, button_coords))

    def check_click(self, event, coords):
        for i, (x1, y1, x2, y2) in enumerate(coords):
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                if i == 0:
                    self.master.show_frame(2)
                elif i == 1:
                    self.master.show_frame(0)
                break

# Class for the third page of the application
class PageThree(Page):
    def create_widgets(self):
        button_coords = [button['coords'] for button in self.config['buttons']['page_three']]
        self.label.bind("<Button-1>", lambda event: self.check_click(event, button_coords))
        self.label.bind("<Motion>", lambda event: self.update_cursor(event, button_coords))

    def check_click(self, event, coords):
        for i, (x1, y1, x2, y2) in enumerate(coords):
            if x1 <= event.x <= x2 and y1 <= y2:
                if i == 0:
                    self.master.show_frame(1)
                else:
                    self.master.show_frame(0)
                break

# Initialize and run the application
app = App(config_path="GUI\\config.json")
app.mainloop()
