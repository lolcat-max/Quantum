
# Photon geodesic with affine parameter:

The equation says that a photon’s path in curved spacetime is a geodesic (a “straightest-possible” path) traced using an affine parameter λ, because proper time is not available for light.[^4][^8]

### Symbols and meaning

- $x^{\mu}(\lambda)$: spacetime coordinates of the photon as a function of the affine parameter $\lambda$; the dot or derivative with respect to $\lambda$ gives the tangent four-vector along the path.[^6][^4]
- $\Gamma^{\mu}_{\nu\rho}$: Christoffel symbols (connection) built from the metric; they encode how coordinates curve so that “straight” lines bend in curved spacetime.[^8][^6]
- The equation

$$
\frac{d^{2}x^{\mu}}{d\lambda^{2}}+\Gamma^{\mu}_{\nu\rho}\,\frac{dx^{\nu}}{d\lambda}\,\frac{dx^{\rho}}{d\lambda}=0
$$

states that the tangent vector is parallel-transported along the curve, which defines a geodesic.[^4][^8]

### Why an affine parameter

- For lightlike paths $ds^{2}=0$, so proper time $\tau$ cannot parametrize the curve; any $\lambda$ that is related to another by $\lambda' = a\lambda + b$ keeps the equation’s form and is called an affine parameter.[^6][^4]
- Using a non-affine parameter adds an extra term proportional to the tangent vector on the right-hand side, so the “clean” geodesic form signals an affine choice.[^7][^4]


### Null constraint for photons

- In addition to the geodesic equation, photon worldlines satisfy the null condition

$$
g_{\mu\nu}\,\frac{dx^{\mu}}{d\lambda}\,\frac{dx^{\nu}}{d\lambda}=0,
$$

ensuring the path is lightlike. This distinguishes photon geodesics from massive particle (timelike) geodesics.[^11][^4]

### Physical interpretation

- Defining $k^{\mu}=\frac{dx^{\mu}}{d\lambda}$, the equation becomes $k^{\nu}\nabla_{\nu}k^{\mu}=0$, i.e., the photon wave‑vector is parallel‑transported; changes in its components encode gravitational redshift/blueshift along the path.[^5][^4]

In short, the displayed equation is the geodesic equation for light, written with an affine parameter so that the photon’s null trajectory is described by parallel transport of its tangent vector in curved spacetime.[^8][^4]
<span style="display:none">[^1][^10][^2][^3][^9]</span>

<div align="center">⁂</div>

[^1]: https://robertevanshine.com/assets/notes/Null Geodesics and Affine Parameters.html

[^2]: https://robertevanshine.com/research/notes/Null Geodesics and Affine Parameters.html

[^3]: https://www.physicsforums.com/threads/can-affine-parameters-be-used-to-describe-null-curves-in-gr.691497/

[^4]: https://physics.umd.edu/grt/taj/675e/675eNotes.pdf

[^5]: https://news.ycombinator.com/item?id=19002063

[^6]: https://en.wikipedia.org/wiki/Geodesic

[^7]: https://www.nikhef.nl/~jo/quantum/qm/gw2/Notes.pdf

[^8]: https://www.damtp.cam.ac.uk/user/tong/gr/grhtml/S1.html

[^9]: https://www.physicsforums.com/threads/geodesics-and-affine-parameterisation.891679/

[^10]: https://www.youtube.com/watch?v=Szj5ojYkZzc

[^11]: http://www.ncra.tifr.res.in:8081/~tirth/Teaching/Cosmology-2021/Lectures/lecture-04-web.pdf

