"""
BPhO Task #2 - Brownian Motion Simulation
==========================================
N small particles (mass m, radius r) moving randomly (random walk style).
One large particle (mass M, radius R) starts from rest at centre.
Collisions handled via conservation of momentum (coefficient of restitution C).

Units: nm for position, nm/ps for velocity, ps for time.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
import matplotlib.lines as mlines

BOX          = 300          # nm, box half-width
N_SMALL      = 80           # number of small particles
m_small      = 1.0          # mass of small particle
r_small      = 3.0          # radius of small particle
M_large      = 50.0         # mass of large particle
R_large      = 20.0         # radius of large particle
v_small      = 2.0          # speed of small particles
C_restitution= 1.0          # coefficient of restitution (1 = elastic)
Kn           = 20           # Knudsen number
DT           = 0.5          


rng = np.random.default_rng(42)

def init_particles():
    """Randomly place small particles, avoiding large particle zone."""
    pos = np.zeros((N_SMALL, 2))
    vel = np.zeros((N_SMALL, 2))
    angles = rng.uniform(0, 2*np.pi, N_SMALL)
    vel[:, 0] = v_small * np.cos(angles)
    vel[:, 1] = v_small * np.sin(angles)

    placed = 0
    while placed < N_SMALL:
        x = rng.uniform(-BOX + r_small, BOX - r_small)
        y = rng.uniform(-BOX + r_small, BOX - r_small)
        if np.sqrt(x**2 + y**2) > R_large + r_small + 10:
            pos[placed] = [x, y]
            placed += 1

    # Large particle starts at rest in the centre
    large_pos = np.array([0.0, 0.0])
    large_vel = np.array([0.0, 0.0])
    return pos, vel, large_pos, large_vel

pos_s, vel_s, pos_L, vel_L = init_particles()
steps_since_redirect = rng.integers(0, Kn, N_SMALL)
trail_L = [pos_L.copy()]
time_ps  = 0.0

def step(pos_s, vel_s, pos_L, vel_L, steps_since_redirect, C):
    global time_ps
    time_ps += DT

    # 1. Move small particles
    pos_s += vel_s * DT

    # 2. Bounce small particles off walls (reflect velocity)
    for i in range(N_SMALL):
        for ax in range(2):
            lim = BOX - r_small
            if pos_s[i, ax] < -lim:
                pos_s[i, ax] = -lim
                vel_s[i, ax] *= -1
            elif pos_s[i, ax] > lim:
                pos_s[i, ax] = lim
                vel_s[i, ax] *= -1

    # 3. Randomise small particle direction every Kn steps (Knudsen model)
    steps_since_redirect += 1
    redirect = steps_since_redirect >= Kn
    if redirect.any():
        n_redir = redirect.sum()
        new_angles = rng.uniform(0, 2*np.pi, n_redir)
        vel_s[redirect, 0] = v_small * np.cos(new_angles)
        vel_s[redirect, 1] = v_small * np.sin(new_angles)
        steps_since_redirect[redirect] = 0

    # 4. Move large particle
    pos_L = pos_L + vel_L * DT

    # 5. Bounce large particle off walls
    for ax in range(2):
        lim = BOX - R_large
        if pos_L[ax] < -lim:
            pos_L[ax] = -lim
            vel_L[ax] *= -1
        elif pos_L[ax] > lim:
            pos_L[ax] = lim
            vel_L[ax] *= -1

    # 6. Collision: small particles with large particle
    for i in range(N_SMALL):
        diff = pos_s[i] - pos_L
        dist = np.linalg.norm(diff)
        min_dist = r_small + R_large
        if dist < min_dist and dist > 1e-9:
            
            n = diff / dist

            
            v_rel = np.dot(vel_s[i] - vel_L, n)

            if v_rel < 0:

                J = -(1 + C) * v_rel / (1/m_small + 1/M_large)
                vel_s[i] += (J / m_small) * n
                vel_L    -= (J / M_large) * n


                overlap = min_dist - dist
                pos_s[i] += n * overlap * (M_large / (m_small + M_large))
                pos_L    -= n * overlap * (m_small / (m_small + M_large))

    return pos_s, vel_s, pos_L, vel_L, steps_since_redirect


fig, (ax_sim, ax_trail) = plt.subplots(1, 2, figsize=(13, 7))
plt.subplots_adjust(bottom=0.22, left=0.06, right=0.97, wspace=0.35)


ax_sim.set_xlim(-BOX, BOX); ax_sim.set_ylim(-BOX, BOX)
ax_sim.set_aspect('equal'); ax_sim.set_facecolor('#f8f8f8')
box_rect = patches.Rectangle((-BOX, -BOX), 2*BOX, 2*BOX,
                               linewidth=2, edgecolor='black',
                               facecolor='none', zorder=3)
ax_sim.add_patch(box_rect)
ax_sim.set_title('Brownian motion simulation: t = 0 ps', fontsize=11, fontweight='bold')
ax_sim.set_xlabel('x (nm)'); ax_sim.set_ylabel('y (nm)')


sc_small = ax_sim.scatter(pos_s[:, 0], pos_s[:, 1],
                           s=10, color='steelblue', marker='*', zorder=4)


large_circle = plt.Circle(pos_L, R_large, color='#cc3333', fill=False,
                           linewidth=1.5, zorder=5)
ax_sim.add_patch(large_circle)


trail_line, = ax_sim.plot([], [], 'r-', linewidth=0.8, alpha=0.7, zorder=4)


start_marker, = ax_sim.plot(0, 0, 'g*', markersize=10, zorder=6)


cur_marker, = ax_sim.plot(0, 0, 'r*', markersize=10, zorder=7)


ax_trail.set_aspect('equal')
ax_trail.set_title('Large particle trail', fontsize=11)
ax_trail.set_xlabel('x (nm)'); ax_trail.set_ylabel('y (nm)')
trail_line2, = ax_trail.plot([0], [0], 'r-', linewidth=1, alpha=0.8)
trail_start, = ax_trail.plot(0, 0, 'g*', markersize=12, label='Start')
trail_cur,   = ax_trail.plot(0, 0, 'r*', markersize=12, label='Current')
ax_trail.legend(fontsize=9)

ax_c   = plt.axes([0.15, 0.13, 0.35, 0.03])
ax_kn  = plt.axes([0.15, 0.08, 0.35, 0.03])
ax_btn = plt.axes([0.60, 0.08, 0.12, 0.06])
ax_pau = plt.axes([0.75, 0.08, 0.12, 0.06])

sl_c  = Slider(ax_c,  'Restitution C', 0.1, 1.0, valinit=C_restitution, valstep=0.05)
sl_kn = Slider(ax_kn, 'Kn (redirect)', 5,   50,  valinit=Kn,            valstep=1)
btn_reset = Button(ax_btn, 'Reset', color='#f0f0f0', hovercolor='#ddd')
btn_pause = Button(ax_pau, 'Pause', color='#f0f0f0', hovercolor='#ddd')

paused = [False]

def reset(_):
    global pos_s, vel_s, pos_L, vel_L, steps_since_redirect, trail_L, time_ps
    pos_s, vel_s, pos_L, vel_L = init_particles()
    steps_since_redirect = rng.integers(0, Kn, N_SMALL)
    trail_L = [pos_L.copy()]
    time_ps = 0.0

def toggle_pause(_):
    paused[0] = not paused[0]
    btn_pause.label.set_text('Resume' if paused[0] else 'Pause')

btn_reset.on_clicked(reset)
btn_pause.on_clicked(toggle_pause)

STEPS_PER_FRAME = 3

def animate(frame):
    global pos_s, vel_s, pos_L, vel_L, steps_since_redirect, trail_L, time_ps

    if paused[0]:
        return

    C  = sl_c.val
    kn = int(sl_kn.val)

    for _ in range(STEPS_PER_FRAME):
        pos_s, vel_s, pos_L, vel_L, steps_since_redirect = step(
            pos_s, vel_s, pos_L, vel_L, steps_since_redirect, C)
        trail_L.append(pos_L.copy())

    sc_small.set_offsets(pos_s)
    large_circle.center = pos_L
    cur_marker.set_data([pos_L[0]], [pos_L[1]])

    trail_arr = np.array(trail_L)
    trail_line.set_data(trail_arr[:, 0], trail_arr[:, 1])

    trail_line2.set_data(trail_arr[:, 0], trail_arr[:, 1])
    trail_cur.set_data([pos_L[0]], [pos_L[1]])
    ax_trail.relim(); ax_trail.autoscale_view()

    ax_sim.set_title(f'Brownian motion simulation: t = {time_ps:.0f} ps',
                     fontsize=11, fontweight='bold')

ani = FuncAnimation(fig, animate, interval=30, cache_frame_data=False)

plt.suptitle('BPhO Task #2', fontsize=13, fontweight='bold')

plt.show()