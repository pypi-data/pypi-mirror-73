
import  __future__

import numpy as np

class Kpoints(object):

    """
    Aim to produce the kmesh
    """
    #auto_density  = False
    
    __value = 0
 
    def __init__(self, *args, **kwargs):

        self.__kpoints = ('auto', 12)
        self.__model   = None 
        self.__band_insert = 30
        self.__emass_insert = 50
        self.__comment = ''
        self.__value = 0

    @property 
    def model(self):
        return self.__model 

    @property 
    def comment(self):
        if len(self.__comment):
            return self.__comment
        else:
            return self.__model
    @comment.setter
    def comment(self, value=None):
        self.__comment = value 

    @property 
    def num(self):
        return self.__value
    @num.setter
    def num(self, n=0):
        self.__value = n 

    @property
    def band_insert(self):
        return self.__band_insert
    @band_insert.setter
    def band_insert(self, value=None):
        if isinstance(value,int):
            self.__band_insert = value 

    @property
    def emass_insert(self):
        return self.__emass_insert
    @emass_insert.setter
    def emass_insert(self, value=None):
        if isinstance(value,int):
            self.__emass_insert = value 

    @property 
    def kpath(self):
        return self.__band_kpath
    @kpath.setter
    def kpath(self,value=None):
        if isinstance(value,dict):
            self.__band_kpath = value
        if isinstance(value,tuple):
            band_kpath = {}
            for line in value:
                if isinstance(line,int):
                    self.__band_insert = line

                elif isinstance(line,str):
                    try:
                        tmp = line.split(':')
                        band_kpath[tmp[0]] = tmp[1]
                    except: 
                        pass
            if len(band_kpath.keys()) > 0:
                self.__band_kpath = band_kpath

    @property 
    def kpoints(self):
        return self.__kpoints  

    @kpoints.setter 
    def kpoints(self,value=None):

        if isinstance(value,float):         # kspacing % 
            self.__model   = 'kspacing'
            self.__kpoints = value 

        elif isinstance(value,str):
            self.__model = 'string'
            self.__kpoints = value
            self.__comment  = 'kmesh' 

        elif isinstance(value,int) and value >= 1000:
            self.auto_density = True 
            self.density = value 

        elif isinstance(value,tuple):     

            # split %
            if len(value) == 2:
                model,kpoint = value 

            elif len(value) == 3:
                self.__comment,model,kpoint = value 

            elif len(value) == 4:
                self.__comment,self.__value,model,kpoint = value

            # set kpoints base on model %
            if model.lower()[0] == 'a':  # Auto % 
                self.__model = 'Auto'
                self.__kpoints = int(kpoint) 

            elif model.lower()[0] in ['m', 'g']: # Gamma and Monk % 
                if model.lower()[0] == 'm':
                    self.__model = 'Monkhorst-pack' 
                elif model.lower()[0] == 'g':
                    self.__model = 'Gamma'

                if isinstance(kpoint,str):
                    kpoint = kpoint.split()

                try:
                    if len(kpoint) == 3:
                        self.__kpoints = np.array([kpoint, [0,0,0]],dtype=int)
                    elif len(kpoint) == 6:
                        self.__kpoints = np.array(kpoint,dtype=int).reshape(2,3)
                    else:
                        raise
                except:
                    raise ('Error Monk/Gamma type kpoint')

            elif model.lower()[0] == 'l': # Line-model % 
                self.__model = 'Line Model'
                if isinstance(kpoint,str):
                    self.__kpoints = kpoint
                if isinstance(kpoint,list):
                    self.__kpoints = '\n'.join(kpoint)

            elif model.lower()[0] == 'r': # Line-model % 
                self.__model = 'Reciprocal'
                if isinstance(kpoint,str):
                    self.__kpoints = kpoint
                if isinstance(kpoint,list):
                    self.__kpoints = kpoint
                if isinstance(kpoint,np.ndarray):
                    self.__kpoints = ""
                    if len(kpoint.shape) == 2 and kpoint.shape[1] == 4:
                        for k in kpoint:
                            self.__kpoints+="{0[0]:20.14f}{0[1]:20.14f}{0[2]:20.14f}{0[3]:14}\n".format(k)
                    elif len(kpoint.shape) == 2 and kpoint.shape[1] == 3:
                        kpoint = np.column_stack((kpoint,np.ones(len(kpoint))))
                        for k in kpoint:
                            self.__kpoints+="{0[0]:20.14f}{0[1]:20.14f}{0[2]:20.14f}{0[3]:14}\n".format(k)


            elif model.lower()[0] == 'c': # Cartesian % 
                self.__model = 'Cartesian'
                if isinstance(kpoint,list):
                    self.__kpoints = np.array(kpoint).reshape(len(kpoint)/3, 3)

                elif isinstance(kpoint,str) and len(kpoint.split()) % 3 == 0:
                    self.__kpoints = np.float64(kpoint.split()).reshape(len(kpoint)/3,3)
                else:
                    raise('Error cartesian coordinations')

        elif isinstance(value,list):
            self.__kpoints = value 
 
