import numpy as np
import matplotlib.pyplot as plt
from scipy.special import sph_harm_y, genlaguerre
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

def R(n, l, r, Z_eff):
    a0 = 1.0
    rho = 2 * Z_eff * r / (n * a0)
    prefactor = np.sqrt((2*Z_eff/(n*a0))**3 *
                        np.math.factorial(n-l-1) /
                        (2*n*np.math.factorial(n+l)))
    laguerre = genlaguerre(n-l-1, 2*l+1)(rho)
    return prefactor * np.exp(-rho/2) * rho**l * laguerre

def slater_zeff(Z, n):
    if n == 1:
        return Z - 0.30
    elif n == 2:
        return Z - 0.85
    else:
        return Z - 1.00

Z = 8
n, l = 3, 2  
Z_eff = slater_zeff(Z, n)

# 3D grid
grid = np.linspace(-10, 10, 50)
X, Y, Z3 = np.meshgrid(grid, grid, grid)

r = np.sqrt(X**2 + Y**2 + Z3**2)
theta = np.arccos(np.divide(Z3, r, where=r!=0))
phi = np.arctan2(Y, X)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

m_values = list(range(-l, l+1))

def update(frame):
    ax.clear()

    t = frame / 50
    i = int(t * (len(m_values)-1))
    frac = (t * (len(m_values)-1)) - i

    m1 = m_values[i]
    m2 = m_values[min(i+1, len(m_values)-1)]

    psi1 = R(n, l, r, Z_eff) * sph_harm_y(l, m1, theta, phi)
    psi2 = R(n, l, r, Z_eff) * sph_harm_y(l, m2, theta, phi)

    psi = (1-frac)*psi1 + frac*psi2
    prob = np.abs(psi)**2

    threshold = prob.max() * 0.15
    mask = prob > threshold

    ax.scatter(X[mask], Y[mask], Z3[mask], c=prob[mask], s=5)

    ax.set_title(f"3D Morph: n={n}, l={l}, m≈{m1}→{m2}")
    ax.set_xlim(-10,10)
    ax.set_ylim(-10,10)
    ax.set_zlim(-10,10)

    return []

anim = FuncAnimation(fig, update, frames=50, interval=100)

plt.show()
