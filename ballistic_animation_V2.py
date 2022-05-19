# ballistic_animation
import os
from pathlib import Path
import numpy as np

import pyqtgraph as pg
import pyqtgraph.exporters
from pyqtgraph.parametertree import Parameter, ParameterTree
from pyqtgraph.Qt import QtGui
from PIL import Image
import cv2


params = [
    {"name": "Initial Velocity", "type": "int", "value": 10},
    {"name": "Launch Angle", "type": "int", "value": 45},
    {"name": "Go!", "type": "action"}
]

app = pg.mkQApp("Ballistic Animation")
p = Parameter.create(name="params", type="group", children=params)
t = ParameterTree()
t.setParameters(p, showTop=False)
t.setWindowTitle("Starting Values")


def x_pos(x_0: int, v_x: int, t_i: int) -> int:
    """Calculate x displacement."""
    return x_0 + v_x * t_i


def y_pos(y_0: int, v_y: int, t_i: int) -> int:
    """Calculate y displacement."""
    return y_0 + v_y * t_i - (0.5 * g * t_i**2)


def x_vel(V: int, theta: int) -> int:
    return V * np.cos(np.deg2rad(theta))


def y_vel(V: int, theta: int) -> int:
    return V * np.sin(np.deg2rad(theta))


g = 9.8  # acceleration due to gravity in m/s**2

win = QtGui.QWidget()
layout = QtGui.QGridLayout()
win.setLayout(layout)
plot_1 = pg.PlotWidget()
curve = pg.PlotCurveItem([0, 1], [0, 1])
a = pg.CurveArrow(curve)
a.setStyle(headLen=40)
layout.addWidget(plot_1, 0, 0, 1, 1)
layout.addWidget(t, 1, 0, 1, 1)

animation = None


def run():
    plot_1.clear()
    V = p["Initial Velocity"]
    theta = p["Launch Angle"]
    print(f"{V = }\n{theta = }")
    x_0 = 0  # initial x position in m
    y_0 = 0  # initial y position in m
    t_end = (2 * y_vel(V, theta)) / g  # flight time in s
    time = np.arange(0, t_end, 1 / 30).tolist()  # range of time
    y_max = (V ** 2 * np.sin(np.deg2rad(theta)) ** 2) / (2 * g)  # maximum height in m
    x_max = (V ** 2 * np.sin(np.deg2rad(2 * theta))) / (g)  # maximum range in m
    max_range = pg.TextItem(text=f"Range: {x_max:.2f}")
    max_height = pg.TextItem(text=f"Max Height: {y_max:.2f}", anchor=(0, 1))
    X = [x_pos(x_0, x_vel(V, theta), i) for i in time]
    Y = [y_pos(y_0, y_vel(V, theta), i) for i in time]
    for item in max_range, max_height, a, curve:
        plot_1.addItem(item)
    curve.setData(X, Y)
    # max_height.setText(f"Max Height: {max_height:.2f}")
    # max_range.setText(f"Range: {max_range:.2f}")
    max_range.setPos(x_max, 0)
    max_height.setPos(x_max / 2, y_max)
    global animation
    animation = a.makeAnimation(loop=-1)
    animation.start()


image_folder = Path(__file__).parent
image_list = sorted(os.listdir(image_folder), key=os.path.getctime)
all_images = [image for image in image_list if "png" in image]


def gif(save_name: str) -> None:
    """Function to create a gif from a series of images

    Args:
        save_name (str): Save name for the file.
    """
    images = [Image.open(file) for file in all_images]
    images[0].save(
        f"{os.path.join(image_folder, save_name)}.gif",
        save_all=True,
        append_images=images,
        optimize=True,
        # duration=200,
        loop=0,
    )


p.child("Go!").sigActivated.connect(run)

win.show()

if __name__ == "__main__":
    pg.exec()
    gif("test")
