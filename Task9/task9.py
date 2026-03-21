"""
Compton Scattering Simulator  —  Task #9
=========================================
Plots vs photon scattering angle θ (0-180°):
  1. Fractional wavelength shift  Δλ/λ
  2. Electron recoil speed  v/c
  3. Electron recoil angle  φ

Key formulae:
  Δλ = (h / m_e c)(1 - cosθ)           [Compton shift]
  λ  = hc / E_photon
  v  = c √[1 - (m_e c² / (hc/λ - hc/λ' + m_e c²))²]
  tan φ = sinθ / [1 + (h/m_e c λ)(1 - cosθ) - cosθ]
"""

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation
from matplotlib.widgets import Slider
from matplotlib.patches import FancyArrowPatch

h   = 6.62607e-34   # J·s
m_e = 9.10938e-31   # kg
c   = 2.99792e8     # m/s
e   = 1.60218e-19   # C (for keV conversion)
lc  = h / (m_e * c)  # Compton wavelength ≈ 2.426 pm

ENERGIES_keV = [50, 100, 200, 500, 1000]
COLORS = ["#00cfff", "#44ff88", "#ffdd00", "#ff8800", "#ff3366"]

theta_deg = np.linspace(0, 180, 1000)
theta_rad = np.radians(theta_deg)

def compute(E_keV):
    E = E_keV * 1e3 * e          # J
    lam = h * c / E              # initial wavelength

    delta_lam = lc * (1 - np.cos(theta_rad))
    lam_prime = lam + delta_lam

    frac_shift = delta_lam / lam  # Δλ/λ

    # Recoil speed
    E_prime = h * c / lam_prime
    E_kin   = E - E_prime
    gamma_m = E_kin / (m_e * c**2) + 1
    # relativistic: v/c = sqrt(1 - 1/γ²)
    # energy conservation: K = (γ-1)m_e c²
    # formula from slides:
    denom = h * c / lam - h * c / lam_prime + m_e * c**2
    ratio = (m_e * c**2 / denom) ** 2
    v_over_c = np.sqrt(np.maximum(0, 1 - ratio))

    with np.errstate(divide="ignore", invalid="ignore"):
        numer = np.sin(theta_rad)
        denom2 = (1 + (h / (m_e * c * lam)) * (1 - np.cos(theta_rad))
                  - np.cos(theta_rad))
        tan_phi = np.where(np.abs(denom2) < 1e-30, 0.0, numer / denom2)
        phi_deg = np.degrees(np.arctan(np.abs(tan_phi)))
        phi_deg = np.where(theta_deg == 0, 0, phi_deg)

    return frac_shift, v_over_c, phi_deg

all_data = {E: compute(E) for E in ENERGIES_keV}


fig = plt.figure(figsize=(17, 9.5), facecolor="#080808")
fig.suptitle("Compton Scattering Simulator", color="#ff6699",
             fontsize=19, fontweight="bold", fontfamily="monospace", y=0.98)

gs = gridspec.GridSpec(2, 4, figure=fig,
                       left=0.06, right=0.98,
                       top=0.93, bottom=0.12,
                       hspace=0.42, wspace=0.38)

ax1 = fig.add_subplot(gs[0, 0:2])   # Δλ/λ
ax2 = fig.add_subplot(gs[1, 0:2])   # v/c
ax3 = fig.add_subplot(gs[0, 2])     # φ
ax4 = fig.add_subplot(gs[1, 2])     # collision animator
ax5 = fig.add_subplot(gs[0:2, 3])   # info / equations panel

BG = "#080808"
for ax in [ax1, ax2, ax3, ax4, ax5]:
    ax.set_facecolor("#0d0d0d")
    for sp in ax.spines.values():
        sp.set_color("#3a1a2a")

GRID_KW = dict(color="#1e0e16", linewidth=0.6)
TICK_COL = "#8a4a6a"

for E, col in zip(ENERGIES_keV, COLORS):
    fs, vc, phi = all_data[E]
    lbl = f"E={E} keV"
    ax1.plot(theta_deg, fs,  color=col, linewidth=1.8, label=lbl, alpha=0.9)
    ax2.plot(theta_deg, vc,  color=col, linewidth=1.8, label=lbl, alpha=0.9)
    ax3.plot(theta_deg, phi, color=col, linewidth=1.8, label=lbl, alpha=0.9)

for ax, ylabel, title in [
    (ax1, "Δλ / λ", "Fractional Wavelength Shift"),
    (ax2, "Electron recoil speed  v/c", "Electron Recoil Speed"),
    (ax3, "Electron recoil angle φ  /deg", "Electron Recoil Angle"),
]:
    ax.set_xlabel("Photon scattering angle θ  /deg",
                  color=TICK_COL, fontfamily="monospace", fontsize=8)
    ax.set_ylabel(ylabel, color=TICK_COL, fontfamily="monospace", fontsize=8)
    ax.set_title(title, color="#ff88aa", fontfamily="monospace", fontsize=9)
    ax.set_xlim(0, 180)
    ax.grid(True, **GRID_KW)
    ax.tick_params(colors=TICK_COL, labelsize=7)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_color(TICK_COL)
    ax.legend(fontsize=6.5, facecolor="#0d0d0d", edgecolor="#3a1a2a",
              labelcolor="white", loc="upper left")

ax3.set_ylim(0, 92)

vline1 = ax1.axvline(x=90, color="#ffffff", linewidth=1, linestyle=":", alpha=0.5)
vline2 = ax2.axvline(x=90, color="#ffffff", linewidth=1, linestyle=":", alpha=0.5)
vline3 = ax3.axvline(x=90, color="#ffffff", linewidth=1, linestyle=":", alpha=0.5)


dots1 = [ax1.plot([], [], "o", color=col, markersize=5, zorder=10)[0]
         for col in COLORS]
dots2 = [ax2.plot([], [], "o", color=col, markersize=5, zorder=10)[0]
         for col in COLORS]
dots3 = [ax3.plot([], [], "o", color=col, markersize=5, zorder=10)[0]
         for col in COLORS]


ax4.set_xlim(-2.5, 2.5)
ax4.set_ylim(-2.5, 2.5)
ax4.set_aspect("equal")
ax4.set_title("Live Collision  (E = 200 keV)", color="#ff88aa",
               fontfamily="monospace", fontsize=9)
ax4.axis("off")


ax4.annotate("", xy=(0.0, 0.0), xytext=(-2.3, 0.0),
             arrowprops=dict(arrowstyle="-|>", color="#ff4444",
                             lw=2.5, mutation_scale=18))
ax4.text(-2.3, 0.15, "X-ray  λ", color="#ff8888", fontsize=7.5,
         fontfamily="monospace")


elec = plt.Circle((0, 0), 0.22, color="#44dd66", zorder=5)
ax4.add_patch(elec)
ax4.text(-0.12, -0.12, "e⁻", color="#0a0a0a", fontsize=7,
         fontweight="bold", zorder=6)

phot_arrow = FancyArrowPatch((0, 0), (1.8, 0), arrowstyle="-|>",
                              color="#ff8800", linewidth=2.5,
                              mutation_scale=18, zorder=4)
elec_arrow = FancyArrowPatch((0, 0), (1.5, 0), arrowstyle="-|>",
                              color="#00ddff", linewidth=2.5,
                              mutation_scale=18, zorder=4)
ax4.add_patch(phot_arrow)
ax4.add_patch(elec_arrow)

phot_lbl = ax4.text(1.9, 0.2, "λ'", color="#ffaa44",
                     fontsize=10, fontfamily="monospace", zorder=7)
elec_lbl = ax4.text(1.9, -0.2, "v", color="#44ddff",
                     fontsize=10, fontfamily="monospace", zorder=7)
theta_lbl = ax4.text(0.5, 0.25, "θ=90°", color="#ffffff",
                      fontsize=7.5, fontfamily="monospace", zorder=7)
phi_lbl   = ax4.text(0.5, -0.25, "φ=?", color="#aaddff",
                      fontsize=7.5, fontfamily="monospace", zorder=7)

# Arc for θ
theta_arc_data = np.linspace(0, np.pi / 2, 60)
arc_r = 0.55
theta_arc, = ax4.plot(arc_r * np.cos(theta_arc_data),
                       arc_r * np.sin(theta_arc_data),
                       color="#ffffff", linewidth=1, alpha=0.5)

ax4.plot([0, 2.3], [0, 0], "--", color="#555555", linewidth=0.8)

ax5.axis("off")
ax5.set_title("Equations & Current Values",
               color="#ff88aa", fontfamily="monospace", fontsize=9)

eq_text = (
    "Compton shift:\n"
    "  Δλ = (h/mₑc)(1−cosθ)\n\n"
    "Compton wavelength:\n"
    "  λc = h/mₑc ≈ 2.426 pm\n\n"
    "Photon wavelength:\n"
    "  λ = hc / E\n\n"
    "Recoil speed:\n"
    "  v = c√[1−(mₑc²/Etot)²]\n\n"
    "Recoil angle:\n"
    "  tanφ = sinθ /\n"
    "   [1+(h/mₑcλ)(1−cosθ)−cosθ]\n"
)
ax5.text(0.05, 0.98, eq_text, transform=ax5.transAxes,
         color="#cc88ff", fontfamily="monospace", fontsize=8,
         va="top", ha="left", linespacing=1.5)

info_box = ax5.text(0.05, 0.38, "", transform=ax5.transAxes,
                     color="#88ffcc", fontfamily="monospace", fontsize=8.5,
                     va="top", ha="left", linespacing=1.6,
                     bbox=dict(boxstyle="round,pad=0.4",
                               facecolor="#0a1a10", edgecolor="#225533"))

ax_sl = fig.add_axes([0.08, 0.05, 0.62, 0.025])
ax_sl.set_facecolor("#0d0d0d")
slider = Slider(ax_sl, "θ  (deg)", 0, 180, valinit=90,
                color="#cc3366", initcolor="none")
slider.label.set_color("#ff88aa")
slider.label.set_fontfamily("monospace")
slider.valtext.set_color("#ff88aa")
slider.valtext.set_fontfamily("monospace")

fig.text(0.73, 0.065, "Animator uses E = 200 keV",
         color="#888888", fontsize=8, fontfamily="monospace")

E_anim = 200

def update(val):
    th = slider.val
    th_rad = np.radians(th)
    idx = np.searchsorted(theta_deg, th)
    idx = min(idx, len(theta_deg) - 1)

    for vl in [vline1, vline2, vline3]:
        vl.set_xdata([th, th])

    for i, (E, col) in enumerate(zip(ENERGIES_keV, COLORS)):
        fs, vc, phi = all_data[E]
        dots1[i].set_data([th], [fs[idx]])
        dots2[i].set_data([th], [vc[idx]])
        dots3[i].set_data([th], [phi[idx]])

    fs_anim, vc_anim, phi_anim = all_data[E_anim]
    phi_val = phi_anim[idx]   # degrees
    phi_rad = np.radians(phi_val)

    L_phot = 1.8
    px, py = L_phot * np.cos(th_rad), L_phot * np.sin(th_rad)
    phot_arrow.set_positions((0, 0), (px, py))

    E0 = E_anim * 1e3 * e
    lam0 = h * c / E0
    dlam = lc * (1 - np.cos(th_rad))
    lam_p = lam0 + dlam
    Ep = h * c / lam_p
    ratio_E = Ep / E0   # 0..1
    r_col = 1.0
    g_col = 0.3 + 0.5 * ratio_E
    phot_arrow.set_color((r_col, g_col * 0.5, 0.0))

    L_elec = 1.5 * vc_anim[idx] + 0.3
    ex, ey = L_elec * np.cos(-phi_rad), L_elec * np.sin(-phi_rad)
    elec_arrow.set_positions((0, 0), (ex, ey))
    # Faster electron → brighter cyan
    cyan_bright = 0.3 + 0.7 * vc_anim[idx]
    elec_arrow.set_color((0.0, cyan_bright, 1.0))

    # Labels
    phot_lbl.set_position((px + 0.1, py + 0.05))
    elec_lbl.set_position((ex + 0.1, ey - 0.15))
    theta_lbl.set_text(f"θ={th:.0f}°")
    phi_lbl.set_text(f"φ={phi_val:.1f}°")
    phi_lbl.set_position((ex * 0.6 + 0.05, ey * 0.6 - 0.18))

    # θ arc
    arc_angles = np.linspace(0, th_rad, 60)
    theta_arc.set_data(arc_r * np.cos(arc_angles), arc_r * np.sin(arc_angles))

    lines = [f"θ  = {th:.1f}°\n"]
    for E in ENERGIES_keV:
        fs2, vc2, phi2 = all_data[E]
        lines.append(
            f"E={E:4d}keV: Δλ/λ={fs2[idx]:.3f}  "
            f"v/c={vc2[idx]:.3f}  φ={phi2[idx]:.1f}°"
        )
    info_box.set_text("\n".join(lines))

    fig.canvas.draw_idle()

slider.on_changed(update)
update(90)

plt.show()