# Projectile-Simulation ⚽
This project is a graphical simulation designed for the GRA163 Group 3. It provides a user-friendly interface to simulate and calculate projectile trajectories and target hits using given parameters.

# Project Structure 💻
GUI: Contains the configuration and image assets for the GUI.

Function: Contains the necessary functions for projectile and trajectory calculations.

Simulation Calculation: Contains configuration and simulation data files.

# Installation ⬇️
Download all Require Module First!
```bash
  pip install -r requirements.txt
```

# Configuration 😁
## GUI Configuration 📊
You can find this file  in ``GUI\config.json``
You can change the area of buttons, text_areas, and text_boxes using ``GUI\FindCoordinateOnButton.py``

For each GUI page, you can add below.
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
## Luncher and Feild Configuration 🎯
You can find this file  in ``Simulation Calculation\config.json`` (every unit is SI unit such as meter, degree, or meter per second square)
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

# Feedback 📞
If you have any feedback, please reach out to Group 3 FRAB10 🙏
