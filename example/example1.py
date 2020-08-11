import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

####
import matplotlib.pyplot as plt
from kmap.library.orbital import Orbital

cubefile = open('pentacene_HOMO.cube').read()  # read cube-file from file
homo     = Orbital(cubefile,        # compute 3D Fourier transform (see Eqs. 6-11)  
                   dk3D=0.15)       # with a desired k-spacing of dkx = dky = dkz = 0.15 1/Angstroem                           

fig, ax = plt.subplots(1,3)         # create empty figure with 3 axes

# plot Figure 3(a): HOMO of pentacene with phi = 30°
homo.get_kmap(E_kin=30,             # compute momentum map for E_kin = 30 eV (Eq. 12)
              phi=30)               # Euler angle phi = 30            
homo.plot(ax[0])                    # plot kmap in axis 0

# plot Figure 3(b): HOMO of pentacene with phi = 0°, theta = -45°
homo.get_kmap(E_kin=30,             # compute momentum map for E_kin = 30 eV (Eq. 12)
              phi=0,                # Euler angle phi = 0   
              theta=-45)            # Euler angle theta = -45                 
homo.plot(ax[1])                    # plot kmap in axis 1

# plot Figure 3(c): HOMO of pentacene with phi = 90°, theta = -45°, psi = 60°
homo.get_kmap(E_kin=30,             # compute momentum map for E_kin = 30 eV (Eq. 12)
              phi=90,               # Euler angle phi = 90   
              theta=-45,            # Euler angle theta = -45  
              psi=60)               # Euler angle psi = 60°               
homo.plot(ax[2])                    # plot kmap in axis 2


plt.tight_layout()
plt.show()                          # show figure