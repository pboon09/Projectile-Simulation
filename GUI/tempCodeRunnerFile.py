lf.warning_label_x.config(text='Please input a valid number for X in cm (e.g., 12.34).')
            return  # Stop further execution if input is not valid
        if not valid_y:
            self.warning_label_y.config(text='Please input a valid number for Y in cm (e.g., 12.34).')
            return  # Stop further execution if input is not valid

        try:
            x_deg, y_deg, pressure = Calculate(float(x_target_text), float(y_target_text))
            # The following function should check if the target is in the triangle and raise an exception if not
            plot_Target_view(0.5, float(x_target_text)/100, float(y_target_text)/100, 0.137, 'Simulation Calculation\SquashBall_Pos.json')  # Ensure this doesn't raise an error
            
            # If no exceptions, update labels and images
            self.text_labels[0].config(text=f"{x_deg:.2f}°")  # X_Deg
            self.text_labels[1].config(text=f"{y_deg:.2f}°")  # Y_Deg
            self.text_labels[2].config(text=f"{pressure} bar")  # Pressure

            self.update_image('photo', 'canvas', 'Picture\\Trajectory.png', (30, 85), (787, 332), 30)
            self.update_image('photo_second', 'canvas_second', 'Picture\\Target.png', (842, 85), (331, 331), 30)

        except ValueError as e:
            self.warning_label_x.config(text=str(e))  # Display specific error message
            # Optionally clear any previous data or images if needed
            for label in self.text_labels:
                label.config(text='')  # Clear the text
            self.update_image('photo', 'canvas', r'Picture\EmptyTarjectory.png', (30, 85), (787, 332), 30)
            self.update_image('photo_second', 'canvas_second', r'Picture\EmptyTarget.png', (842, 85), (331, 331), 30)