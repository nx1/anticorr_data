# binsep.py
# Binary seperation calculator
import numpy as np

M_SOL = 1.99E30
R_SOL = 6.96E8
G     = 6.67E-11
PI    = np.pi
DAY   = 24*60*60

def calc_a(T, M1, M2):
    """Calculate semi-major axis.
    T  : Orbital period in Days
    M1 : Mass of CO in kg
    M2 : Mass of companion in kg
    """
    a = ((T/2*np.pi)**2*G*(M1+M2))**(1/3)
    return a 

def calc_r1(a, M1, M2):
    """Calculate the radius of the roche lobe
       from the Eggleton Formula"""
    q = M1 / M2
    r1 = a * (0.4*(q)**(2/3) / (0.6*q**(2/3) + np.log(1+q**(1/3))))
    return r1

if __name__ == "__main__":
    M1 = 2 * M_SOL
    M2 = 10 * M_SOL
    T  = 64 * DAY
    a  = calc_a(T, M1, M2)
    r1 = calc_r1(a, M1, M2) 
    print(f'a  = {a:.2e} m')
    print(f'r1 = {r1:.2e} m')

    a_scaled = 1
    r1_scaled = r1 / a
    print('scaled so that the binary seperation is 1')
    print(f'r1_scaled = {r1_scaled:.2f}')

    
