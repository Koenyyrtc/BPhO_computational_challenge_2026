import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.widgets import Slider, RadioButtons, CheckButtons
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec

h   = 6.626e-34   
m_e = 9.109e-31   
e   = 1.602e-19   
r   = 65e-3       

D1 = 0.123e-9
D2 = 0.213e-9

V_MIN, V_MAX = 1000, 5000 
phosphor_cmap = LinearSegmentedColormap.from_list(
    "phosphor",
    [(0, "#000000"), (0.3, "#003300"), (0.7, "#00bb44"), (1.0, "#ccffcc")]
)

def de_broglie(V):
    """Return de Broglie wavelength in metres for accelerating voltage V."""
    return h / np.sqrt(2 * m_e * e * V)

def ring_radii(V, d_values, n_max=5):

    # x = r * sin(2φ),  sin(φ/2) = nλ/(2d)
    
    lam = de_broglie(V)
    rings = []
    for d in d_values:
        for n in range(1, n_max + 1):
            sin_half_phi = (n * lam) / (2 * d)
            if sin_half_phi >= 1.0:
                break
            half_phi = np.arcsin(sin_half_phi)
            phi      = 2 * half_phi
            x        = r * np.sin(2 * phi)   # metres
            rings.append((x * 1e3, d, n, phi))   # x in mm
    return rings

def build_verification_data(d_values, n_max=3):
    voltages = np.linspace(V_MIN, V_MAX, 300)
    data = {d: {"inv_sqrtV": [], "sin_half_phi": []} for d in d_values}
    for V in voltages:
        lam = de_broglie(V)
        inv_sqV = 1 / np.sqrt(V)
        for d in d_values:
            for n in range(1, n_max + 1):
                s = (n * lam) / (2 * d)
                if s < 1.0:
                    data[d]["inv_sqrtV"].append(inv_sqV)
                    data[d]["sin_half_phi"].append(s)
    return data

class AnimState:
    def __init__(self):
        self.running    = False
        self.frame      = 0
        self.total      = 40      # frames for one pulse
        self.rings_data = []
        self.trigger_V  = None

anim_state = AnimState()


fig = plt.figure(figsize=(16, 9), facecolor="#0a0a0a")
fig.suptitle("Electron Diffraction Simulator", color="#00ff88",
             fontsize=18, fontweight="bold", fontfamily="monospace", y=0.97)

gs = gridspec.GridSpec(
    3, 3,
    figure=fig,
    left=0.06, right=0.97,
    top=0.92, bottom=0.10,
    hspace=0.45, wspace=0.38
)

ax_screen = fig.add_subplot(gs[0:2, 0:2])   # Phosphor screen (large)
ax_tube   = fig.add_subplot(gs[2,   0:2])   # Tube diagram
ax_graph  = fig.add_subplot(gs[0:2, 2])     # graph
ax_info   = fig.add_subplot(gs[2,   2])     # Info panel

for ax in [ax_screen, ax_tube, ax_graph, ax_info]:
    ax.set_facecolor("#050505")
    for spine in ax.spines.values():
        spine.set_color("#1a3a1a")

ax_screen.set_xlim(-75, 75)
ax_screen.set_ylim(-75, 75)
ax_screen.set_aspect("equal")
ax_screen.set_title("Phosphor Screen", color="#00cc66",
                     fontfamily="monospace", fontsize=11)
ax_screen.tick_params(colors="#336633")
ax_screen.set_xlabel("x  (mm)", color="#336633", fontfamily="monospace")
ax_screen.set_ylabel("y  (mm)", color="#336633", fontfamily="monospace")
for label in ax_screen.get_xticklabels() + ax_screen.get_yticklabels():
    label.set_color("#336633")

theta_bg = np.linspace(0, 2 * np.pi, 500)
for rad, alpha in zip([70, 60, 50], [0.04, 0.06, 0.08]):
    ax_screen.fill(rad * np.cos(theta_bg), rad * np.sin(theta_bg),
                   color="#003300", alpha=alpha, zorder=0)

beam_spot = plt.Circle((0, 0), 1.5, color="#ffffff", zorder=5)
ax_screen.add_patch(beam_spot)

ring_artists = []

# diagram
ax_tube.set_xlim(0, 10)
ax_tube.set_ylim(-1.5, 1.5)
ax_tube.set_aspect("equal")
ax_tube.set_title("Electron Tube  (schematic)", color="#00cc66",
                   fontfamily="monospace", fontsize=10)
ax_tube.axis("off")

# Tube body
tube_rect = patches.FancyBboxPatch((0.3, -0.5), 7.0, 1.0,
    boxstyle="round,pad=0.05", linewidth=1.5,
    edgecolor="#225522", facecolor="#0a140a")
ax_tube.add_patch(tube_rect)

# Filament (cathode)
ax_tube.plot([0.8, 0.8], [-0.4, 0.4], color="#ffaa00", linewidth=3, zorder=4)
ax_tube.text(0.8, -0.75, "Cathode\n(filament)", color="#ffaa00",
             ha="center", fontsize=7, fontfamily="monospace")

# Anode
ax_tube.plot([2.2, 2.2], [-0.45, 0.45], color="#4488ff", linewidth=2, zorder=4)
ax_tube.text(2.2, -0.75, "Anode", color="#4488ff",
             ha="center", fontsize=7, fontfamily="monospace")

# Graphite target
graphite = patches.Ellipse((4.5, 0), 0.15, 0.8,
    facecolor="#444444", edgecolor="#888888", linewidth=1.5, zorder=4)
ax_tube.add_patch(graphite)
ax_tube.text(4.5, -0.75, "Graphite\ntarget", color="#888888",
             ha="center", fontsize=7, fontfamily="monospace")

# Screen (sphere cross-section)
screen_arc = patches.Arc((8.5, 0), 2.5, 2.5, angle=0,
    theta1=120, theta2=240, color="#00aa55", linewidth=2, zorder=4)
ax_tube.add_patch(screen_arc)
ax_tube.text(8.7, 0, "Screen", color="#00aa55",
             ha="left", va="center", fontsize=7, fontfamily="monospace")

# Beam line (static dashes)
ax_tube.plot([0.9, 4.4], [0, 0], color="#00ff88", linewidth=1,
             linestyle="--", alpha=0.3, zorder=3)
ax_tube.plot([4.6, 7.25], [0, 0], color="#00ff88", linewidth=1,
             linestyle="--", alpha=0.3, zorder=3)

beam_dot, = ax_tube.plot([], [], "o", color="#00ffcc",
                          markersize=8, zorder=10,
                          markeredgecolor="#ffffff", markeredgewidth=0.5)
beam_trail, = ax_tube.plot([], [], "-", color="#00ffcc",
                            linewidth=2, alpha=0.5, zorder=9)

V_label_tube = ax_tube.text(5.0, 1.1, "", color="#ffff66",
                              ha="center", fontsize=9, fontfamily="monospace",
                              fontweight="bold")

ax_graph.set_title("Bragg Verification\n1/√V  vs  sin(φ/2)",
                    color="#00cc66", fontfamily="monospace", fontsize=10)
ax_graph.set_xlabel("sin(½φ)", color="#336633", fontfamily="monospace", fontsize=9)
ax_graph.set_ylabel("1/√V   (V⁻¹/²)", color="#336633", fontfamily="monospace", fontsize=9)
ax_graph.tick_params(colors="#336633", labelsize=7)
for label in ax_graph.get_xticklabels() + ax_graph.get_yticklabels():
    label.set_color("#336633")


d_colors = {D1: "#00ff88", D2: "#ff6644"}
d_labels = {D1: "d₁ = 0.123 nm", D2: "d₂ = 0.213 nm"}
ver_data  = build_verification_data([D1, D2])

for d, col in d_colors.items():
    xs = ver_data[d]["sin_half_phi"]
    ys = ver_data[d]["inv_sqrtV"]
    ax_graph.scatter(xs, ys, color=col, s=1, alpha=0.6, label=d_labels[d])
    # Fit line
    coeffs = np.polyfit(xs, ys, 1)
    x_fit  = np.array([min(xs), max(xs)])
    ax_graph.plot(x_fit, np.polyval(coeffs, x_fit),
                  color=col, linewidth=1.5, linestyle="--", alpha=0.8)

ax_graph.legend(fontsize=7, facecolor="#0a0a0a", edgecolor="#225522",
                labelcolor="white", loc="upper left")
ax_graph.grid(True, color="#112211", linewidth=0.5)

graph_dot_d1, = ax_graph.plot([], [], "o", color="#00ff88", markersize=6, zorder=10)
graph_dot_d2, = ax_graph.plot([], [], "o", color="#ff6644", markersize=6, zorder=10)


ax_info.axis("off")
ax_info.set_title("Ring Data", color="#00cc66",
                   fontfamily="monospace", fontsize=10)
info_text = ax_info.text(0.05, 0.95, "", transform=ax_info.transAxes,
                          color="#00ee77", fontfamily="monospace", fontsize=8,
                          va="top", ha="left")

ax_slider = fig.add_axes([0.10, 0.03, 0.55, 0.025])
ax_slider.set_facecolor("#0a0a0a")
slider = Slider(ax_slider, "V  (kV)", V_MIN / 1000, V_MAX / 1000,
                valinit=3.0, color="#00aa55")
slider.label.set_color("#00cc66")
slider.label.set_fontfamily("monospace")
slider.valtext.set_color("#00ff88")
slider.valtext.set_fontfamily("monospace")

def draw_rings(V, alpha_scale=1.0):
    """Remove old rings and draw new ones for voltage V."""
    global ring_artists
    for art in ring_artists:
        art.remove()
    ring_artists.clear()

    rings = ring_radii(V, [D1, D2])
    theta = np.linspace(0, 2 * np.pi, 500)

    for (x_mm, d, n, phi) in rings:
        if x_mm > 74:
            continue
        col  = "#00ff88" if d == D1 else "#ff6644"
        # Glow layers
        for width, alp in [(4, 0.08), (2.5, 0.15), (1.2, 0.55 * alpha_scale)]:
            circ, = ax_screen.plot(
                x_mm * np.cos(theta), x_mm * np.sin(theta),
                color=col, linewidth=width, alpha=alp, zorder=3
            )
            ring_artists.append(circ)

    return rings


def update_info(V, rings):
    lam = de_broglie(V) * 1e12   # pm
    lines = [f"V  = {V/1000:.2f} kV",
             f"λ  = {lam:.3f} pm",
             ""]
    for x_mm, d, n, phi in rings:
        d_nm = d * 1e9
        lines.append(f"n={n} d={d_nm:.3f}nm  x={x_mm:.1f}mm")
    info_text.set_text("\n".join(lines))


def update_graph_dots(rings):
    pts_d1 = [(np.sin(phi / 2), 1 / np.sqrt(V_val))
               for x_mm, d, n, phi in rings if d == D1
               for V_val in [slider.val * 1000]]
    pts_d2 = [(np.sin(phi / 2), 1 / np.sqrt(V_val))
               for x_mm, d, n, phi in rings if d == D2
               for V_val in [slider.val * 1000]]

    if pts_d1:
        graph_dot_d1.set_data([p[0] for p in pts_d1], [p[1] for p in pts_d1])
    else:
        graph_dot_d1.set_data([], [])
    if pts_d2:
        graph_dot_d2.set_data([p[0] for p in pts_d2], [p[1] for p in pts_d2])
    else:
        graph_dot_d2.set_data([], [])

BEAM_PATH_X = np.array([0.9, 4.4, 7.25])   
BEAM_PATH_BREAKS = [0, 20, 40]             

def beam_x_at_frame(frame):
    if frame <= BEAM_PATH_BREAKS[1]:
        t = frame / BEAM_PATH_BREAKS[1]
        return BEAM_PATH_X[0] + t * (BEAM_PATH_X[1] - BEAM_PATH_X[0])
    else:
        t = (frame - BEAM_PATH_BREAKS[1]) / (BEAM_PATH_BREAKS[2] - BEAM_PATH_BREAKS[1])
        return BEAM_PATH_X[1] + t * (BEAM_PATH_X[2] - BEAM_PATH_X[1])

def animate(frame):
    if not anim_state.running:
        return

    f = anim_state.frame
    bx = beam_x_at_frame(f)

    trail_start = beam_x_at_frame(max(0, f - 8))
    beam_dot.set_data([bx], [0])
    beam_trail.set_data([trail_start, bx], [0, 0])

    if f >= BEAM_PATH_BREAKS[1]:
        alpha = (f - BEAM_PATH_BREAKS[1]) / (BEAM_PATH_BREAKS[2] - BEAM_PATH_BREAKS[1])
        draw_rings(anim_state.trigger_V, alpha_scale=alpha)

    anim_state.frame += 1
    if anim_state.frame >= anim_state.total:
        anim_state.running = False
        beam_dot.set_data([], [])
        beam_trail.set_data([], [])
        rings = draw_rings(anim_state.trigger_V, alpha_scale=1.0)
        update_info(anim_state.trigger_V, rings)
        update_graph_dots(rings)

ani = animation.FuncAnimation(fig, animate, interval=30, blit=False)

last_V = [slider.val * 1000]

def on_slider(val):
    V = val * 1000
    V_label_tube.set_text(f"V = {V/1000:.1f} kV")
    anim_state.trigger_V = V
    anim_state.frame     = 0
    anim_state.running   = True
    last_V[0] = V

slider.on_changed(on_slider)
V0    = slider.val * 1000
rings0 = draw_rings(V0)
update_info(V0, rings0)
update_graph_dots(rings0)
V_label_tube.set_text(f"V = {V0/1000:.1f} kV")

ax_screen.plot([], [], color="#00ff88", label="d₁ = 0.123 nm", linewidth=1.5)
ax_screen.plot([], [], color="#ff6644", label="d₂ = 0.213 nm", linewidth=1.5)
ax_screen.legend(fontsize=7, facecolor="#050505", edgecolor="#225522",
                 labelcolor="white", loc="lower right")

plt.show()
