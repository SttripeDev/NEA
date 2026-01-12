import math
from tkinter import Canvas

''' 
Name: PieChart
Purpose: Contains logic for piechart creation
'''
class PieChart(Canvas):
    '''
    Name: __init__
    Parameters: parent:tkinter , correct:integer, incorrect:integer ,**kwargs : keyword arguments (allows for more changes involving Canvas integration)
    Returns: None
    Purpose: Initialize the pie chart canvas.
    '''
    def __init__(self, parent, correct=0, incorrect=0, **kwargs):
        super().__init__(parent, **kwargs)

        self.arc_data = {
            "Correct": [correct, "#00FF00"],
            "Incorrect": [incorrect, "#FF0000"]
        }

        # Bind resize event to redraw chart
        self.bind("<Configure>", lambda e: self.draw_chart())
    '''
    Name: update_Values
    Parameters: correct: integer, incorrect : integer
    Returns: None
    Purpose: Updates the value within the piechart.
    '''
    def update_values(self, correct, incorrect):
        self.arc_data = {
            "Correct": [correct, "#00FF00"],
            "Incorrect": [incorrect, "#FF0000"]
        }
        self.draw_chart()
    '''
    Name: draw_chart
    Parameters: None
    Returns: None
    Purpose: Draw or redraw the pie chart.
    '''
    def draw_chart(self):
        self.delete("all")

        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return

        center_x = canvas_width // 2
        center_y = canvas_height // 2
        radius = min(canvas_width, canvas_height) * 0.35

        total = sum(value for value, _ in self.arc_data.values())

        if total == 0:
            self.create_text(
                center_x, center_y,
                text="No data to display",
                font=("Segoe UI", 14),
                fill="gray"
            )
            return

        start_angle = 0
        for key, (value, color) in self.arc_data.items():
            if value == 0:
                continue

            percentage = (value / total) * 100
            extent = 360 * (value / total)

            arc_x = center_x - radius
            arc_y = center_y - radius
            arc_x1 = center_x + radius
            arc_y1 = center_y + radius

            self.create_arc(
                arc_x, arc_y, arc_x1, arc_y1,
                extent=extent,
                start=start_angle,
                fill=color,
                outline="white",
                width=2
            )

            mid_angle = math.radians(start_angle + extent / 2)
            label_radius = radius * 0.65
            label_x = center_x + label_radius * math.cos(mid_angle)
            label_y = center_y - label_radius * math.sin(mid_angle)

            self.create_text(
                label_x, label_y,
                text=f"{key}\n({percentage:.1f}%)",
                font=("Segoe UI", 12, "bold"),
                fill="white",
                justify="center"
            )

            start_angle += extent