# Quantum Cryptography — Detector Mismatch Calculator

Alice and Bob each measure entangled photons with polarisation detectors at angles θ and φ. The probability of their results matching or mismatching differs depending on whether the photons are classically correlated or quantum-entangled — and whether an eavesdropper (Eve) is present.

---

## Setup

Two detectors measure entangled photon pairs:

- **Alice** measures at angle **θ**
- **Bob** measures at angle **φ**
- Each detector gives outcome X (along its axis) or Y (perpendicular)

---

## Classical Scenario

Photons carry hidden polarisation set at Alice's angle. Bob's detector then resolves it:

$$P(\text{match}) = \cos^2\theta\cos^2\phi + \sin^2\theta\sin^2\phi$$

$$P(\text{mismatch}) = 1 - \cos^2\theta\cos^2\phi - \sin^2\theta\sin^2\phi$$

---

## Quantum Scenario (entangled)

Measuring Alice's photon instantly collapses the joint state. Bob's photon is now polarised along Alice's axis, so only the **relative angle** matters:

$$P(\text{match}) = \cos^2(\phi - \theta)$$

$$\boxed{P(\text{mismatch}) = \sin^2(\phi - \theta)}$$

The quantum result depends only on the *difference* φ − θ, not on θ and φ individually. This is a fundamentally non-classical correlation.

---

## Eve Intercepts (Special Feature)

Eve measures at angle **ε**, collapsing the entangled state and re-emitting a new photon toward Bob. This breaks entanglement — Bob no longer shares a state with Alice.

The combined match probability becomes:

$$P(\text{match}) = P_{AE} \cdot P_{EB} + (1 - P_{AE})(1 - P_{EB})$$

where $P_{AE} = \cos^2(\varepsilon - \theta)$ and $P_{EB} = \cos^2(\phi - \varepsilon)$.

**Eve raises the mismatch rate** above the quantum prediction. Alice and Bob can detect her by comparing a sample of their results over a classical channel — if the error rate is too high, someone has been listening.

---

## Key Difference at a Glance

| | Match probability |
|---|---|
| Classical | $\cos^2\theta\cos^2\phi + \sin^2\theta\sin^2\phi$ |
| Quantum | $\cos^2(\phi - \theta)$ |
| Quantum + Eve | $P_{AE}\cdot P_{EB} + (1-P_{AE})(1-P_{EB})$ |

At θ = 0°, φ = 45°: classical gives P(mismatch) = 0.5, quantum gives P(mismatch) = 0.5 too — but at other angles they diverge, and Eve always pushes mismatch *up*.
