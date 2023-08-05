
class Potentials(object):

    def __init__(self, *args, **kwargs):
        
        self.__pot = None  

    @property
    def potential(self):
        return self.__pot 

    @potential.setter
    def potential(self, value=None):
        self.__pot = value  

  # @staticmethod
  # def get_pesudopentials(self, structure, name='POTCAR'):
  #    
  #     # dirpotential is the gobal varibles %  
  #     lines = ''
  #     
  #     global dirpotential

  #     species = structure.elements 
  #    
  #     for e in species:
  #         path = os.path.join(dirpotential, e, name)
  #         with open(path, 'r') as f:
  #             lines += f.readlines()

  #           
