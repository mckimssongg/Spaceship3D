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

    for i in reversed(range(game.getMeteorCount())):
        meteor = game.getMeteor(i)
        x, y = meteor.getX(), meteor.getY()
        update_meteor_shape(meteor_shapes[i], x, y, 10)

        collision_distance = 15.0
        if spaceship.collidesWithMeteor(meteor, collision_distance):
            canvas.delete(meteor_shapes[i])
            game.destroyMeteor(i)
            del meteor_shapes[i]

    root.after(500, update_meteors)

def draw_meteor(x, y, size):
    points = [(round(x + size * math.cos(math.radians(angle))), round(y + size * math.sin(math.radians(angle)))) for angle in range(0, 360, 60)]
    flat_points = [coord for point in points for coord in point]
    return canvas.create_polygon(*flat_points, outline="red", fill="red")

def update_meteor_shape(shape, x, y, size):
    points = [(round(x + size * math.cos(math.radians(angle))), round(y + size * math.sin(math.radians(angle)))) for angle in range(0, 360, 60)]
    flat_points = [coord for point in points for coord in point]
    canvas.coords(shape, *flat_points)

def fire_projectile(event):
    x, y = spaceship.getX(), spaceship.getY()
    size = 5
    projectile_shape = canvas.create_oval(x - size, y - size, x + size, y + size, fill="yellow")
    projectiles_shapes.append(projectile_shape)
    game.addProjectile(x, y)

def update_projectiles():
    global projectiles_shapes

    game.moveProjectiles(0, -10)
    new_projectiles_shapes = []

    if game.projectileCollidesWithMeteor(15.0):
        # Asumiendo que el método 'projectileCollidesWithMeteor' elimina proyectiles y meteoros colisionados
        # debemos actualizar la lista de shapes para reflejar estos cambios.
        # Aquí deberías implementar la lógica para eliminar las shapes de los proyectiles y meteoros colisionados.
        pass

    for i in range(game.getProjectileCount()):
        projectile = game.getProjectile(i)
        x, y = projectile.getX(), projectile.getY()
        canvas.coords(projectiles_shapes[i], x - 5, y - 5, x + 5, y + 5)

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
