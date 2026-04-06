import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Slider, RadioButtons

def classical_probs(theta_deg, phi_deg):
    t = np.radians(theta_deg)
    p = np.radians(phi_deg)
    match    = np.cos(t)**2 * np.cos(p)**2 + np.sin(t)**2 * np.sin(p)**2
    mismatch = 1 - match
    return match, mismatch

def quantum_probs(theta_deg, phi_deg):
    diff = np.radians(phi_deg - theta_deg)
    match    = np.cos(diff)**2
    mismatch = np.sin(diff)**2
    return match, mismatch

def eve_probs(theta_deg, phi_deg, eve_deg):
    """After Eve (at eve_deg) intercepts, Bob effectively sees classical
    probabilities from Eve's angle ε to his angle φ."""
    match_AE, _ = quantum_probs(theta_deg, eve_deg)   # Alice to Eve (quantum)
    match_EB, _ = quantum_probs(eve_deg,   phi_deg)   # Eve to Bob  (quantum, re-emitted)
    # Eve's interception breaks entanglement; combined match probability
    match    = match_AE * match_EB + (1 - match_AE) * (1 - match_EB)
    mismatch = 1 - match
    return match, mismatch

fig = plt.figure(figsize=(13, 8), facecolor='#0d1117')
fig.suptitle('Quantum Cryptography — Mismatch Probability Calculator',
             color='white', fontsize=14, fontweight='bold', y=0.97)

# axes positions
ax_polar  = fig.add_axes([0.03, 0.35, 0.28, 0.52], polar=True,
                          facecolor='#161b22')
ax_bar    = fig.add_axes([0.38, 0.38, 0.25, 0.48], facecolor='#161b22')
ax_sweep  = fig.add_axes([0.70, 0.38, 0.27, 0.48], facecolor='#161b22')

# slider axes
ax_theta  = fig.add_axes([0.10, 0.22, 0.35, 0.025])
ax_phi    = fig.add_axes([0.10, 0.16, 0.35, 0.025])
ax_eve    = fig.add_axes([0.10, 0.10, 0.35, 0.025])

# radio button
ax_mode   = fig.add_axes([0.60, 0.06, 0.18, 0.18], facecolor='#161b22')

for ax in [ax_bar, ax_sweep]:
    ax.set_facecolor('#161b22')
    for spine in ax.spines.values():
        spine.set_edgecolor('#30363d')
    ax.tick_params(colors='#8b949e')
    ax.yaxis.label.set_color('#8b949e')
    ax.xaxis.label.set_color('#8b949e')
    ax.title.set_color('white')

slider_style = dict(color='#238636')
s_theta = Slider(ax_theta, 'Alice θ (°)', 0, 180, valinit=30,
                 color='#1f6feb', track_color='#21262d')
s_phi   = Slider(ax_phi,   'Bob φ (°)',   0, 180, valinit=60,
                 color='#3fb950', track_color='#21262d')
s_eve   = Slider(ax_eve,   'Eve ε (°)',   0, 180, valinit=45,
                 color='#f85149', track_color='#21262d')

for s, label in [(s_theta, 'Alice θ (°)'), (s_phi, 'Bob φ (°)'), (s_eve, 'Eve ε (°)')]:
    s.label.set_color('white')
    s.valtext.set_color('white')

radio = RadioButtons(ax_mode, ('No Eve', 'Eve intercepts'),
                     activecolor='#f85149')
ax_mode.set_title('Mode', color='white', fontsize=9)
for label in radio.labels:
    label.set_color('white')
    label.set_fontsize(9)

phi_sweep = np.linspace(0, 180, 500)

def draw_polar(theta, phi, eve, mode):
    ax_polar.clear()
    ax_polar.set_facecolor('#161b22')
    ax_polar.tick_params(colors='#8b949e', labelsize=7)
    ax_polar.set_title('Detector angles', color='white', fontsize=9, pad=10)

    t = np.radians(theta)
    p = np.radians(phi)
    e = np.radians(eve)

    ax_polar.annotate('', xy=(t, 1), xytext=(0, 0),
        arrowprops=dict(arrowstyle='->', color='#1f6feb', lw=2.5))
    ax_polar.annotate('', xy=(p, 1), xytext=(0, 0),
        arrowprops=dict(arrowstyle='->', color='#3fb950', lw=2.5))
    if mode == 'Eve intercepts':
        ax_polar.annotate('', xy=(e, 0.85), xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', color='#f85149', lw=2,
                            linestyle='dashed'))
        ax_polar.text(e, 0.92, 'Eve ε', color='#f85149', fontsize=8,
                      ha='center')

    ax_polar.text(t, 1.08, f'Alice θ={theta:.0f}°', color='#1f6feb',
                  fontsize=8, ha='center')
    ax_polar.text(p, 1.08, f'Bob φ={phi:.0f}°', color='#3fb950',
                  fontsize=8, ha='center')
    ax_polar.set_ylim(0, 1.2)
    ax_polar.set_yticklabels([])
    ax_polar.grid(color='#30363d', alpha=0.5)


def draw_bars(theta, phi, eve, mode):
    ax_bar.clear()
    ax_bar.set_facecolor('#161b22')
    for spine in ax_bar.spines.values():
        spine.set_edgecolor('#30363d')
    ax_bar.tick_params(colors='#8b949e')

    cm, cM = classical_probs(theta, phi)
    qm, qM = quantum_probs(theta, phi)

    if mode == 'Eve intercepts':
        em, eM = eve_probs(theta, phi, eve)
        labels  = ['Classical', 'Quantum\n(no Eve)', 'Quantum\n(+ Eve)']
        matches = [cm, qm, em]
        mismatches = [cM, qM, eM]
        colors_m  = ['#388bfd', '#3fb950', '#f85149']
        colors_mm = ['#1f4e8c', '#1a6030', '#8c1c1c']
    else:
        labels  = ['Classical', 'Quantum']
        matches = [cm, qm]
        mismatches = [cM, qM]
        colors_m  = ['#388bfd', '#3fb950']
        colors_mm = ['#1f4e8c', '#1a6030']

    x = np.arange(len(labels))
    w = 0.35
    bars1 = ax_bar.bar(x - w/2, matches,    w, color=colors_m,  label='Match',    alpha=0.9)
    bars2 = ax_bar.bar(x + w/2, mismatches, w, color=colors_mm, label='Mismatch', alpha=0.9)

    for bar in list(bars1) + list(bars2):
        h = bar.get_height()
        ax_bar.text(bar.get_x() + bar.get_width()/2, h + 0.01,
                    f'{h:.2f}', ha='center', va='bottom',
                    color='white', fontsize=8)

    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(labels, color='white', fontsize=8)
    ax_bar.set_ylim(0, 1.15)
    ax_bar.set_ylabel('Probability', color='#8b949e')
    ax_bar.set_title('Match vs Mismatch', color='white', fontsize=10)
    ax_bar.legend(fontsize=8, facecolor='#21262d', labelcolor='white',
                  edgecolor='#30363d')
    ax_bar.grid(axis='y', color='#30363d', alpha=0.5)


def draw_sweep(theta, phi, eve, mode):
    ax_sweep.clear()
    ax_sweep.set_facecolor('#161b22')
    for spine in ax_sweep.spines.values():
        spine.set_edgecolor('#30363d')
    ax_sweep.tick_params(colors='#8b949e')

    cm_sw = [classical_probs(theta, p)[1] for p in phi_sweep]
    qm_sw = [quantum_probs(theta, p)[1]   for p in phi_sweep]

    ax_sweep.plot(phi_sweep, cm_sw, color='#388bfd', lw=2, label='Classical mismatch')
    ax_sweep.plot(phi_sweep, qm_sw, color='#3fb950', lw=2, label='Quantum mismatch')

    if mode == 'Eve intercepts':
        em_sw = [eve_probs(theta, p, eve)[1] for p in phi_sweep]
        ax_sweep.plot(phi_sweep, em_sw, color='#f85149', lw=2,
                      linestyle='--', label='Quantum + Eve')

    ax_sweep.axvline(phi, color='white', lw=1, linestyle=':', alpha=0.6)
    ax_sweep.set_xlabel("Bob's angle φ (°)", color='#8b949e')
    ax_sweep.set_ylabel('P(mismatch)', color='#8b949e')
    ax_sweep.set_title(f'Mismatch vs φ  (Alice θ={theta:.0f}°)', color='white', fontsize=10)
    ax_sweep.legend(fontsize=8, facecolor='#21262d', labelcolor='white',
                    edgecolor='#30363d')
    ax_sweep.grid(color='#30363d', alpha=0.4)
    ax_sweep.set_xlim(0, 180)
    ax_sweep.set_ylim(0, 1.05)


def update(_=None):
    theta = s_theta.val
    phi   = s_phi.val
    eve   = s_eve.val
    mode  = radio.value_selected
    draw_polar(theta, phi, eve, mode)
    draw_bars(theta, phi, eve, mode)
    draw_sweep(theta, phi, eve, mode)
    fig.canvas.draw_idle()

s_theta.on_changed(update)
s_phi.on_changed(update)
s_eve.on_changed(update)
radio.on_clicked(update)


update()
plt.show()