import numpy as np

class WCApotential():

    def __init__(self,epsilon=1):
        
        self.epsilon = epsilon

        return

    def V_WCA(self,r):
        
        a = 4*self.epsilon*(r**(-12)-r**(-6))+self.epsilon

        return np.where(r<2**(1./6.),a,0*a)
    
    def _limited_domain_WCA_deriv(self,r):

        # this function is only valid when r <= 1 !!!
        
        return -24*self.epsilon*(2*r**(-13)-r**(-7))
    
    def V_WCA_prime(self,r):

        a = self._limited_domain_WCA_deriv(r)

        return np.where(r<=2**(1./6.),a,a*0)
        
