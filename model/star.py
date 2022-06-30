import numpy as np
from dataclasses import dataclass
import astropy.units as u

SIGMA = 5.67E5 * u.erg * u.cm**-2 * u.second**-1 * u.K**-4
PI    = np.pi
R_SOL = 6.957e+10 * u.cm
BOLTZMANN = 1.38e-28 * u.J * u.K**-1

def j(T):
    """
    j : Radiant Emittance
    """
    return SIGMA * T**4

def A(r):
    """
    A : Sphere area
    """
    return 4* PI * r**2

def A_proj(r):
    """
    A_proj : Projected 2D area
    """
    return PI*r**2

def L(r,T):
    """
    L : Star Luminosity
    """
    return j(T) * A(r)

def F(L, d):
    """
    F : Flux at specified distance
    """
    F = L / A(d())
    F = F.to(u.erg * u.cm**-2 * u.second**-1)
    return F

def temp2keV(T):
    T = T.to(u.K)
    E = BOLTZMANN * T
    E = E.to(u.keV)
    return E


def x0():
    return 1e6 * np.random.random() * u.mpc

def y0():
    return 1e6 * np.random.random() * u.mpc

def z0():
    return 1e6 * np.random.random() * u.mpc

def d():
    return (x0()**2 + y0()**2 + z0()**2)**0.5

if __name__ == "__main__":
    for temp in [100, 5778, 10000, 20000, 50000, 210000, 1e6, 1e9]:
        temp = temp * u.K
        for r in [1*u.km, 10*u.km, 100*u.km, 0.5*R_SOL, R_SOL, 1700*R_SOL]:
            r = r.to(u.cm)
            print(f'T={temp:.2e}   T={temp2keV(temp):.2e}   j={j(temp):.2e}   r={r:.2e}   A={A(r):.2e}   A_proj={A_proj(r):.2e}  L={L(r,temp):.2e}   d={d():.2e}   F={F(L(r,temp), d):.2e}   x0={x0():.2e}   y0={y0():.2e}   z0={z0():.2e}')
