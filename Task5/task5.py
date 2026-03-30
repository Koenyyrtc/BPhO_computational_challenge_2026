# Special feature: hover over a line to see its transition details


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

R_H = 1.097e7       # Rydberg constant (m^-1)
h = 6.626e-34       # Planck's constant (J·s)
c = 3e8             # Speed of light (m/s)
eV = 1.602e-19      # Joules per eV

SERIES = [
    ("Lyman",    1, "purple"),
    ("Balmer",   2, "red"),
    ("Paschen",  3, "green"),
    ("Brackett", 4, "blue"),
    ("Pfund",    5, "orange"),
]

def photon_energy_eV(n1, n2):
    """E = R_H * hc * (1/n1^2 - 1/n2^2)  [eV]"""
    return R_H * h * c * (1/n1**2 - 1/n2**2) / eV

def wavelength_nm(n1, n2):
    """λ = 1 / (R_H * (1/n1^2 - 1/n2^2))  [nm]"""
    return 1 / (R_H * (1/n1**2 - 1/n2**2)) * 1e9

fig, ax = plt.subplots(figsize=(10, 6))
lines = []          
line_meta = []     

for name, n1, colour in SERIES:
    for n2 in range(n1 + 1, n1 + 8):
        lam = wavelength_nm(n1, n2)
        E   = photon_energy_eV(n1, n2)
        if lam > 8000:
            break
        ln, = ax.plot([lam, lam], [0, E], color=colour, lw=1.2, alpha=0.8,
                      label=name if n2 == n1 + 1 else "")
        lines.append(ln)
        line_meta.append((name, n1, n2, lam, E))

handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), fontsize=9)

ax.set_xlabel("Wavelength λ / nm", fontsize=11)
ax.set_ylabel("Photon energy / eV", fontsize=11)
ax.set_title("Bohr Model of Hydrogenic Atom\nPhoton Emissions: Z = 1", fontsize=12)
ax.set_xlim(0, 8000)
ax.set_ylim(0, 14)


annot = ax.annotate("", xy=(0, 0), xytext=(15, 15),
                    textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="lightyellow", ec="grey"),
                    fontsize=9)
annot.set_visible(False)

def on_move(event):
    if event.inaxes != ax:
        return
    for ln, (name, n1, n2, lam, E) in zip(lines, line_meta):
        cont, _ = ln.contains(event)
        if cont:
            annot.xy = (lam, E / 2)
            annot.set_text(f"{name} series\nn={n1} → n={n2}\nλ = {lam:.1f} nm\nE = {E:.3f} eV")
            annot.set_visible(True)
            fig.canvas.draw_idle()
            return
    annot.set_visible(False)
    fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", on_move)

plt.tight_layout()
plt.show()