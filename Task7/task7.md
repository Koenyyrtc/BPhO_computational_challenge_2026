# Particle in a Box

A particle of mass *m* is confined to a 1D box of width *a*, with infinite potential walls.

## The Model

$$V(x) = \begin{cases} \infty & x \le 0,\; x \ge a \\ 0 & 0 < x < a \end{cases}$$

The wavefunction must be zero at the walls, giving standing-wave solutions.

## Schrodinger Equation

$$-\frac{\hbar^2}{2m}\frac{\partial^2\psi}{\partial x^2} + V\psi = i\hbar\frac{\partial\psi}{\partial t}$$

Inside the box (*V* = 0), the time-independent spatial solution is:

$$\psi_n(x) = \sqrt{\frac{2}{a}}\sin\!\left(\frac{n\pi x}{a}\right), \quad n = 1, 2, 3, \ldots$$

The full wavefunction includes the time phase factor:

$$\psi_n(x,t) = \psi_n(x)\,e^{-iE_n t/\hbar}$$

