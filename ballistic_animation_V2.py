# ballistic_animation
import glob
import os
from pathlib import Path

import numpy as np
from PIL import Image

import pyqtgraph as pg
from pyqtgraph.exporters import ImageExporter
from pyqtgraph.parametertree import Parameter, ParameterTree
from pyqtgraph.Qt import QtCore, QtWidgets

params = [
    {"name": "Initial Velocity", "type": "int", "value": 10},
    {"name": "Launch Angle", "type": "int", "value": 45},
    {"name": "Go!", "type": "action"},
]

app = pg.mkQApp("Ballistic Animation")
p = Parameter.create(name="params", type="group", children=params)
t = ParameterTree()
t.setParameters(p, showTop=False)
t.setWindowTitle("Starting Values")

win = QtWidgets.QWidget()
layout = QtWidgets.QGridLayout()
win.setLayout(layout)
plot_1 = pg.PlotWidget()
plot_1.setAspectLocked(True)
curve = pg.PlotCurveItem([0, 1], [0, 1])
a = pg.CurveArrow(curve)
a.setStyle(headLen=40)
layout.addWidget(plot_1, 0, 0, 1, 1)
layout.addWidget(t, 1, 0, 1, 1)

animation = None
screenshotTimer = None
counter = 0
screenshotFolder = os.path.join(Path(__file__).parent, "screenshots")
screenshotPngGlob = f"{screenshotFolder}/*.png"

g = 9.8  # acceleration due to gravity in m/s**2


def x_pos(x_0: int, v_x: int, t_i: int) -> int:
    """Calculate x displacement.

    Args:
        x_0 (int): Initial x position in m.
        v_x (int): Initial x velocity in m/s.
        t_i (int): Time in s.

    Returns:
        int: x displacement in m.
    """
    return x_0 + v_x * t_i


def y_pos(y_0: int, v_y: int, t_i: int) -> int:
    """Calculate y displacement.

    Args:
        y_0 (int): Initial y position in m.
        v_y (int): Initial y velocity in m/s.
        t_i (int): Time in s.

    Returns:
        int: y displacement in m.
    """
    return y_0 + v_y * t_i - (0.5 * g * t_i**2)


def x_vel(V: int, theta: int) -> int:
    """Calculate the initial x component of velocity.

    Args:
        V (int): initial velocity in m/s
        theta (int): launch angle in degrees

    Returns:
        int: initial x velocity in m/s
    """
    return V * np.cos(np.deg2rad(theta))


def y_vel(V: int, theta: int) -> int:
    """Calculate the initial y component of velocity.

    Args:
        V (int): initial velocity in m/s
        theta (int): launch angle in degrees

    Returns:
        int: initial y velocity in m/s
    """
    return V * np.sin(np.deg2rad(theta))


def screenshot():
    """Helper function to export a screenshot of the plot."""
    global counter
    # Give the exporter the scene you want to render
    exporter = ImageExporter(plot_1.plotItem)
    exporter.export(f"{screenshotFolder}/{counter}.png")
    counter += 1


def run():
    """Main event loop to run the animation."""
    # First, clear out possible previous screenshots
    for file in glob.glob(screenshotPngGlob):
        os.remove(file)

    plot_1.clear()
    V = p["Initial Velocity"]
    theta = p["Launch Angle"]
    print(f"{V = }\n{theta = }")

    x_0 = 0  # initial x position in m
    y_0 = 0  # initial y position in m
    t_end = (2 * y_vel(V, theta)) / g  # flight time in s
    updateIntervalSeconds = 1 / 30
    time = np.arange(0, t_end, 1 / 30).tolist()  # range of time

    y_max = (V**2 * np.sin(np.deg2rad(theta)) ** 2) / (2 * g)  # maximum height in m
    x_max = (V**2 * np.sin(np.deg2rad(2 * theta))) / (g)  # maximum range in m

    max_range = pg.TextItem(text=f"Range: {x_max:.2f}")
    max_height = pg.TextItem(text=f"Max Height: {y_max:.2f}", anchor=(0, 1))
    max_range.setPos(x_max * 0.9, 0)
    max_height.setPos(x_max / 2, y_max)

    X = [x_pos(x_0, x_vel(V, theta), i) for i in time]
    Y = [y_pos(y_0, y_vel(V, theta), i) for i in time]

    curve.setData(X, Y)

    for item in max_range, max_height, a, curve:
        plot_1.addItem(item)

    global animation, screenshotTimer
    animation = a.makeAnimation(duration=int(t_end) * 1000)
    animation.start()

    # Fire "screenshot" every "update" milliseconds
    # Stop when animation is over
    screenshotTimer = QtCore.QTimer()
    screenshotTimer.timeout.connect(screenshot)
    animation.finished.connect(screenshotTimer.stop)
    screenshotTimer.start(int(updateIntervalSeconds * 1000))


def gif(save_name: str) -> None:
    """Function to create a gif from a series of images

    Args:
        save_name (str): Save name for the file.
    """
    base_dir = Path(__file__).parent
    image_folder = os.path.join(base_dir, "screenshots")
    os.chdir(image_folder)
    image_list = sorted(os.listdir(image_folder), key=os.path.getctime)
    all_images = [image for image in image_list if "png" in image]
    images = [Image.open(file) for file in all_images]
    images[0].save(
        f"{os.path.join(image_folder, save_name)}.gif",
        save_all=True,
        append_images=images,
        optimize=True,
        fps=30,
        loop=0,
    )


p.child("Go!").sigActivated.connect(run)

win.show()

if __name__ == "__main__":
    pg.exec()
    gif("test")
