import math
import matplotlib.pyplot as plt
import numpy as np

e = 1.6021766208
h = 6.626
W = {"Ag": 4.3, "Al": 4.3, "Au": 5.1, "Cu": 4.7, "Sn": 4.4, "Pb": 4.3, "W": 4.5, "Ni": 4.6, "Na": 2.4}

def voltage(f, material):
    return h/e*f-W[material]

def f_cutoff(material):
    return W[material]/h

material = input("Enter the material.")

frequency = np.linspace(0, 2, num=1000)
vertical = np.linspace(-20, 20, num=1000)
f_cutoff_values = np.linspace(f_cutoff(material), f_cutoff(material)+0.001, num=1000)


plt.figure(figsize = (5,5))
plt.xlim(0, 2)
plt.ylim(math.floor(voltage(0, material)), math.ceil(voltage(2, material)))
plt.xlabel("Frequency (10^15Hz)")
plt.ylabel("Stopping Voltage (V)")
plt.title("Photoelectron Stopping Voltage vs Frequency")
plt.plot(frequency, voltage(frequency, material), label=f"W={W[material]}eV", color="blue")
plt.plot(f_cutoff_values, vertical, ":", label="f_cutoff", color="black")

plt.legend()
plt.grid(True)
plt.show()
