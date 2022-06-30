# ULX UV / X-Ray Model.
# Norman Khan
# This model describes the relative X-ray and UV 
# emission produced by an Accreting Black Hole or
# Neutron Star in a binary star System with a
# companion star of a given spectral type.

# The  model is defined as follows:
# The companion star is modelled as a spherical black body.
# It's flux is given by the Stefan Boltmann Law.

# The radiant emittance is given by:
    # j* = sigma * T**4                 (W m^-2) (W m^-2  Hz^-1) (erg cm^-2 s^-1)
# Where the Stefan Boltmann Constant is given by:
    # sigma = 5.67 x 10^8        W m^-2 K^-4
    # sigma = 5.67 x 10^-5 erg   erg cm^-2 s^-1 K^-4

# The luminosity L is the measure of the total power emitted
# and is given in units of W (J s^-1) (erg s^-1)
# we may multiply the radiant emittance by the surface area of the star
# to obtain the total luminosity of the object.
#   L = j * A

T=100.0         K j=5.67e+13 erg / (cm2 s)   r=1.00e+05 cm   A=1.26e+11 cm2   L=7.12e+24 erg / s
T=5778.0        K j=6.32e+20 erg / (cm2 s)   r=1.00e+05 cm   A=1.26e+11 cm2   L=7.94e+31 erg / s
T=10000.0       K j=5.67e+21 erg / (cm2 s)   r=1.00e+05 cm   A=1.26e+11 cm2   L=7.12e+32 erg / s
T=20000.0       K j=9.07e+22 erg / (cm2 s)   r=1.00e+05 cm   A=1.26e+11 cm2   L=1.14e+34 erg / s
T=50000.0       K j=3.54e+24 erg / (cm2 s)   r=1.00e+05 cm   A=1.26e+11 cm2   L=4.45e+35 erg / s
T=210000.0      K j=1.10e+27 erg / (cm2 s)   r=1.00e+05 cm   A=1.26e+11 cm2   L=1.39e+38 erg / s
T=1000000.0     K j=5.67e+29 erg / (cm2 s)   r=1.00e+05 cm   A=1.26e+11 cm2   L=7.12e+40 erg / s
T=1000000000.0  K j=5.67e+41 erg / (cm2 s)   r=1.00e+05 cm   A=1.26e+11 cm2   L=7.12e+52 erg / s
T=100.0         K j=5.67e+13 erg / (cm2 s)   r=1.00e+06 cm   A=1.26e+13 cm2   L=7.12e+26 erg / s
T=5778.0        K j=6.32e+20 erg / (cm2 s)   r=1.00e+06 cm   A=1.26e+13 cm2   L=7.94e+33 erg / s
T=10000.0       K j=5.67e+21 erg / (cm2 s)   r=1.00e+06 cm   A=1.26e+13 cm2   L=7.12e+34 erg / s
T=20000.0       K j=9.07e+22 erg / (cm2 s)   r=1.00e+06 cm   A=1.26e+13 cm2   L=1.14e+36 erg / s
T=50000.0       K j=3.54e+24 erg / (cm2 s)   r=1.00e+06 cm   A=1.26e+13 cm2   L=4.45e+37 erg / s
T=210000.0      K j=1.10e+27 erg / (cm2 s)   r=1.00e+06 cm   A=1.26e+13 cm2   L=1.39e+40 erg / s
T=1000000.0     K j=5.67e+29 erg / (cm2 s)   r=1.00e+06 cm   A=1.26e+13 cm2   L=7.12e+42 erg / s
T=1000000000.0  K j=5.67e+41 erg / (cm2 s)   r=1.00e+06 cm   A=1.26e+13 cm2   L=7.12e+54 erg / s
T=100.0         K j=5.67e+13 erg / (cm2 s)   r=1.00e+07 cm   A=1.26e+15 cm2   L=7.12e+28 erg / s
T=5778.0        K j=6.32e+20 erg / (cm2 s)   r=1.00e+07 cm   A=1.26e+15 cm2   L=7.94e+35 erg / s
T=10000.0       K j=5.67e+21 erg / (cm2 s)   r=1.00e+07 cm   A=1.26e+15 cm2   L=7.12e+36 erg / s
T=20000.0       K j=9.07e+22 erg / (cm2 s)   r=1.00e+07 cm   A=1.26e+15 cm2   L=1.14e+38 erg / s
T=50000.0       K j=3.54e+24 erg / (cm2 s)   r=1.00e+07 cm   A=1.26e+15 cm2   L=4.45e+39 erg / s
T=210000.0      K j=1.10e+27 erg / (cm2 s)   r=1.00e+07 cm   A=1.26e+15 cm2   L=1.39e+42 erg / s
T=1000000.0     K j=5.67e+29 erg / (cm2 s)   r=1.00e+07 cm   A=1.26e+15 cm2   L=7.12e+44 erg / s
T=1000000000.0  K j=5.67e+41 erg / (cm2 s)   r=1.00e+07 cm   A=1.26e+15 cm2   L=7.12e+56 erg / s
T=100.0         K j=5.67e+13 erg / (cm2 s)   r=3.48e+10 cm   A=1.52e+22 cm2   L=8.62e+35 erg / s
T=5778.0        K j=6.32e+20 erg / (cm2 s)   r=3.48e+10 cm   A=1.52e+22 cm2   L=9.60e+42 erg / s
T=10000.0       K j=5.67e+21 erg / (cm2 s)   r=3.48e+10 cm   A=1.52e+22 cm2   L=8.62e+43 erg / s
T=20000.0       K j=9.07e+22 erg / (cm2 s)   r=3.48e+10 cm   A=1.52e+22 cm2   L=1.38e+45 erg / s
T=50000.0       K j=3.54e+24 erg / (cm2 s)   r=3.48e+10 cm   A=1.52e+22 cm2   L=5.39e+46 erg / s
T=210000.0      K j=1.10e+27 erg / (cm2 s)   r=3.48e+10 cm   A=1.52e+22 cm2   L=1.68e+49 erg / s   WR 102 HOTTEST KNOWN STAR
T=1000000.0     K j=5.67e+29 erg / (cm2 s)   r=3.48e+10 cm   A=1.52e+22 cm2   L=8.62e+51 erg / s
T=1000000000.0  K j=5.67e+41 erg / (cm2 s)   r=3.48e+10 cm   A=1.52e+22 cm2   L=8.62e+63 erg / s
T=100.0         K j=5.67e+13 erg / (cm2 s)   r=6.96e+10 cm   A=6.08e+22 cm2   L=3.45e+36 erg / s
T=5778.0        K j=6.32e+20 erg / (cm2 s)   r=6.96e+10 cm   A=6.08e+22 cm2   L=3.84e+43 erg / s   SUN
T=10000.0       K j=5.67e+21 erg / (cm2 s)   r=6.96e+10 cm   A=6.08e+22 cm2   L=3.45e+44 erg / s   
T=20000.0       K j=9.07e+22 erg / (cm2 s)   r=6.96e+10 cm   A=6.08e+22 cm2   L=5.51e+45 erg / s
T=50000.0       K j=3.54e+24 erg / (cm2 s)   r=6.96e+10 cm   A=6.08e+22 cm2   L=2.15e+47 erg / s
T=210000.0      K j=1.10e+27 erg / (cm2 s)   r=6.96e+10 cm   A=6.08e+22 cm2   L=6.70e+49 erg / s   SUN @ WR TEMP
T=1000000.0     K j=5.67e+29 erg / (cm2 s)   r=6.96e+10 cm   A=6.08e+22 cm2   L=3.45e+52 erg / s
T=1000000000.0  K j=5.67e+41 erg / (cm2 s)   r=6.96e+10 cm   A=6.08e+22 cm2   L=3.45e+64 erg / s
T=100.0         K j=5.67e+13 erg / (cm2 s)   r=1.18e+14 cm   A=1.76e+29 cm2   L=9.96e+42 erg / s
T=5778.0        K j=6.32e+20 erg / (cm2 s)   r=1.18e+14 cm   A=1.76e+29 cm2   L=1.11e+50 erg / s    UY Scuti Radius
T=10000.0       K j=5.67e+21 erg / (cm2 s)   r=1.18e+14 cm   A=1.76e+29 cm2   L=9.96e+50 erg / s
T=20000.0       K j=9.07e+22 erg / (cm2 s)   r=1.18e+14 cm   A=1.76e+29 cm2   L=1.59e+52 erg / s
T=50000.0       K j=3.54e+24 erg / (cm2 s)   r=1.18e+14 cm   A=1.76e+29 cm2   L=6.23e+53 erg / s
T=210000.0      K j=1.10e+27 erg / (cm2 s)   r=1.18e+14 cm   A=1.76e+29 cm2   L=1.94e+56 erg / s   BIGGEST AND HOTTEST STAR EVER
T=1000000.0     K j=5.67e+29 erg / (cm2 s)   r=1.18e+14 cm   A=1.76e+29 cm2   L=9.96e+58 erg / s
T=1000000000.0  K j=5.67e+41 erg / (cm2 s)   r=1.18e+14 cm   A=1.76e+29 cm2   L=9.96e+70 erg / s

The total power irradiated by our own sun at a temperature of 5778 K
and a radius of 6.96e+10 cm is L=3.84e+43. If the sun was as hot as
one of the hottest known stars WR 102 and had the same radius, the
emitted luminosity would be L=6.70e+49 erg / (cm s). The star however
is thought to have a radius of half that of the Sun's which gives a WR 102
a luminosity of L = 1.68e+49, still the same order of magnitude.

The largest known star UY scuti has r=1.18e+14 cm which at 5779 K would give
L=1.11e+50 erg / s and at 210000 K would give  L=1.94e+56 erg / s


ULXs are commonly associated with supergiant companions, but clearly there must
be an another source of emission to account for a luminosity exceeding 1e+39 in
the 0.2 - 10.0 keV range.

We will next consider luminosity contribution from an accretion disc.

In 





