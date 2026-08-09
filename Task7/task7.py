import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider

hbar = 1.0546e-34   # J·s
m_e  = 9.1094e-31   # kg
eV   = 1.6022e-19   # J per eV
a = 0.5e-10         # box width in metres
x = np.linspace(0, a, 1000)

def energy(n, m=m_e, box=a):
    return (hbar**2 * np.pi**2 * n**2) / (2 * m * box**2)
def psi_spatial(n, x, box=a):
    return np.sqrt(2 / box) * np.sin(n * np.pi * x / box)

def prob_density(n, x, box=a):
    return psi_spatial(n, x, box)**2

ns   = np.arange(1, 6)
E_eV = [energy(n) / eV for n in ns]

fig1, ax1 = plt.subplots(figsize=(6, 5))
ax1.plot(ns, E_eV, 'o--', color='royalblue', lw=2, markersize=8)
for n, E in zip(ns, E_eV):
    ax1.annotate(f'n={n}\n{E:.1f} eV', (n, E),
                 textcoords='offset points', xytext=(8, 0), fontsize=8)
ax1.set_xlabel('Quantum number n')
ax1.set_ylabel('Energy / eV')
ax1.set_title(f'Particle-in-a-box energy\nm = {m_e:.4e} kg,  a = {a*1e10:.1f} Å')
ax1.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('energy_vs_n.png', dpi=150)
print("Saved: energy_vs_n.png")

colours = ['royalblue', 'forestgreen', 'crimson']
fig2, ax2 = plt.subplots(figsize=(7, 5))
for n, c in zip([1, 2, 3], colours):
    pd = prob_density(n, x)
    E  = energy(n) / eV
    ax2.plot(x * 1e10, pd, color=c, lw=2,
             label=f'n = {n}  E = {E:.4f} eV')
ax2.set_xlabel('x / Å')
ax2.set_ylabel('Probability density  |ψ|²')
ax2.set_title(f'Particle in a box\nm = {m_e:.4e} kg')
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('prob_density.png', dpi=150)
print("Saved: prob_density.png")

# ψ_n(x,t) = ψ_n(x) · e^{-iE_n t/ħ}   ->   Re[ψ] = ψ_n(x)·cos(E_n t/ħ)

fig3, ax3 = plt.subplots(figsize=(8, 5))
plt.subplots_adjust(bottom=0.2)

n_anim  = 2
omega   = energy(n_anim) / hbar          # angular freq
T       = 2 * np.pi / omega              
psi_x   = psi_spatial(n_anim, x)

line_re,  = ax3.plot(x * 1e10, psi_x,        color='dodgerblue', lw=2, label='Re[ψ(x,t)]')
line_pd,  = ax3.plot(x * 1e10, psi_x**2,     color='crimson',    lw=2, label='|ψ(x,t)|²', linestyle='--')
ax3.set_xlim(0, a * 1e10)
ax3.set_ylim(-max(abs(psi_x)) * 1.3, max(abs(psi_x)) * 1.3)
ax3.set_xlabel('x / Å')
ax3.set_ylabel('ψ  or  |ψ|²')
ax3.set_title(f'Time evolution  n = {n_anim}  (Special Feature: animated)')
ax3.legend()
ax3.grid(True, alpha=0.3)
time_text = ax3.text(0.02, 0.92, '', transform=ax3.transAxes, fontsize=9)

ax_slider = plt.axes([0.15, 0.05, 0.65, 0.03])
slider_n  = Slider(ax_slider, 'n', 1, 5, valinit=n_anim, valstep=1)

def update_n(val):
    global psi_x, omega
    n_new  = int(slider_n.val)
    psi_x  = psi_spatial(n_new, x)
    omega  = energy(n_new) / hbar
    ax3.set_title(f'Time evolution  n = {n_new}  (Special Feature: animated)')

slider_n.on_changed(update_n)

frames = 120

def animate(frame):
    theta = 2 * np.pi * frame / frames
    n_cur = int(slider_n.val)
    ps    = psi_spatial(n_cur, x)
    re_psi = ps * np.cos(theta)
    pd     = ps**2                       
    line_re.set_ydata(re_psi)
    line_pd.set_ydata(pd)
    time_text.set_text(f'phase θ = {theta:.2f} rad')
    return line_re, line_pd, time_text

ani = animation.FuncAnimation(fig3, animate, frames=frames,
                              interval=50, blit=True)
plt.show()

print("\nDone. Close the animation window to exit.")
print(f"\nEnergy levels (electron, a = {a*1e10:.1f} Å):")
for n in range(1, 6):
    print(f"  n={n}: E = {energy(n)/eV:.4f} eV")
