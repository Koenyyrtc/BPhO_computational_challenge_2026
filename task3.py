import math
import matplotlib.pyplot as plt
import numpy as np

kB = 1.381e-23
h = 6.626e-34
c = 2.998e8
R = 8.314
pi = math.pi
sigma = 2/15 * (pi**5 * kB**4)/(c**2 * h**3)

def planck(lam, T): # B(lmb, T)
    return (2 * h * c**2)/(lam**5 * (np.exp((h * c)/(lam * kB * T)) - 1))

def irradiance(T): # I = sigma * T**4
    return sigma * T**4

einstein_frequency = {"Au": 0.2855e13, "Cu": 0.5769e13, "Ti": 0.7054e13, "Al": 0.7188e13, "Fe": 0.7893e13, "Si": 1.0832e13, "C": 3.7451e13}

def C(T, element):
    x = (einstein_frequency[element] * h)/(T * kB)
    return 3*R * (x**2 * np.exp(x))/(np.exp(x) - 1)**2

part = int(input("1 for solar irradiance, 2 for heat capacity"))

plt.figure(figsize = (5,5))

if part == 1:
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Solar Irradiance (Wm^-2nm^-1)")
    plt.title("Solar Irradiance vs Wavelength")

    temperatures = [4000, 5000, 6000] # In kelvin
    wavelength = np.linspace(100e-9, 3000e-9, num=1000) # In m
    for T in temperatures:
        plt.plot(wavelength*1e9, planck(wavelength, T)*1e-9/pi, label = f"T = {T}K")

elif part == 2:
    plt.xlabel("Temperature (K)")
    plt.ylabel("Molar Heat Capacity (Jmol^-1K^-1)")
    plt.title("Einstein Model for Solar Molar Heat Capacity")

    elements = ["Au", "Cu", "Ti", "Al", "Fe", "Si", "C"]
    temperature = np.linspace(0, 800, num=1000) # In kelvin
    for element in elements:
        plt.plot(temperature, C(temperature, element), label = element)

plt.legend()
plt.grid(True)
plt.show()
