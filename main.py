import time
import math
import pygame
import sys

#values
g = 9.81
PPM = 100.0
ball_radius = 0.5
#x, y values
initial_velocity = [0.0, 10.0]
velocity = [0.0, 0.0]
sum_forces = [0.0, 0.0]
acceleration = [0.0, 0.0]
displacement = [0.0, 0.0]
forces = [0.0, 0.0]
position = [0.0, 0.0]
#time
dt = 0.1
current_time = 0
time_duration = 10

#classes
class Material:
    def __init__(self ,name ,roughness ,e ,density ,colour):
        self.name = name
        self.roughness = roughness         #coefficient of friction
        self.e = e                         #coefficient of restitution 0<=e<=1
        self.density = density
        self.colour = colour

#materials
wood = Material("wood",0.3, 0.45,700 , (140, 70,20))
rubber = Material("rubber" ,0.80, 0.85,1100 , (35, 35, 35))
glass = Material("glass" ,0.15, 0.92,2500 , (173, 216, 230))
steel = Material("steel" ,0.20, 0.60,7850 , (170, 170, 170))
class Particle:
    def __init__(self, name, radius, material):
        self.name = name
        self.radius = radius
        self.material = material
        self.velocity = [0.0, 0.0]
        self.acceleration = [0.0, 0.0]
        self.displacement = [0.0, 0.0]
        self.position = [0.0, 0.0]
#particles
ball = Particle("ball",ball_radius ,rubber)


#TEMP!
current_material = glass
e = current_material.e
mu = current_material.roughness
density = current_material.density
mass = (4/3) * math.pi * (ball_radius**3) * density

#forces
def air_resistance_f(velocity):
    density_air = 1.225
    drag_coefficient = 0.47
    area = math.pi * (ball_radius**2)
    force_magnitude = 0.5 * density_air * (velocity**2) * drag_coefficient * area
    if velocity > 0.0 :
        force = -force_magnitude
    else:
        force = force_magnitude
    return force

weight = mass * g

screen_width = 1920
screen_height = 1080

world_centre = [(screen_width/2) / PPM ,(screen_height/2) / PPM]
offset = [0 ,0]
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()
fps_font = pygame.font.SysFont(None, 30)
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                PPM += 10
            elif event.button == 5:
                PPM -= 10
                if PPM < 10:
                    PPM = 10
        elif event.type == pygame.VIDEORESIZE:
            screen_width = event.w
            screen_height = event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    current_fps = clock.get_fps()
    # Arguments: (Text string, Anti-aliasing True/False, Text Color)
    fps_surface = fps_font.render(f"FPS: {current_fps}", True, (255, 255, 255))
    #tick rate
    dt = clock.tick() / 1000.0
    if dt > 0.1:
        dt = 1/60
    #rendered objects
    offset[0] = (screen_width/2)
    offset[1] = (screen_height/2)
    screen.fill((44, 48, 54))
    screen.blit(fps_surface, (10, 10))
    position[0] = ((displacement[0] * PPM) + offset[0])
    position[1] = ((displacement[1] * PPM) + offset[1])
    pygame.draw.circle(screen, (155, 0, 0), (position[0], position[1]), int(ball_radius * PPM))
    rectangle_height = 100
    rectangle_length = 80
    pygame.draw.rect(screen, (155,155,155),((offset[0] - (rectangle_length/2)*PPM)  ,((4)*PPM) + offset[1] ,rectangle_length*PPM ,rectangle_height*PPM ))
    #X forcecomponents

    #Y force components
    drag_AR = air_resistance_f(velocity[1])
    sum_forces[1] = drag_AR + weight
    #collisions
    if displacement[1] >= 4-ball_radius:
        displacement[1] = 4-ball_radius
        if abs(velocity[1]) > 0.1:
            velocity[1] *= -e
        else:
            velocity[1] = 0
            normal_force = -sum_forces[1]
            sum_forces[1] += normal_force  #reaction force
    #acceleration velocity displacement
    acceleration[1] = sum_forces[1] / mass
    velocity[1] += acceleration[1] * dt
    displacement[1] += velocity[1] * dt



#console
    print(f"seconds :{current_time}")
    #Y values
    print(f"total force  X: {sum_forces[0]} Y:{sum_forces[1]}")
    print(f"acceleration X: {acceleration[0]} Y:{acceleration[1]}")
    print(f"velocity     X: {velocity[0]} Y:{velocity[1]}")
    print(f"displacement X: {displacement[0]} Y:{displacement[1]}")


    current_time += dt
    pygame.display.flip()








