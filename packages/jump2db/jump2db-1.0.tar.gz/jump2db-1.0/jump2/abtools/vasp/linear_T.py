
class LinearPhase(object):

    k = 8.617333262145E10-5 # unit eV/K

    def __init___(self, stdout=None):
        self.stdout = stdout 

    @property
    def free_energy(self,temperture=300):
        """
        omiga: weight;
        temperature: unit K;
        """
        import numpy as np 

        energy = self.energy(temperature)
        x = self.sigma(energy,temperature)
        w = self.weight

	
        R = [] # R = kTln(x_i/w_i)
        for i in range(len(x)):
            R.append(self.k*temperature*np.exp(x[i]/w[i]))
	
        return np.sum(x*(R+energy))
   
     
    def zeta(self,F,T):
       	"""
        function: zeta_i 
        F: array, free energy for each configuration;
        T: given temperture;
        """
        return np.exp(-(F/self.k*T))	
   
    @property 
    def weight(self):
        """
        w_i: the multiplicity of the configuration

        # note: this can be solve by other method?
        """
        import numpy as np

        dat = np.loadtxt('multiplicity.dat',dtype=int)	

        dat = dict(zip(dat.T[0],dat.T[1]))
	
        return dat.values() 

   
    def sigma(self,F,T):
        """
        Get the x_sigma_i for each configuration; 
        """
        Ztot = self.weight * self.zeta(F,T)
	
        return Ztot/sum(Ztot)
	
	    
    def energy(temperature):
        self.get_energy(temperture)

    def __get_energy(temperature):
	
        """
        how to get the phonon contribution and electronic contribution?
        """
        Evib = self.__free_energy__(temperature)
        Eelec= self.__electronic__(temperature)
	
        return Evib + Eelec 
	
    def FreeEnergy(self, U, F_vib, F_elec,T):
        """
        Get the free energy for each configuration
        Note: only consider the phonon and electonic contribution; 
        """

        F = U + F_vib + F_elec

        return F 

    def Phonon_Eenergy(self, T):
        """
        return the phonon energy: T*S_vib;
        how to remove the imingary frequencies?
        how to get the zero-point energy, and phonon enthalpies?
        """
	
        Fvib = Ezpt + Hvib - T*Svib
	
        return Fvib

    def electronic_enetropy(self):
	
        e_entropy = -3*self.k*(sum(dos*((1-fermi)*np.log(1-fermi)+fermi*np.log(fermi))))*de

    def fermi_T(self, T):
	
        fermi = 1.0/(np.exp(E/self.k/T)+1.0)

