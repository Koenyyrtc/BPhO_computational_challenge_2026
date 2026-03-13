import matplotlib.pyplot as plt
import random
import math


particle_num = 10
N = 10
s = 1
pi = 3.14159
cm = 1/2.54

x = [0] * particle_num
y = [0] * particle_num

graph = plt.scatter(x, y, color = "b")
plt.xlim(-10, 10)
plt.ylim(-10, 10)
fig = plt.gcf()
fig.set_size_inches(18*cm, 18*cm)
plt.pause(1)

for frame in range(N):
    for particle in range(particle_num):
        theta = random.uniform(0, 2*pi)
        x[particle] += s*math.cos(theta)
        y[particle] += s*math.sin(theta)
    
    graph.remove()
    graph = plt.scatter(x, y, color = "b")
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    
    plt.pause(0.25)

plt.pause(10)