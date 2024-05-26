import sys
sys.path.insert(0, 'Simulation Calculation')
from CalculateProgram import *

import os
import json
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

# Main application class inheriting from tkinter.Tk
class App(tk.Tk):
    def __init__(self, config_path):
        super().__init__()
        self.title("GRA163 Group 3 Simulation")

        # Load configuration from JSON file
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

        # Show the first frame (PageOne) initially
        self.show_frame(0)

    # Function to display a specific frame
    def show_frame(self, page_number):
        frame = self.frames[page_number]
        frame.tkraise()

    # Function to load and resize images
    def load_image(self, path):
        image = Image.open(path)
        resized_image = self.resize_image(image, 1200, 2133)
        return ImageTk.PhotoImage(resized_image)

    # Function to resize images to fit within max_width and max_height
    def resize_image(self, image, max_width, max_height):
        ratio = min(max_width / image.width, max_height / image.height)
        new_size = (int(image.width * ratio), int(image.height * ratio))
        return image.resize(new_size, Image.LANCZOS)

# Base class for each page
class Page(tk.Frame):
    def __init__(self, master, image, page_number, config):
        super().__init__(master)
        self.config = config
        self.page_number = page_number
        self.label = tk.Label(self, image=image)
        self.label.image = image  # Keep a reference to prevent garbage collection
        self.label.pack()
        self.create_widgets()

    # Placeholder for widgets creation, to be overridden by subclasses
    def create_widgets(self):
        pass

    # Utility to set cursor style
    def set_cursor(self, cursor_style):
        self.label.config(cursor=cursor_style)

    # Check if the cursor is in any button area
    def update_cursor(self, event, button_coords):
        for x1, y1, x2, y2 in button_coords:
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.set_cursor("hand2")
                return
        self.set_cursor("")

# Container for different GUI components
class GUIComponents:
    class Button:
        def __init__(self, parent, button_coords, callback):
            self.parent = parent
            self.button_coords = button_coords
            self.callback = callback
            self.bind_events()

        # Bind mouse events to check clicks and update cursor
        def bind_events(self):
            self.parent.label.bind("<Button-1>", self.check_click)
            self.parent.label.bind("<Motion>", self.update_cursor)

        # Check if a button is clicked and call the callback
        def check_click(self, event):
            for i, (x1, y1, x2, y2) in enumerate(self.button_coords):
                if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                    self.callback(i)
                    break

        # Update cursor style based on mouse position
        def update_cursor(self, event):
            for x1, y1, x2, y2 in self.button_coords:
                if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                    self.parent.set_cursor("hand2")
                    return
            self.parent.set_cursor("")

    class TextBox:
        def __init__(self, parent, text_box_areas):
            self.text_boxes = {}
            self.create_text_boxes(parent, text_box_areas)

        # Create text boxes in specified areas
        def create_text_boxes(self, parent, text_box_areas):
            for key, (x1, y1, x2, y2) in text_box_areas.items():
                text_box = tk.Entry(parent, font=("Helvetica", 18, "bold"), bg='#D9D9D9', fg='black',
                                    justify='center', borderwidth=0, highlightthickness=0)
                text_box.place(x=x1, y=y1, width=x2-x1, height=y2-y1)
                self.text_boxes[key] = text_box

    class TextArea:
        def __init__(self, parent, text_areas):
            self.text_labels = []
            self.create_text_areas(parent, text_areas)

        # Create text areas in specified locations
        def create_text_areas(self, parent, text_areas):
            for x1, y1, x2, y2 in text_areas:
                label = tk.Label(parent, font=("Helvetica", 18, "bold"), bg='#D9D9D9', fg='black',
                                 text='', anchor='center')
                label.place(x=x1, y=y1, width=x2-x1, height=y2-y1)
                self.text_labels.append(label)

    class WarningLabel:
        def __init__(self, parent, coords):
            self.labels = [self.create_label(parent, x1, y1, x2, y2) for x1, y1, x2, y2 in coords]

        # Create warning labels in specified locations
        def create_label(self, parent, x1, y1, x2, y2):
            label = tk.Label(parent, font=("Helvetica", 8), fg='red', bg='white', text='', anchor='w')
            label.place(x=x1, y=y1, width=x2-x1, height=y2-y1)
            return label

# PageOne class inheriting from Page
class PageOne(Page):
    def __init__(self, master, image, page_number, config):
        super().__init__(master, image, page_number, config)
        self.load_and_display_additional_image()

    def create_widgets(self):
        super().create_widgets()

        # Load button coordinates from config
        button_coords = [button['coords'] for button in self.config['buttons']['page_one']]
        self.buttons = GUIComponents.Button(self, button_coords, self.check_click)

        # Load text areas from config
        text_areas = [text_area['coords'] for text_area in self.config['text_areas']['page_one']]
        self.text_areas = GUIComponents.TextArea(self, text_areas)

        # Load text box areas from config
        text_box_areas = {box['name']: box['coords'] for box in self.config['text_boxes']['page_one']}
        self.text_boxes = GUIComponents.TextBox(self, text_box_areas)

        # Add warning labels for X_Target and Y_Target
        warning_coords = [label['coords'] for label in self.config['warning_labels']['page_one']]
        self.warning_labels = GUIComponents.WarningLabel(self, warning_coords)

    def load_and_display_additional_image(self):
        img_path_first = self.config["images"]["page_one"]["additional_1"]
        self.place_image(img_path_first, (30, 85), (787, 332), 30, 'photo', 'canvas')

        img_path_second = self.config["images"]["page_one"]["additional_2"]
        self.place_image(img_path_second, (842, 85), (331, 331), 30, 'photo_second', 'canvas_second')

    # Utility to place and display images with rounded corners
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

    # Utility to round corners of an image
    def round_corners(self, image, radius):
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)

        rounded_image = Image.new('RGBA', image.size)
        rounded_image.paste(image, (0, 0), mask=mask)

        return rounded_image

    # Handle button clicks
    def check_click(self, index):
        if index == 0:  # Calculate button
            self.perform_calculate()
        elif index == 1:  # Reset button
            self.perform_reset()
        elif index == 2:  # Manual button
            self.master.show_frame(1)

    # Perform calculation logic
    def perform_calculate(self):
        z_target_text = self.text_boxes.text_boxes['Z_Target'].get()
        y_target_text = self.text_boxes.text_boxes['Y_Target'].get()

        self.warning_labels.labels[0].config(text='')
        self.warning_labels.labels[1].config(text='')

        valid_z = self.validate_input(z_target_text)
        valid_y = self.validate_input(y_target_text)

        if valid_z is not True or valid_y is not True:
            self.perform_reset()
            self.warning_labels.labels[0].config(text=valid_z) if valid_z != True else self.warning_labels.labels[0].config(text='')
            self.warning_labels.labels[1].config(text=valid_y) if valid_y != True else self.warning_labels.labels[1].config(text='')
            return

        if valid_z and valid_y:
            Pitch, Yaw, TargetInside = Calculate(float(z_target_text), float(y_target_text))

            if not TargetInside:
                self.warning_labels.labels[0].config(text="Target is not inside the triangle.")
                self.warning_labels.labels[1].config(text="Target is not inside the triangle.")
                return
            
            self.text_areas.text_labels[0].config(text=f"{Pitch:.2f}")
            self.text_areas.text_labels[1].config(text=f"{Yaw:.2f}")

            self.update_image('photo', 'canvas', 'Picture/Trajectory.png', (30, 85), (787, 332), 30)
            self.update_image('photo_second', 'canvas_second', 'Picture/Target.png', (842, 85), (331, 331), 30)

    # Reset all fields and images
    def perform_reset(self):
        for label in self.text_areas.text_labels:
            label.config(text='')
        for text_box in self.text_boxes.text_boxes.values():
            text_box.delete(0, 'end')
        self.warning_labels.labels[0].config(text='')
        self.warning_labels.labels[1].config(text='')

        self.update_image('photo', 'canvas', 'Picture/EmptyTarjectory.png', (30, 85), (787, 332), 30)
        self.update_image('photo_second', 'canvas_second', 'Picture/EmptyTarget.png', (842, 85), (331, 331), 30)

    # Update displayed image
    def update_image(self, photo_attr_name, canvas_attr_name, img_path, position, size, radius):
        full_path = os.path.abspath(img_path)
        img = Image.open(full_path).convert("RGBA")
        img_resized = self.round_corners(img.resize(size, Image.LANCZOS), radius)
        setattr(self, photo_attr_name, ImageTk.PhotoImage(img_resized))
        canvas = getattr(self, canvas_attr_name)
        canvas.create_image(0, 0, anchor='nw', image=getattr(self, photo_attr_name))

    # Validate input to ensure it is a number
    def validate_input(self, text):
        if text.strip() == "":
            return "Please input a number."
        try:
            float(text)
            return True
        except ValueError:
            return "Only numbers are allowed."

# PageTwo class inheriting from Page
class PageTwo(Page):
    def __init__(self, master, image, page_number, config):
        super().__init__(master, image, page_number, config)
    
    def create_widgets(self):
        button_coords = [button['coords'] for button in self.config['buttons']['page_two']]
        self.buttons = GUIComponents.Button(self, button_coords, self.check_click)

    # Handle button clicks
    def check_click(self, index):
        if index == 0:
            self.master.show_frame(2)
        elif index == 1:
            self.master.show_frame(0)

# PageThree class inheriting from Page
class PageThree(Page):
    def __init__(self, master, image, page_number, config):
        super().__init__(master, image, page_number, config)

    def create_widgets(self):
        button_coords = [button['coords'] for button in self.config['buttons']['page_three']]
        self.buttons = GUIComponents.Button(self, button_coords, self.check_click)

    # Handle button clicks
    def check_click(self, index):
        if index == 0:
            self.master.show_frame(1)
        else:
            self.master.show_frame(0)

# Create the application instance and run the main loop
app = App(config_path="GUI\\config.json")
app.mainloop()
