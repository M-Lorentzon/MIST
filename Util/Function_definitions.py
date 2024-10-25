
import numpy as np
import lmfit as lmfit





def Gaussian(x, Ampl, centre, sigma):

    y = Ampl * 1/(np.sqrt(2*np.pi)) * np.exp( -0.5 * ((x - centre) / sigma)**2 )
    return y

