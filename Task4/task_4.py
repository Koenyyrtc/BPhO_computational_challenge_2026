import math
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.widgets import Slider
import matplotlib.gridspec as gridspec
import random

c = 3e8
e = 1.6021766208
h = 6.626
h_eV = 4.135
m = 9.11
W = {"Ag": 4.3, "Al": 4.3, "Au": 5.1, "Cu": 4.7, "Sn": 4.4, "Pb": 4.3, "W": 4.5, "Ni": 4.6, "Na": 2.4}

def voltage(f, material):
    return h/e*f-W[material]

def f_cutoff(material):
    return W[material]/h_eV

material = input("Enter the material.")


class AnimState:
    def __init__(self):
        self.running    = True
        self.frame      = 0
        self.total      = 40
        self.rings_data = []
        self.trigger_V  = None

anim_state = AnimState()

fig = plt.figure(figsize=(16, 9), facecolor="#0a0a0a")
fig.suptitle("Photoelectric Effect Simulator", color="#00ff88",
             fontsize=18, fontweight="bold", fontfamily="monospace", y=0.97)

gs = gridspec.GridSpec(
    1, 3,
    figure=fig,
    left=0.06, right=0.97,
    top=0.92, bottom=0.10,
    hspace=0.45, wspace=0.38
)

ax_graph = fig.add_subplot(gs[:, 2])
ax_sim = fig.add_subplot(gs[:, :2])
ax_light = fig.add_subplot(gs[:, :2])


for ax in [ax_graph, ax_light]:
    ax.set_facecolor("#050505")
    for spine in ax.spines.values():
        spine.set_color("#1a3a1a")
ax_light.set_facecolor("none")
for spine in ax_light.spines.values():
        spine.set_color("#1a3a1a")

# graph

ax_graph.set_xlim(0, 2)
ax_graph.set_ylim(math.floor(voltage(0, material)), math.ceil(voltage(2, material)))
ax_graph.set_aspect(2/(math.ceil(voltage(2, material))-math.floor(voltage(0, material))))
ax_graph.set_title("Photoelectron Stopping Voltage vs Frequency", color="#00cc66",
                     fontfamily="monospace", fontsize=11)
ax_graph.tick_params(colors="#336633")
ax_graph.set_xlabel("Frequency (10^15Hz)", color="#336633", fontfamily="monospace")
ax_graph.set_ylabel("Stopping Voltage (V)", color="#336633", fontfamily="monospace")

frequency = np.linspace(0, 2, num=1000)
vertical = np.linspace(-20, 20, num=1000)
f_cutoff_values = np.linspace(f_cutoff(material), f_cutoff(material)+0.001, num=1000)

ax_graph.plot(frequency, voltage(frequency, material), label=f"W={W[material]}eV", color="blue")
ax_graph.plot(f_cutoff_values, vertical, ":", label="f_cutoff", color="#FFFFFF")

ax_graph.legend()
ax_graph.grid(True)

# simulation

ax_sim.set_xlim(0, 20)
ax_sim.set_ylim(0, 10)
ax_sim.set_aspect("equal")
ax_sim.set_title("Simulation", color="#00cc66",
                   fontfamily="monospace", fontsize=10)
ax_sim.axis("off")

tube_rect = patches.FancyBboxPatch((2.0, 2.0), 13.0, 5.0,
    boxstyle="round,pad=0.05", linewidth=1.5,
    edgecolor="#225522", facecolor="#000000", zorder = 2)
ax_sim.add_patch(tube_rect)

wire_rect = patches.FancyBboxPatch((1.0, 0.7), 15.0, 3.8,
    boxstyle="round,pad=0.05", linewidth=1.5,
    edgecolor="#225522", facecolor="#000000", zorder = 1)
ax_sim.add_patch(wire_rect)

battery_rect = patches.FancyBboxPatch((6.5, 0.1), 4.0, 1.4,
    boxstyle="round,pad=0.05", linewidth=1.5,
    edgecolor="#225522", facecolor="#000000", zorder = 2)
ax_sim.add_patch(battery_rect)

lamp_rect = patches.FancyBboxPatch((8.5, 7.3), 10.0, 2.6,
    boxstyle="round,pad=0.05", linewidth=1.5,
    edgecolor="#225522", facecolor="#000000", zorder = 100)
ax_sim.add_patch(lamp_rect)

ax_sim.text(18.0, 6.9, "Lamp", color="#00cc66",
             ha="center", fontfamily="monospace", zorder = 1000)
ax_sim.text(8.5, 0.6, "Battery", color="#00cc66",
             ha="center", fontfamily="monospace", zorder = 1000)

slider_f_cutoff = 11.9 + ((c/(f_cutoff(material)*1e6)-100)/750) * 5.1
ax_sim.plot([slider_f_cutoff, slider_f_cutoff], [8.2, 8.4], color="#00cc66", linewidth=1.5, zorder=1000)
ax_sim.plot([13.9, 13.9], [8.2, 8.6], color="#00cc66", linewidth=1.5, zorder=1000)

ax_sim.text(slider_f_cutoff, 8.5, "f_cutoff", color="#00cc66",
             ha="center", fontfamily="monospace", zorder = 1000, fontsize = 6)
ax_sim.text(13.7, 8.7, "UV/", color="#cd28ff",
             ha="center", fontfamily="monospace", zorder = 1000, fontsize = 6)
ax_sim.text(14.7, 8.7, "Visible light", color="#ffffff",
             ha="center", fontfamily="monospace", zorder = 1000, fontsize = 6)


# intensity

ax_intensity_slider = fig.add_axes([0.4, 0.73, 0.15, 0.025])
ax_intensity_slider.set_facecolor("#0a0a0a")
intensity_slider = Slider(ax_intensity_slider, "Intensity (%)", 0.0, 100.0,
                valinit=100.0, color="#00aa55", zorder = 10)
intensity_slider.label.set_color("#00cc66")
intensity_slider.label.set_fontfamily("monospace")
intensity_slider.valtext.set_color("#00cc66")
intensity_slider.valtext.set_fontfamily("monospace")


def update_light():
    ax_light.cla()
    ax_light.set_xlim(0, 20)
    ax_light.set_ylim(0, 10)
    ax_light.set_aspect("equal")
    ax_light.axis("off")
    for i in range(laser_num + 1):
        ax_light.plot([2.0, 8.5], [3.2 + 2.6 * i/laser_num, 7.3 + 2.6 * i/laser_num], color="#ffffff", linewidth=1.5, zorder=1000, alpha=intensity)

def intensity_update(val):
    global intensity
    intensity = val/100
    update_light()

intensity_slider.on_changed(intensity_update)

# wavelength

ax_wavelength_slider = fig.add_axes([0.4, 0.67, 0.15, 0.025])
ax_wavelength_slider.set_facecolor("#0a0a0a")
wavelength_slider = Slider(ax_wavelength_slider, "Wavelength (nm)", 100, 850,
                valinit=100, color="#00aa55", zorder = 10)
wavelength_slider.label.set_color("#00cc66")
wavelength_slider.label.set_fontfamily("monospace")
wavelength_slider.valtext.set_color("#00cc66")
wavelength_slider.valtext.set_fontfamily("monospace")

def wavelength_update(val):
    global frequency
    global max_velocity
    frequency = c / (val * 1e-9)
    try:
        max_velocity = math.sqrt(3.2*(h_eV*(frequency*1e-15)-W[material])/m)
    except:
        pass

wavelength_slider.on_changed(wavelength_update)

# voltage

ax_voltage_slider = fig.add_axes([0.23, 0.2, 0.15, 0.025])
ax_voltage_slider.set_facecolor("#0a0a0a")
voltage_slider = Slider(ax_voltage_slider, "Voltage (V)", -8.0, 8.0,
                valinit=1.0, color="#00aa55", zorder = 10)
voltage_slider.label.set_color("#00cc66")
voltage_slider.label.set_fontfamily("monospace")
voltage_slider.valtext.set_color("#00ff88")
voltage_slider.valtext.set_fontfamily("monospace")

def voltage_update(val):
    global acceleration
    acceleration = e*val/(m*d)

voltage_slider.on_changed(voltage_update)

# animation

class electron():
    def __init__(self, velocity):
        self.x = 2.0
        self.y = random.uniform(3.0, 6.0)
        self.velocity = velocity
        self.terminated = False

ax_light.set_xlim(0, 20)
ax_light.set_ylim(0, 10)
ax_light.set_aspect("equal")
ax_light.axis("off")

laser_num = 5
intensity = 1
for i in range(laser_num + 1):
    ax_light.plot([2.0, 8.5], [3.2 + 2.6 * i/laser_num, 7.3 + 2.6 * i/laser_num], color="#ffffff", linewidth=1.5, zorder=1000, alpha=intensity)

electron_num = 0
electrons = []
electron_data = []
frequency = c / 100e-9 
f_threshold = f_cutoff(material)*1e15
max_electron_rate = 0.3 # 0 < max_electron_rate < 1
try:
    max_velocity = math.sqrt(3.2*(h_eV*(frequency*1e-15)-W[material])/m)
except:
    pass
voltage_value = 1.0
d = 5.0 # I just put a reasonable number here
acceleration = e/(m*d)

def animate(frame):
    if not anim_state.running:
        return

    global electron_num
    if frequency > f_threshold:
        if random.random() <= max_electron_rate * intensity:
            temp, = ax_sim.plot([], [], "o", color="#ffff66", markersize=8, zorder=10, markeredgecolor="none", markeredgewidth=0.5)
            electrons.append(temp)
            temp = electron(random.uniform(0.0, max_velocity))
            electron_data.append(temp)
            electron_num += 1
    for num in range(electron_num):
        electron_data[num].velocity += acceleration
        electron_data[num].x += electron_data[num].velocity
        electrons[num].set_data([electron_data[num].x], [electron_data[num].y])
        if electron_data[num].x >= 15.0 or electron_data[num].x < 2.0:
            electrons[num].set_alpha(0)
    
    anim_state.frame += 1

ani = animation.FuncAnimation(fig, animate, interval=30, blit=False)

plt.show()
