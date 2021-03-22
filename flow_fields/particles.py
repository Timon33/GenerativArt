from pyglet import shapes
import numpy as np

class Particle():

    def __init__(self, pos, x_max, y_max):
        self.pos = np.array(pos, dtype=np.float64)
        self.prev_pos = np.array(pos, dtype=np.float64)
        # self.vel = np.array((0, 0), dtype=np.float64)

        self.x_max = x_max
        self.y_max = y_max

    def add_force(self, force):
        self.prev_pos = np.copy(self.pos)
        self.pos += np.array(force)
    
    def update_pos(self):

        x = self.pos[0]
        y = self.pos[1]

        if x > self.x_max or x < 0 or y > self.y_max or y < 0:
            self.pos[0] %= self.x_max
            self.pos[1] %= self.y_max
            self.prev_pos = np.copy(self.pos)
            

    def draw(self):
        return (*self.prev_pos, *self.pos)

    def cell_pos(self, cell_size):
        return self.pos.astype(int) // cell_size

    def __repr__(self):
        return f"particle from {self.prev_pos} to {self.pos}"
