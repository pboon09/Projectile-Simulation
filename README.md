# Projectile-Simulation ⚽
This project is a graphical simulation designed for the GRA163 Group 3. It provides a user-friendly interface to simulate and calculate projectile trajectories and target hits using given parameters.

# Project Structure 💻
- GUI:Contains the configuration and image assets for the GUI.

- Function: Contains the necessary functions for projectile and trajectory calculations.

- Simulation Calculation: Contains configuration and simulation data files.

# Installation ⬇️
Download all Require Module First!
```bash
  pip install -r requirements.txt
```

# Configuration 😁
### GUI Configuration 📊
The configuration file can be found at ``GUI/config.json``.
You may adjust the coordinates of buttons, text areas, and text boxes using the script ``GUI/FindCoordinateOnFrame.py.``

For each GUI page, the configuration can be specified as follows:

```json
{
    "buttons": {
        "page_one": [
            {"name": "Calculate", "coords": [111, 606, 265, 652]},
            {"name": "Reset", "coords": [348, 609, 507, 652]},
            {"name": "Manual", "coords": [1113, 11, 1162, 68]}
        ],
        ...
    },
    "text_areas": {
        "page_one": [
            {"name": "Pitch", "coords": [760, 475, 980, 510]},
            {"name": "Yaw", "coords": [760, 593, 980, 617]}
        ]
    },
    "text_boxes": {
        "page_one": [
            {"name": "Z_Target", "coords": [220, 454, 490, 494]},
            {"name": "Y_Target", "coords": [220, 530, 490, 570]}
        ]
    },
    "warning_labels": {
        "page_one": [
            {"name": "Z_Label","coords": [220, 500, 490, 525]},
            {"name": "Y_Label","coords": [220, 577, 490, 602]}
        ]
    },
    "images": {
        "page_one": {
            "main": "Picture/GUI_Page/LandingPage.png",
            "additional_1": "Picture/EmptyTarjectory.png",
            "additional_2": "Picture/EmptyTarget.png"
        },
        ...
    }
}
```

### Luncher and Feild Configuration 🎯
The configuration file can be found at ``Simulation Calculation/config.json``. The units are specified in meters, meters per second, and degrees.
```json
{
    "luncher_parameters": {
        "luncher_length": 0.3,
        "luncher_baseHight": 0.07,
        "velocity": 6.7,
        "Pitch_min": -21,
        "Pitch_max": 21,
        "Pitch_step": 3,        
        "Yaw_min": 24,
        "Yaw_max": 60,
        "Yaw_step": 3
    },
    "field_parameters": {
        "table": 0.755,
        "target_distance": 2,
        "wall_distance": 1,
        "wall_height": 0.6
    },
    "target_parameters": {
        "triangle_side_length": 0.5,
        "circle_diameter": 0.137,
        "squash_ball_diameter": 0.04
    }
}
```

# How to use! ❓
### Step 1: Find Coordinates on Frame
Navigate to ``GUI/FindCoordinateOnFrame.py``. Paste your image path and then run the program. Click on the pop-up screen to see the coordinates.

```python
# Load your image
image = Image.open("YOUR PATH")  # Make sure to provide the correct path here
```

### Step 2: Configure Coordinates
Go to ``GUI/config.json`` and set the coordinates for each element such as buttons, text areas, or text boxes. The format is ``"coords": [X1, Y1, X2, Y2], `` representing the top-left and bottom-right coordinates.

### Step 3: Set Simulation Parameters
Go to Simulation ``Calculation/config.json`` and set each parameter based on your settings.

### Step 4: Run the GUI
```python
python GUI\GUI.py
```

# Feedback 📞
If you have any feedback, please reach out to Group 3 FRAB10 🙏
