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

def randNoise(a, b, speed=10):

    x = math.cos(a * 2 * math.pi) * speed
    y = math.sin(a * 2 * math.pi) * speed

    # z = math.cos(b * 2 * math.pi) * 0.1
    # w = math.sin(b * 2 * math.pi) * 0.1

    return noise.noise3d(x, y, b)

def f(x):
    a = 0.3
    return a * math.pow(x, 3) / abs(x) + (1 - a) * x

def gen_cirle(p, i, t):
    
    # r = 6 * (1 + randNoise(p, 300, 2) * 0.1)
    # r = 6 * (1 + math.sin(t * math.pi * 2) * 0.15)
    r = 6
    s = 4

    i = int(randNoise(p, -100, s) * 10) % 3
    pos = np.array((randNoise(p, 0, s), randNoise(p, 100, s), randNoise(p, 200, s)))
    dist = np.linalg.norm(pos)
    pos /= dist / r

    return pos

def gen_cube(p, i, t):
    s = 4
    r = 4

    pos = np.array((randNoise(p, 0, s), randNoise(p, 100, s), randNoise(p, 200, s)))
    factor = abs(r / pos[np.argmax(abs(pos))])
    pos *= factor
    return pos

def gen_point(p, i, t):
    return gen_cube(p, i, t)

def points_to_lines(points, batch, tri_tresh):
    for i in range(len(points)):
        lines = np.empty((len(points) - i, 2, 3))
        # triangles = tuple()
        color = np.empty((len(points) - i, 8), dtype=np.int8)

        for j in range(len(points) - i):
            lines[j] = points[i], points[j]

            # dst = max(np.linalg.norm(points[i] - points[j], ord=2), 1)
            '''
            if dst < tri_tresh:
                for k in range(len(points) - j):
                    dst1 = np.linalg.norm(points[i] - points[k])
                    dst2 = np.linalg.norm(points[j] - points[k])
                    if dst1 < tri_tresh and dst2 < tri_tresh:
                        triangles += tuple(points[i])
                        triangles += tuple(points[j])
                        triangles += tuple(points[k])
            '''
            alpha = int(1 / math.pow(dst, 2) * 100)
            color[j] = (255, 255, 255, alpha) * 2

        lines = lines.reshape(-1)
        color = color.reshape(-1)

        batch.add((len(points) - i) * 2, pyglet.graphics.GL_LINES, None, ("v3f", lines), ("c4B", color))

        # batch.add(len(triangles) // 3, pyglet.graphics.GL_TRIANGLES, None, ("v3f", triangles))


FRAMES = 200
time = 0
K = 100

SIZE = 500
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

    batch = pyglet.graphics.Batch()

    if time == FRAMES:
        exit()

    points = np.empty((K, 3))

    for i in range(K):
        points[i] = gen_point((i + t) / K, i, t)

    # points = points.reshape(-1)
    # batch.add(len(points) // 3, pyglet.graphics.GL_POINTS, None, ("v3f", points))
    # print(points)
    points_to_lines(points, batch, 1.2)

    batch.draw()

    save_frame(time % FRAMES)
    time += 1


pyglet.gl.glLineWidth(LINE_SIZE)
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

pyglet.clock.schedule(on_draw)
pyglet.app.run()

