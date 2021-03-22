import pyglet
from pyglet import shapes
import pyglet.gl as gl


import subprocess
from time import sleep

import numpy as np
import math
import random
import os
from numba import njit, jit
from opensimplex import OpenSimplex


# save the current screen to png file
def save_frame(time, folder="frames"):

    filename = f"frame-{time:03}.gif"
    path = os.path.join(folder, filename)
    pyglet.image.get_buffer_manager().get_color_buffer().save(path)
    print(filename)

def randomValue(a, b):

    speed = 10

    x = math.cos(a * 2 * math.pi) * speed
    y = math.sin(a * 2 * math.pi) * speed

    # z = math.cos(b * 2 * math.pi) * 0.1
    # w = math.sin(b * 2 * math.pi) * 0.1

    return noise.noise3d(x, y, b)

def f(x):
    a = 0.3
    return a * math.pow(x, 3) / abs(x) + (1 - a) * x

def gen_point(p, i):
    x = f(randomValue(p, 0))
    y = f(randomValue(p, 100))
    z = f(randomValue(p, 200))

    # x += math.cos(p * 0.1) * 0.1
    # y += math.sin(p * 0.1) * 0.1

    x *= 10
    y *= 10
    z *= 10

    return (x, y, z)

def distance(a, b):
    return math.sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2) + pow(a[2] - b[2], 2))

def points_to_lines(points, batch):
    for i in range(len(points)):
        lines = tuple()
        color = tuple()
        for j in range(i, len(points)):
            lines += points[i]
            lines += points[j]

            dst = max(distance(points[i], points[j]), 1)
            alpha = int(1 / math.pow(dst, 2) * 100)
            color += (255, 255, 255, alpha) * 2

        batch.add((len(points) - i) * 2, pyglet.graphics.GL_LINES, None, ("v3f", lines), ("c4B", color))


FRAMES = 170
time = 0
K = 150

SIZE = 1200
LINE_SIZE = 1

# pyglet main window
window = pyglet.window.Window(width=SIZE, height=SIZE)
noise = OpenSimplex(seed=random.randint(0, 2**32))

@window.event
def on_draw(*args):
    global time, particles

    t = time / FRAMES

    window.clear()

    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.gluPerspective(90, 1, 0.1, 100)

    gl.glTranslatef(0, 0, -10)

    gl.glRotatef(t * 360, 0, 1, 0)
    # gl.glRotatef(t * 360, 1, 0, 0)

    batch = pyglet.graphics.Batch()

    if time == FRAMES:
        exit()

    points = []

    for i in range(K):
        points.append(gen_point((i + t) / K, i))


    # print(points)
    points_to_lines(points, batch)

    batch.draw()

    save_frame(time % FRAMES)
    time += 1


pyglet.gl.glLineWidth(LINE_SIZE)
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

pyglet.clock.schedule(on_draw)
pyglet.app.run()

