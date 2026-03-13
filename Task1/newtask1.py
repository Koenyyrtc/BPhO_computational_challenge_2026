import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

fig, ax = plt.subplots(figsize=(8, 7))
plt.subplots_adjust(bottom=0.25)

ax_n   = plt.axes([0.15, 0.15, 0.65, 0.03])
ax_s   = plt.axes([0.15, 0.10, 0.65, 0.03])
ax_w   = plt.axes([0.15, 0.05, 0.65, 0.03])
ax_btn = plt.axes([0.40, 0.00, 0.20, 0.04])

slider_n   = Slider(ax_n, 'N steps',  100,  5000, valinit=2000, valstep=100)
slider_s   = Slider(ax_s, 'Step size', 1,   10,   valinit=1,    valstep=1)
slider_w   = Slider(ax_w, 'Walks',     5,   100,  valinit=50,   valstep=5)
btn        = Button(ax_btn, 'New walks', color='#f0f0f0', hovercolor='#ddd')

drawn = []

def draw_walks(N, step_size, num_walks):
    global drawn
    for obj in drawn:
        obj.remove()
    drawn = []

    colors = plt.cm.hsv(np.linspace(0, 1, num_walks, endpoint=False))

    for i in range(num_walks):
        angles = np.random.uniform(0, 2 * np.pi, N)
        x = np.concatenate([[0], np.cumsum(step_size * np.cos(angles))])
        y = np.concatenate([[0], np.cumsum(step_size * np.sin(angles))])
        l, = ax.plot(x, y, color=colors[i], linewidth=0.5, alpha=0.8)
        drawn.append(l)

    ax.set_title(f'Random walk.  Step size = {step_size}', fontsize=11)
    ax.set_xlabel('x'); ax.set_ylabel('y')
    ax.set_aspect('equal', adjustable='datalim')
    fig.canvas.draw_idle()

def update(_):
    draw_walks(int(slider_n.val), int(slider_s.val), int(slider_w.val))

slider_n.on_changed(update)
slider_s.on_changed(update)
slider_w.on_changed(update)
btn.on_clicked(update)

plt.suptitle('BPhO Task #1', fontsize=12, fontweight='bold')
draw_walks(int(slider_n.val), int(slider_s.val), int(slider_w.val))
plt.show()