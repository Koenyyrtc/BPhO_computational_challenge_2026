# Particle in a Box

A particle of mass *m* is confined to a 1D box of width *a*, with infinite potential walls.

---

## The Model

$$V(x) = \begin{cases} \infty & x \le 0,\; x \ge a \\ 0 & 0 < x < a \end{cases}$$

The wavefunction must be zero at the walls, giving standing-wave solutions.

---

## Schrodinger Equation

$$-\frac{\hbar^2}{2m}\frac{\partial^2\psi}{\partial x^2} + V\psi = i\hbar\frac{\partial\psi}{\partial t}$$

Inside the box (*V* = 0), the time-independent spatial solution is:

$$\psi_n(x) = \sqrt{\frac{2}{a}}\sin\!\left(\frac{n\pi x}{a}\right), \quad n = 1, 2, 3, \ldots$$

The full wavefunction includes the time phase factor:

$$\psi_n(x,t) = \psi_n(x)\,e^{-iE_n t/\hbar}$$

---

## Quantised Energies

$$E_n = \frac{\hbar^2\pi^2 n^2}{2ma^2}$$

Energy grows as *n²* — the first few levels for an electron in a 0.5 Å box:

| n | Energy (eV) |
|---|------------|
| 1 | 134.3 |
| 2 | 537.1 |
| 3 | 1208.5 |

---

## Probability Density

The probability of finding the particle near *x* is:

$$|\psi_n(x)|^2 = \frac{2}{a}\sin^2\!\left(\frac{n\pi x}{a}\right)$$

This is **time-independent** — only *Re[ψ]* oscillates.

---

## Special Feature - Time Evolution Animation

The script animates **Re[ψ(x,t)]** oscillating at angular frequency ω = E_n/ħ, while **|ψ|²** stays fixed. A slider lets you switch between quantum numbers *n* = 1–5 in real time.
