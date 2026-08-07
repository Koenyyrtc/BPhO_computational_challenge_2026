import numpy as np
import matplotlib.pyplot as plt

def zeff(Z):
    return Z - 1

def R(n, l, r, Z_eff):
    a0 = 1.0
    rho = Z_eff * r / a0

    if n == 2 and l == 1:  # 2p
        return (1/(2*np.sqrt(6))) * (rho) * np.exp(-rho/2)
    elif n == 3 and l == 2:  # 3d
        return (1/(81*np.sqrt(30))) * (rho**2) * np.exp(-rho/3)
    else:
        return np.exp(-rho) 

def Y(l, m, theta, phi):
    if l == 1:
        if m == -1:
            return np.sin(theta) * np.sin(phi)
        elif m == 0:
            return np.cos(theta)
        elif m == 1:
            return np.sin(theta) * np.cos(phi)

    if l == 2:
        if m == -2:
            return np.sin(theta)**2 * np.sin(2*phi)
        elif m == -1:
            return np.sin(theta) * np.sin(phi) * np.cos(theta)
        elif m == 0:
            return (3*np.cos(theta)**2 - 1)
        elif m == 1:
            return np.sin(theta) * np.cos(phi) * np.cos(theta)
        elif m == 2:
            return np.sin(theta)**2 * np.cos(2*phi)

    return 0

# ---- Parameters ----
Z = 8
n, l = 3, 2   # 3d orbital
Z_eff = zeff(Z)

# Morph parameter (0 → m1, 1 → m2)
m1, m2 = -2, 2
t = 0.5  # change between 0 and 1 to animate morph

# ---- 2D grid ----
x = np.linspace(-10, 10, 200)
y = np.linspace(-10, 10, 200)
X, Yg = np.meshgrid(x, y)
Zplane = 0

r = np.sqrt(X**2 + Yg**2 + Zplane**2)
theta = np.arccos(np.divide(Zplane, r, where=r!=0))
phi = np.arctan2(Yg, X)

Y1 = Y(l, m1, theta, phi)
Y2 = Y(l, m2, theta, phi)

Ymix = (1 - t)*Y1 + t*Y2
psi = R(n, l, r, Z_eff) * Ymix
prob = psi**2

plt.figure()
plt.imshow(prob, extent=[-10,10,-10,10], origin='lower')
plt.colorbar(label='|ψ|²')
plt.title(f"2D Morph m={m1} → m={m2}, t={t:.2f}")
plt.xlabel("x")
plt.ylabel("y")
plt.show()

from mpl_toolkits.mplot3d import Axes3D

grid = np.linspace(-10, 10, 60)
X3, Y3, Z3 = np.meshgrid(grid, grid, grid)

r3 = np.sqrt(X3**2 + Y3**2 + Z3**2)
theta3 = np.arccos(np.divide(Z3, r3, where=r3!=0))
phi3 = np.arctan2(Y3, X3)

Y1_3 = Y(l, m1, theta3, phi3)
Y2_3 = Y(l, m2, theta3, phi3)
Ymix3 = (1 - t)*Y1_3 + t*Y2_3

psi3 = R(n, l, r3, Z_eff) * Ymix3
prob3 = psi3**2

threshold = prob3.max() * 0.1

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

mask = prob3 > threshold
ax.scatter(X3[mask], Y3[mask], Z3[mask], c=prob3[mask], s=5)

ax.set_title(f"3D Morph m={m1} → m={m2}")
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()
