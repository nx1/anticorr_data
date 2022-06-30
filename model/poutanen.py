#Poutanen 2007
# Equation 38 for T_ph
import numpy as np

THETA = 20 * (np.pi/180)# FULL OPENING ANGLE
ZETA = 1 / np.tan(THETA)    # cot(theta)
BETA = 1
EPSILON_WIND = 0.5 # fraction of radiative energy accelerate the outflow
MASS = 1 

def T_sp(mdot_0):
    return 1.5*MASS**-0.25*mdot_0**-0.5 * (1+0.3*mdot_0**-0.75)

def T_ph(mdot_0):
    """units of keV"""
    return 0.8 * ((ZETA * BETA) / EPSILON_WIND)**0.5 * MASS**-0.25 * mdot_0**0.75 


if __name__ == "__main__":
    print(f'theta = {THETA:.2f} zeta = {ZETA:.2f} beta = {BETA} e_w = {EPSILON_WIND} m = {MASS}')
    for mdot in [1,10,25,100,1000]:
        print(f'mdot = {mdot:<10} T_ph = {T_ph(mdot):7.3f} keV T_sp = {T_sp(mdot):7.3f} keV')
