import tkinter as tk
import random
import geometria
import math

projectiles = []
game = geometria.Game()

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
        points = [(round(x + size * math.cos(math.radians(angle))), round(y + size * math.sin(math.radians(angle)))) for angle in range(0, 360, 60)]
        flat_points = [coord for point in points for coord in point]
        new_shape = canvas.create_polygon(*flat_points, outline="red", fill="red")
        meteor_shapes.append(new_shape)

    existing_meteors = []

    for i in range(len(meteor_shapes)):
        meteor_shape = meteor_shapes[i]

        if canvas.coords(meteor_shape):
            meteor = game.getMeteor(i)
            meteor.move(0, 10, 0)
            x, y = meteor.getX(), meteor.getY()
            size = 10
            points = [(round(x + size * math.cos(math.radians(angle))), round(y + size * math.sin(math.radians(angle)))) for angle in range(0, 360, 60)]
            flat_points = [coord for point in points for coord in point]
            canvas.coords(meteor_shape, *flat_points)

            collision_distance = 15.0
            if spaceship.collidesWithMeteor(meteor, collision_distance):
                canvas.delete(meteor_shape)
                game.destroyMeteor(i)
            else:
                existing_meteors.append(meteor)

    meteor_shapes = [meteor_shapes[i] for i in range(len(meteor_shapes)) if canvas.coords(meteor_shapes[i])]
    meteor_shapes += [new_shape for new_shape in meteor_shapes if new_shape not in meteor_shapes]

    root.after(500, update_meteors)

def fire_projectile(event):
    x, y = spaceship.getX(), spaceship.getY()
    size = 5
    projectile = canvas.create_oval(x - size, y - size, x + size, y + size, fill="yellow")
    projectiles.append(projectile)

def update_projectiles():
    global projectiles

    new_projectiles = []
    for projectile in projectiles:
        canvas.move(projectile, 0, -10)
        x, y, *_ = canvas.coords(projectile)

        meteor_hit = False
        meteor_to_remove = None

        for i in range(len(meteor_shapes)):
            meteor_shape = meteor_shapes[i]

            if canvas.coords(meteor_shape):
                coords = canvas.coords(meteor_shape)
                x1, y1, x2, y2, *_ = coords

                if x1 <= x <= x2 and y1 <= y <= y2:
                    meteor_hit = True
                    meteor_to_remove = i
                    break

        if meteor_hit:
            canvas.delete(meteor_shapes[meteor_to_remove])
            game.destroyMeteor(meteor_to_remove)
            canvas.delete(projectile)
        else:
            new_projectiles.append(projectile)

    projectiles = new_projectiles
    root.after(100, update_projectiles)

spaceship = geometria.Spaceship(200.0, 200.0, 0.0)
root = tk.Tk()
root.title("Meteor Destroyer")
canvas = tk.Canvas(root, width=400, height=400, bg="black")
canvas.pack()
x, y = spaceship.getX(), spaceship.getY()
spaceship_shape = canvas.create_polygon(x-10, y+10, x+10, y+10, x, y-10, fill="yellow")
meteor_shapes = []

canvas.bind("<Motion>", move_spaceship)
root.bind("<space>", fire_projectile)
root.after(500, update_meteors)
root.after(100, update_projectiles)
root.mainloop()
