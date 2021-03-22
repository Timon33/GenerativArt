import pyglet
from pyglet import shapes

import numpy as np
import math
import random
import os
from numba import njit, jit
from opensimplex import OpenSimplex


# save the current screen to png file
def save_frame(time, folder="frames"):

    filename = f"frame-{time}.gif"
    path = os.path.join(folder, filename)
    pyglet.image.get_buffer_manager().get_color_buffer().save(path)
    print(filename)

@njit
def gen_particles(n):
    
    # generate n random particles 
    # dim 1: old pod, new pos
    # dim 2: 2d positions
    r = np.random.rand(n, 2, 2) * SIZE
    r[:][1] = r[:][0]

    return r

def gen_field(pos, time, dtime, scale, twist):

    field = np.empty(pos.shape, dtype=np.float32)

    z = math.cos(time * 2 * math.pi) * dtime
    w = math.sin(time* 2 * math.pi) * dtime

    for i, p in enumerate(pos):
        angle = FIELD.noise4d(*(p * scale), z, w) * math.pi * twist
        field[i] = math.cos(angle), math.sin(angle)

    return field

# particle update function taking the precomputed field vectors
@njit
def update_positions(particles, field, strength):

    for p, f in zip(particles, field):
        p[1] = p[0]
        p[0] += f * strength

        if not (0 < p[0][0] < SIZE and 0 < p[0][1] < SIZE):
            p[0] %= SIZE
            p[1] = p[0]

    return particles

def render_frame(batch, particles, time, dtime, scale, strength, twist):

    for i in range(ITERS_PER_FRAME):

        # white with selected alpha for every vertex
        field = gen_field(particles[:, ::2].reshape(-1, 2), time, dtime, scale, twist)

        particles = update_positions(particles, field, strength)

        # rehape the particles into flat array and added them to the batch
        batch.add(N_PARTICELS * 2, pyglet.graphics.GL_LINES, None, ('v2f', particles.reshape(-1)), ("c4B", COLORS))

    return particles

SIZE = 600
MAX_TIME = 30
N_PARTICELS = 5000

ALPHA = 10
LINE_SIZE = 1
SPAWN_PROB = 0.3
ITERS_PER_FRAME = 200

COLORS = (255, 255, 255, ALPHA) * N_PARTICELS * 2

time = 0

# pyglet main window
window = pyglet.window.Window(width=SIZE, height=SIZE)

FIELD = OpenSimplex()
particles = gen_particles(N_PARTICELS)

@window.event
def on_draw(*args):
    global time, particles

    window.clear()

    batch = pyglet.graphics.Batch()

    # particles = gen_particles(N_PARTICELS)
    paricles = render_frame(batch, particles, (time % MAX_TIME) / MAX_TIME, 0.6, 0.02, 1, 1)

    batch.draw()
    
    for p in random.choices(particles, k=int(N_PARTICELS * SPAWN_PROB)):
        p[0] = np.random.rand(2) * SIZE

    save_frame(time % MAX_TIME)
    time += 1


pyglet.gl.glLineWidth(LINE_SIZE)
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

pyglet.clock.schedule(on_draw)
pyglet.app.run()




