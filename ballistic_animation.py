# ballistic_animation

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from tkinter import Tk, simpledialog

root = Tk()
root.withdraw()
V = simpledialog.askinteger("Initial Velocity", "Enter the initial velocity in m/s", parent=root)
theta = simpledialog.askinteger("Launch Angle", "Enter the launch angle in degrees", parent=root)
root.destroy()

g = 9.8  # acceleration due to gravity in m/s**2
x_0 = 0  # initial x position in m
y_0 = 0  # initial y position in m
v_x = V * np.cos(np.deg2rad(theta))  # initial x velocity in m/s
v_y = V * np.sin(np.deg2rad(theta))  # initial y velocity in m/s
t_end = (2 * v_y) / g  # flight time in s
time_steps = t_end * 30  # number of time steps (flight time * fps)
interval = t_end / time_steps  # interval size based on flight time and time steps
t = np.arange(0, t_end, interval).tolist()  # range of time
y_max = (V ** 2 * np.sin(np.deg2rad(theta)) ** 2) / (2 * g)  # maximum height in m
x_max = (V ** 2 * np.sin(np.deg2rad(2 * theta))) / (g)  # maximum range in m


def x_pos(x_0: int, v_x: int, t_i: int) -> int:
    return x_0 + v_x * t_i


def y_pos(y_0: int, v_y: int, t_i: int) -> int:
    return y_0 + v_y * t_i - (0.5 * g * t_i ** 2)


fig = plt.figure()
ax = plt.axes()
(line,) = ax.plot([], [])
plt.xlim(0, x_max * 1.05)
plt.ylim(0, y_max * 1.5)
plt.gca().set_aspect("equal", adjustable="box")
plt.title(f"Ballistic Trajectory for {V}m/s at {theta} degrees")
plt.xlabel("Distance in meters")
plt.ylabel("Height in meters")

height_label = f"Max Height: {y_max:.1f}m"
plt.hlines(y=y_max, xmin=0, xmax=x_max, color="firebrick", label=height_label)
plt.annotate(height_label, xy=(x_max / 2, y_max), textcoords="offset points", xytext=(0, 10), ha="center")

range_label = f"Max Distance: {x_max:.1f}m"
plt.vlines(x=x_max, ymin=0, ymax=y_max, color="firebrick", label=range_label)
plt.annotate(range_label, xy=(x_max, y_max / 2), textcoords="offset points", xytext=(0, 10), ha="center")


def init():
    line.set_data([], [])
    return (line,)


X = []
Y = []


def animate(i):
    t_i = i
    X.append(x_pos(x_0, v_x, t_i))
    Y.append(y_pos(y_0, v_y, t_i))
    line.set_data(X, Y)
    return (line,)


anim = FuncAnimation(fig, animate, init_func=init, frames=t, interval=1, blit=True)

save_name = f"{V} m per sec at {theta} degrees.gif"
anim.save(save_name, writer=PillowWriter(fps=30))
