import tkinter as tk
import random
import geometria
import math

def move_spaceship(event):
    x, y = event.x, event.y
    dx, dy = x - spaceship.getX(), y - spaceship.getY()
    spaceship.move(dx, dy, 0)
    canvas.coords(spaceship_shape, x-10, y+10, x+10, y+10, x, y-10)

def update_meteors():
    global meteors, meteor_shapes
    new_meteors = []
    new_meteor_shapes = []
    
    if random.random() < 0.5:
        new_meteor = geometria.Meteor(random.randint(0, 400), 0, 0)
        x, y = new_meteor.getX(), new_meteor.getY()
        size = 5
        points = [(round(x + size * math.cos(math.radians(angle))), round(y + size * math.sin(math.radians(angle)))) for angle in range(0, 360, 60)]
        flat_points = [coord for point in points for coord in point]
        new_shape = canvas.create_polygon(*flat_points, fill="red")
        meteors.append(new_meteor)
        meteor_shapes.append(new_shape)
    
    for meteor, shape in zip(meteors, meteor_shapes):
        meteor.move(0, 10, 0)
        x, y = meteor.getX(), meteor.getY()
        size = 5
        points = [(round(x + size * math.cos(math.radians(angle))), round(y + size * math.sin(math.radians(angle)))) for angle in range(0, 360, 60)]
        flat_points = [coord for point in points for coord in point]
        canvas.coords(shape, *flat_points)
        
        collision_distance = 15.0
        if spaceship.collidesWithMeteor(meteor, collision_distance):
            canvas.delete(shape)
        else:
            new_meteors.append(meteor)
            new_meteor_shapes.append(shape)

    meteors = new_meteors
    meteor_shapes = new_meteor_shapes
    root.after(500, update_meteors)

spaceship = geometria.Spaceship(200.0, 200.0, 0.0)
root = tk.Tk()
root.title("Meteor Destroyer")
canvas = tk.Canvas(root, width=400, height=400, bg="black")
canvas.pack()
x, y = spaceship.getX(), spaceship.getY()
spaceship_shape = canvas.create_polygon(x-10, y+10, x+10, y+10, x, y-10, fill="yellow")
meteors = [geometria.Meteor(random.randint(0, 400), random.randint(0, 200), 0) for _ in range(10)]
meteor_shapes = []
for meteor in meteors:
    x, y = meteor.getX(), meteor.getY()
    size = 5
    points = [(round(x + size * math.cos(math.radians(angle))), round(y + size * math.sin(math.radians(angle)))) for angle in range(0, 360, 60)]
    flat_points = [coord for point in points for coord in point]
    shape = canvas.create_polygon(*flat_points, fill="red")
    meteor_shapes.append(shape)

canvas.bind("<Motion>", move_spaceship)
root.after(500, update_meteors)
root.mainloop()
