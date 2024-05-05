import sys
sys.path.insert(0, 'Simulation Calculation')
from CalculateProgram import *

import os
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GRA163 Group 3 Simulation")

        # Load and resize images for each page
        self.images = [self.load_image("Picture\GUI_Page\LandingPage.png"),
                       self.load_image("Picture\GUI_Page\Manual1.png"),
                       self.load_image("Picture\GUI_Page\Manual2.png")]

        # Initialize frames for each page
        self.frames = {}
        for i, page in enumerate([PageOne, PageTwo, PageThree]):
            frame = page(self, self.images[i], i)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(0)

    def show_frame(self, page_number):
        frame = self.frames[page_number]
        frame.tkraise()

    def load_image(self, path):
        image = Image.open(path)
        resized_image = self.resize_image(image, 1200, 2133)
        return ImageTk.PhotoImage(resized_image)

    def resize_image(self, image, max_width, max_height):
        ratio = min(max_width / image.width, max_height / image.height)
        new_size = (int(image.width * ratio), int(image.height * ratio))
        return image.resize(new_size, Image.ANTIALIAS)

class Page(tk.Frame):
    def __init__(self, master, image, page_number):
        super().__init__(master)
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

    # Check if the cursor is in any button area
    def update_cursor(self, event, button_coords):
        for x1, y1, x2, y2 in button_coords:
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.set_cursor("hand2")
                return
        self.set_cursor("")

class PageOne(Page):
    def __init__(self, master, image, page_number):
        super().__init__(master, image, page_number)  # Call the correct superclass constructor
        self.load_and_display_additional_image()

    def create_widgets(self):
        super().create_widgets()  # This will handle setting the background image

        button_coords = [(111, 606, 265, 652),  # Calculate
                         (348, 609, 507, 652),  # Reset
                         (1113, 11, 1162, 68)]  # Manual  

        # Define text areas for labels
        self.text_areas = [
            (790, 458, 1015, 490),   # X_Deg
            (790, 535, 1015, 567),   # Y_Deg
            (790, 612, 1015, 644)    # Pressure
        ]

        # Create Label widgets for each area
        self.text_labels = []
        for x1, y1, x2, y2 in self.text_areas:
            label = tk.Label(self, font=("Helvetica", 18, "bold"), bg='#D9D9D9', fg='black',
                             text='', anchor='center')
            label.place(x=x1, y=y1, width=x2-x1, height=y2-y1)
            self.text_labels.append(label)

        # Define text boxes
        text_box_areas = {
            'text_box_1': (220, 454, 490, 494), # X_Target
            'text_box_2': (220, 530, 490, 570)  # Y_Target
        }

        # Create Text Box widgets for each area
        self.text_boxes = {}
        for key, (x1, y1, x2, y2) in text_box_areas.items():
            text_box = tk.Entry(self, font=("Helvetica", 18, "bold"), bg='#D9D9D9', fg='black',
                                justify='center', borderwidth=0, highlightthickness=0)
            text_box.place(x=x1, y=y1, width=x2-x1, height=y2-y1)
            self.text_boxes[key] = text_box

        # Add warning labels for X_Target and Y_Target with a white background
        self.warning_label_x = tk.Label(self, font=("Helvetica", 8), fg='red', bg='white', text='', anchor='w')
        self.warning_label_x.place(x=220, y=500, width=270, height=25)

        self.warning_label_y = tk.Label(self, font=("Helvetica", 8), fg='red', bg='white', text='', anchor='w')
        self.warning_label_y.place(x=220, y=577, width=270, height=25)


        # Bind click and motion events
        self.label.bind("<Button-1>", lambda event: self.check_click(event, button_coords))
        self.label.bind("<Motion>", lambda event: self.update_cursor(event, button_coords))

    def load_and_display_additional_image(self):
        # Load, resize, round corners, and place the first image
        img_path_first = "Picture/EmptyTarjectory.png"
        self.place_image(img_path_first, (30, 85), (787, 332), 30, 'photo', 'canvas')

        # Load, resize, and place the second image
        img_path_second = "Picture/EmptyTarget.png"
        self.place_image(img_path_second, (842, 85), (331,331), 30, 'photo_second', 'canvas_second')

    def place_image(self, img_path, position, size, radius, photo_attr_name, canvas_attr_name):
        # Load the image
        img = Image.open(img_path).convert("RGBA")
        # Resize the image
        img_resized = img.resize(size, Image.ANTIALIAS)

        # If a radius is given, apply rounded corners
        if radius:
            img_resized = self.round_corners(img_resized, radius)

        # Keep a reference to the PhotoImage to prevent garbage collection
        setattr(self, photo_attr_name, ImageTk.PhotoImage(img_resized))

        # Create a canvas to display the image
        setattr(self, canvas_attr_name, tk.Canvas(self, width=size[0], height=size[1], bg='white', highlightthickness=0))
        canvas = getattr(self, canvas_attr_name)
        canvas.place(x=position[0], y=position[1])
        canvas.create_image(0, 0, anchor='nw', image=getattr(self, photo_attr_name))
        
    def round_corners(self, image, radius):
        """
        Apply rounded corners to a PIL Image, returning a new image.
        """
        # Create a mask with rounded corners
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        
        # Draw a rectangle with rounded corners on the mask
        # The fill=255 paints the inside of the rectangle white on the mask
        # This white area represents the part of the image that will remain
        draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)
        
        # Create a new image with an alpha channel (RGBA)
        # and the same size as the original image
        rounded_image = Image.new('RGBA', image.size)
        
        # Paste the original image onto the new image
        # The mask is used to only paste the parts inside the rounded rectangle
        rounded_image.paste(image, (0, 0), mask=mask)

        return rounded_image


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

    def perform_calculate(self):
        x_target_text = self.text_boxes['text_box_1'].get()
        y_target_text = self.text_boxes['text_box_2'].get()
        
        # Clear previous warnings
        self.warning_label_x.config(text='')
        self.warning_label_y.config(text='')

        valid_x = self.validate_input(x_target_text)
        valid_y = self.validate_input(y_target_text)

        if not valid_x:
            self.warning_label_x.config(text='Please input the number from x.xx cm to x.xx cm.')
        if not valid_y:
            self.warning_label_y.config(text='Please input the number from x.xx cm to x.xx cm.')

        if valid_x and valid_y:
            x_deg, y_deg, pressure = Calculate(float(x_target_text), float(y_target_text))
            self.text_labels[0].config(text=f"{x_deg:.2f}")  # X_Deg
            self.text_labels[1].config(text=f"{y_deg:.2f}")  # Y_Deg
            self.text_labels[2].config(text=f"{pressure}")  # Pressure

            # Update images
            self.update_image('photo', 'canvas', 'Picture\\Trajectory.png', (30, 85), (787, 332), 30)
            self.update_image('photo_second', 'canvas_second', 'Picture\\Target.png', (842, 85), (331, 331), 30)

    def perform_reset(self):
        for label in self.text_labels:
            label.config(text='')  # Clear the text
        for text_box in self.text_boxes.values():
            text_box.delete(0, 'end')  # Clear the text boxes
        self.warning_label_x.config(text='')
        self.warning_label_y.config(text='')

        # Use raw string for paths or replace with forward slashes
        self.update_image('photo', 'canvas', r'Picture\EmptyTarjectory.png', (30, 85), (787, 332), 30)
        self.update_image('photo_second', 'canvas_second', r'Picture\EmptyTarget.png', (842, 85), (331, 331), 30)

    def update_image(self, photo_attr_name, canvas_attr_name, img_path, position, size, radius):
        full_path = os.path.abspath(img_path)
        img = Image.open(full_path).convert("RGBA")
        img_resized = self.round_corners(img.resize(size, Image.ANTIALIAS), radius)
        setattr(self, photo_attr_name, ImageTk.PhotoImage(img_resized))
        canvas = getattr(self, canvas_attr_name)
        canvas.create_image(0, 0, anchor='nw', image=getattr(self, photo_attr_name))

    def validate_input(self, text):
        try:
            float(text)  # Try to convert the text to a float
            return True
        except ValueError:
            return False

    def update_cursor(self, event, coords):
            # Check if the cursor is in any button area and change the cursor style accordingly
            for x1, y1, x2, y2 in coords:
                if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                    self.set_cursor("hand2")
                    return
            self.set_cursor("")  # Reset to default cursor if not in a button area

class PageTwo(Page):
        
    def create_widgets(self):
        button_coords = [(793, 572, 946, 613),   # Next
                         (1113, 11, 1162, 68)]  # Home

        # Bind button areas to actions
        self.label.bind("<Button-1>", lambda event: self.check_click(event, button_coords))
        self.label.bind("<Motion>", lambda event: self.update_cursor(event, button_coords))

    def check_click(self, event, coords):
        for i, (x1, y1, x2, y2) in enumerate(coords):
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                if i == 0:  # Next to Manual 2
                    self.master.show_frame(2)
                elif i == 1:  # Home to landing page
                    self.master.show_frame(0)
                break

class PageThree(Page):
    def create_widgets(self):
        button_coords = [(672, 572, 824, 618),  # Back
                         (908, 573, 1068, 616), # Done
                         (1113, 11, 1162, 68)]  # Home

        # Bind button areas to actions
        self.label.bind("<Button-1>", lambda event: self.check_click(event, button_coords))
        self.label.bind("<Motion>", lambda event: self.update_cursor(event, button_coords))

    def check_click(self, event, coords):
        for i, (x1, y1, x2, y2) in enumerate(coords):
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                if i == 0:  # Back to Manual 1
                    self.master.show_frame(1)
                else:  # Done and Home to landing page
                    self.master.show_frame(0)
                break

app = App()
app.mainloop()
