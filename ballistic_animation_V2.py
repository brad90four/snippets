# ballistic_animation

import numpy as np
import pyqtgraph as pg
import pyqtgraph.parametertree.parameterTypes as pTypes

from pyqtgraph.parametertree import Parameter, ParameterTree
from pyqtgraph.Qt import QtGui
from tkinter import simpledialog, Tk


# root = Tk()
# root.withdraw()
# V = simpledialog.askinteger("Initial Velocity", "Enter the initial velocity in m/s", parent=root)
# theta = simpledialog.askinteger("Launch Angle", "Enter the launch angle in degrees", parent=root)
# root.destroy()

# testing values
# V = 10
# theta = 45

params = [{"name": "Initial Velocity", "type": "int", "value": 10}, {"name": "Launch Angle", "type": "int", "value": 45}]

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
    return y_0 + v_y * t_i - (0.5 * g * t_i ** 2)


def x_vel(V: int, theta: int) -> int:
    return V * np.cos(np.deg2rad(theta))


def y_vel(V: int, theta: int) -> int:
    return V * np.sin(np.deg2rad(theta))


g = 9.8  # acceleration due to gravity in m/s**2
x_0 = 0  # initial x position in m
y_0 = 0  # initial y position in m

V = p["Initial Velocity"]
theta = p["Launch Angle"]
print(f"{V = }\n{theta = }")


# v_x = V * np.cos(np.deg2rad(theta))  # initial x velocity in m/s
# v_y = V * np.sin(np.deg2rad(theta))  # initial y velocity in m/s

t_end = (2 * y_vel(V, theta)) / g  # flight time in s
time_steps = t_end * 30  # number of time steps (flight time * fps)
time = np.arange(0, t_end, 1 / 30).tolist()  # range of time
y_max = (V ** 2 * np.sin(np.deg2rad(theta)) ** 2) / (2 * g)  # maximum height in m
x_max = (V ** 2 * np.sin(np.deg2rad(2 * theta))) / (g)  # maximum range in m

X = [x_pos(x_0, x_vel(V, theta), i) for i in time]
Y = [y_pos(y_0, y_vel(V, theta), i) for i in time]

# X = [x_pos(x_0, v_x, i) for i in t]
# Y = [y_pos(y_0, v_y, i) for i in t]

win = QtGui.QWidget()
layout = QtGui.QGridLayout()
win.setLayout(layout)
plot_1 = pg.PlotWidget()

curve = plot_1.plot(x=X, y=Y)

max_range = pg.TextItem(text=f"Range: {x_max:.2f}")
max_height = pg.TextItem(text=f"Max Height: {y_max:.2f}", anchor=(0, 1))
max_range.setPos(x_max, 0)
max_height.setPos(x_max / 2, y_max)

plot_1.addItem(max_range)
plot_1.addItem(max_height)

layout.addWidget(plot_1, 0, 0, 1, 1)
layout.addWidget(t, 1, 0, 1, 1)

a = pg.CurveArrow(curve)
a.setStyle(headLen=40)
plot_1.addItem(a)
anim = a.makeAnimation(loop=-1)
anim.start()
win.show()

if __name__ == "__main__":
    pg.exec()
