import tkinter as tk
import random
import math

# =========================
# WINDOW SETTINGS
# =========================

WIDTH = 1280
HEIGHT = 720

BACKGROUND = "black"
FOREGROUND = "white"

NUM_BOIDS = 1200

# =========================
# BOID SETTINGS
# =========================

MAX_SPEED = 20
MAX_FORCE = 0.05

ALIGN_RADIUS = 50
COHESION_RADIUS = 60
SEPARATION_RADIUS = 22

# Rectangle enclosure
BOUNDARY_LEFT = 20
BOUNDARY_RIGHT = WIDTH - 20

BOUNDARY_TOP = 20
BOUNDARY_BOTTOM = HEIGHT - 20


# =========================
# BOID CLASS
# =========================

class Boid:

    def __init__(self):

        self.x = random.uniform(
            BOUNDARY_LEFT + 50,
            BOUNDARY_RIGHT - 50
        )

        self.y = random.uniform(
            BOUNDARY_TOP + 50,
            BOUNDARY_BOTTOM - 50
        )

        angle = random.uniform(0, math.pi * 2)

        self.vx = math.cos(angle)
        self.vy = math.sin(angle)

        self.ax = 0
        self.ay = 0

    # =========================
    # APPLY FORCE
    # =========================

    def apply_force(self, fx, fy):

        self.ax += fx
        self.ay += fy

    # =========================
    # FLOCKING LOGIC
    # =========================

    def flock(self, boids):

        align_x = 0
        align_y = 0

        coh_x = 0
        coh_y = 0

        sep_x = 0
        sep_y = 0

        align_total = 0
        coh_total = 0
        sep_total = 0

        for other in boids:

            if other == self:
                continue

            dx = other.x - self.x
            dy = other.y - self.y

            dist = math.sqrt(dx * dx + dy * dy)

            # =========================
            # ALIGNMENT
            # =========================

            if dist < ALIGN_RADIUS:

                align_x += other.vx
                align_y += other.vy

                align_total += 1

            # =========================
            # COHESION
            # =========================

            if dist < COHESION_RADIUS:

                coh_x += other.x
                coh_y += other.y

                coh_total += 1

            # =========================
            # SEPARATION
            # =========================

            if dist < SEPARATION_RADIUS and dist > 0:

                sep_x -= dx / dist
                sep_y -= dy / dist

                sep_total += 1

        # =========================
        # APPLY ALIGNMENT
        # =========================

        if align_total > 0:

            align_x /= align_total
            align_y /= align_total

            mag = math.sqrt(
                align_x**2 + align_y**2
            )

            if mag > 0:

                align_x = (
                    align_x / mag
                ) * MAX_SPEED

                align_y = (
                    align_y / mag
                ) * MAX_SPEED

            steer_x = align_x - self.vx
            steer_y = align_y - self.vy

            self.apply_force(
                steer_x * MAX_FORCE,
                steer_y * MAX_FORCE
            )

        # =========================
        # APPLY COHESION
        # =========================

        if coh_total > 0:

            coh_x /= coh_total
            coh_y /= coh_total

            desired_x = coh_x - self.x
            desired_y = coh_y - self.y

            mag = math.sqrt(
                desired_x**2 + desired_y**2
            )

            if mag > 0:

                desired_x = (
                    desired_x / mag
                ) * MAX_SPEED

                desired_y = (
                    desired_y / mag
                ) * MAX_SPEED

            steer_x = desired_x - self.vx
            steer_y = desired_y - self.vy

            self.apply_force(
                steer_x * MAX_FORCE * 0.6,
                steer_y * MAX_FORCE * 0.6
            )

        # =========================
        # APPLY SEPARATION
        # =========================

        if sep_total > 0:

            sep_x /= sep_total
            sep_y /= sep_total

            mag = math.sqrt(
                sep_x**2 + sep_y**2
            )

            if mag > 0:

                sep_x = (
                    sep_x / mag
                ) * MAX_SPEED

                sep_y = (
                    sep_y / mag
                ) * MAX_SPEED

            steer_x = sep_x - self.vx
            steer_y = sep_y - self.vy

            self.apply_force(
                steer_x * MAX_FORCE * 1.8,
                steer_y * MAX_FORCE * 1.8
            )

    # =========================
    # UPDATE POSITION
    # =========================

    def update(self):

        self.vx += self.ax
        self.vy += self.ay

        speed = math.sqrt(
            self.vx**2 + self.vy**2
        )

        # Speed limit
        if speed > MAX_SPEED:

            self.vx = (
                self.vx / speed
            ) * MAX_SPEED

            self.vy = (
                self.vy / speed
            ) * MAX_SPEED

        self.x += self.vx
        self.y += self.vy

        self.ax = 0
        self.ay = 0

        self.boundaries()

    # =========================
    # BOUNDARY SYSTEM
    # =========================

    def boundaries(self):

        margin = 60
        turn_force = 0.25

        # =========================
        # SOFT WALL AVOIDANCE
        # =========================

        if self.x < BOUNDARY_LEFT + margin:
            self.vx += turn_force

        if self.x > BOUNDARY_RIGHT - margin:
            self.vx -= turn_force

        if self.y < BOUNDARY_TOP + margin:
            self.vy += turn_force

        if self.y > BOUNDARY_BOTTOM - margin:
            self.vy -= turn_force

        # =========================
        # HARD CLAMP
        # =========================

        self.x = max(
            BOUNDARY_LEFT,
            min(self.x, BOUNDARY_RIGHT)
        )

        self.y = max(
            BOUNDARY_TOP,
            min(self.y, BOUNDARY_BOTTOM)
        )

    # =========================
    # DRAW
    # =========================

    def draw(self, canvas):

        # Direction angle
        angle = math.atan2(
            self.vy,
            self.vx
        )

        size = 6

        # Triangle points
        x1 = self.x + math.cos(angle) * size
        y1 = self.y + math.sin(angle) * size

        x2 = self.x + math.cos(angle + 2.5) * size
        y2 = self.y + math.sin(angle + 2.5) * size

        x3 = self.x + math.cos(angle - 2.5) * size
        y3 = self.y + math.sin(angle - 2.5) * size

        canvas.create_polygon(
            x1, y1,
            x2, y2,
            x3, y3,
            fill=FOREGROUND,
            outline=""
        )


# =========================
# CREATE WINDOW
# =========================

root = tk.Tk()

root.title("Bird Flocking Simulation")

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg=BACKGROUND,
    highlightthickness=0
)

canvas.pack()

# =========================
# CREATE BOIDS
# =========================

boids = [
    Boid()
    for _ in range(NUM_BOIDS)
]


# =========================
# MAIN LOOP
# =========================

def update():

    canvas.delete("all")

    # Draw enclosure
    canvas.create_rectangle(
        BOUNDARY_LEFT,
        BOUNDARY_TOP,
        BOUNDARY_RIGHT,
        BOUNDARY_BOTTOM,
        outline=FOREGROUND
    )

    # Flocking
    for boid in boids:
        boid.flock(boids)

    # Update + Draw
    for boid in boids:
        boid.update()
        boid.draw(canvas)

    root.after(16, update)


# Start simulation
update()

root.mainloop()