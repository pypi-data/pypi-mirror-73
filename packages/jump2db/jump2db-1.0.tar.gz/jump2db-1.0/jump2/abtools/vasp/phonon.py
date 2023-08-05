
from setvasp import SetVasp 

class Phonon(object):

    def __init__(self, dfpt=True, symmetry=True, number=151, connect=True,
			     force='write', velocity=True, eigenvectors=True,
			     *args, **kwargs):
	
       
        self.__dfpt = dfpt 

        self.__script ="ATOM_NAME = {elements}\
                 \nDIM = {super}\
                 \nband= {band}\
                 \nBAND_LABELS = {symbols}\
                 \nBAND_POINTS = {number}\
                 \nBAND_CONNECTION = {connect}\
                 \nFC_SYMMETRY = {symmetry}\
                 \nFORCE_CONSTANTS = {force}\
                 \nGROUP_VELOCITY = {velocity}\
                 \nEIGENVECTORS = {eigenvectors}\n"
        if kwargs: 
            for key, value in kwargs.iteritems():
               self.__script=+ "\n{key}={value}".format(key=key,value=value)

    def DFPT_phonon(self, stdout=None, name='POSCAR-unitcell',spc=None, *args, **kwargs):
        
        """
        spc:: the supercell NxM*L, default, automatically produce supercell with vectors
              along certasian coordination > 10 angstrom. 
        """
        import os
        from os.path import join 
        from jump2.structure import read 

        if spc in None:
            pass 
	
        cmd ="phonopy -d --dim='{0}' -c {1}/POSCAR-unitcell".format(spc, stdout) 
        self.func.structure = read(join(stdout,'SPOSCAR'))		 
        self.func.nsw = 1
        self.func.ibrion = 8

        return self.func

    def finite_displacement(self, stdout=None, name='CONTCAR'):
        """
        """
        pass	

    def phonon_calc(self, func=None, stdout=None):
	
        if isinstance(func, SetVasp):
            if self.__dfpt is True:
                self.DFPT_phonon(stdout)
            else:
                self.__finite_displacement(self, stdout, name='POSCAR')
		
        else:
            raise IOError ('only support vasp...')

    def write_phinput(self):
        pass 		

    def extract_phonon(self):
        pass 
