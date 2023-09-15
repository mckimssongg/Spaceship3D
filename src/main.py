import tkinter as tk
import random
import geometria
import math

game = geometria.Game()
meteor_shapes = []
projectiles_shapes = []

def move_spaceship(event):
    x, y = event.x, event.y
    dx, dy = x - spaceship.getX(), y - spaceship.getY()
    spaceship.move(dx, dy, 0)
    canvas.coords(spaceship_shape, x-10, y+10, x+10, y+10, x, y-10)

def update_meteors():
    global meteor_shapes
    game.moveMeteors(0, 10, 0)
    
    if random.random() < 0.5:
        x = random.randint(0, 400)
        y = 0
        z = 0
        size = 10
        game.addMeteor(x, y, z, size)
        new_shape = draw_meteor(x, y, size)
        meteor_shapes.append(new_shape)

    to_remove = game.syncMeteors()
    for index in reversed(to_remove):
        canvas.delete(meteor_shapes[index])
        game.destroyMeteor(index)
        del meteor_shapes[index]

    root.after(500, update_meteors)

def draw_meteor(x, y, size):
    points = [(round(x + size * math.cos(math.radians(angle))), round(y + size * math.sin(math.radians(angle)))) for angle in range(0, 360, 60)]
    flat_points = [coord for point in points for coord in point]
    return canvas.create_polygon(*flat_points, outline="red", fill="red")

def fire_projectile(event):
    x, y = spaceship.getX(), spaceship.getY()
    size = 5
    projectile_shape = canvas.create_oval(x - size, y - size, x + size, y + size, fill="yellow")
    projectiles_shapes.append(projectile_shape)
    game.addProjectile(x, y)

def update_projectiles():
    global projectiles_shapes, meteor_shapes

    game.moveProjectiles(0, -10)
    if game.projectileCollidesWithMeteor(15.0):
        projectiles_shapes = []
        meteor_shapes = []

    to_remove = game.syncProjectiles()
    for index in reversed(to_remove):
        canvas.delete(projectiles_shapes[index])
        del projectiles_shapes[index]

    root.after(100, update_projectiles)

spaceship = geometria.Spaceship(200.0, 200.0, 0.0)
root = tk.Tk()
root.title("Meteor Destroyer")
canvas = tk.Canvas(root, width=400, height=400, bg="black")
canvas.pack()
x, y = spaceship.getX(), spaceship.getY()
spaceship_shape = canvas.create_polygon(x-10, y+10, x+10, y+10, x, y-10, fill="yellow")

canvas.bind("<Motion>", move_spaceship)
root.bind("<space>", fire_projectile)
root.after(500, update_meteors)
root.after(100, update_projectiles)
root.mainloop()
