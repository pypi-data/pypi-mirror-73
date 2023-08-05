

# 1. write poscar % 
# 2. write potcar % 
# 3. write kpoints % 
# 4. write incar % 
# 5. write vdwkernel % 

from jump2.utils import CommonOperation, CopyFile 

from .potentials import Potentials 
from .incar import Incar 
from .kpoints import Kpoints 
from .vaspio import VaspIO
from .vdw import VDW
import os 
class SetVasp(CommonOperation,Potentials,CopyFile,VaspIO,Incar,Kpoints,VDW):

    def __init__(self):
        Kpoints.__init__(self)
        super().__init__()
        self.__program = None 
        self.__tasks = None 
        self.__xc = None
        self.__status__ = None 
        self.__overwrite = False
        self.__accelerate = True
       
    @property	
    def overwrite(self):
        return self.__overwrite

    @overwrite.setter
    def overwrite(self,value):
        self.__overwrite = value

    @property 
    def program(self):
        return self.__program 

    @program.setter
    def program(self, value=None):
        if isinstance(value,str) and os.path.isfile(value):
            self.__program = value 
        elif isinstance(value, dict):
            self.__program = value
        else:
            raise IOError ('invalid input VASP program')

    @property
    def tasks(self):
        return self.__tasks
	
    @tasks.setter
    def tasks(self,value):
        from .tasks import VaspTask
        if isinstance(value,str):
            self.__tasks = VaspTask().minitask(value)
        elif isinstance(value,VaspTask):
            self.__tasks = value

    @property
    def xc_func(self):
        return self.__xc

    @xc_func.setter
    def xc_func(self,value):
        if not isinstance(self.tasks,dict):
            self.__xc = value

        elif isinstance(value,str) :
            gga = value.lower()
            # compute with default parameters %
            if gga in ['pbe', 'pbesol','91','pe','rp','ps','am']:
                if gga == 'pbe': self.__xc = 'pe'
                elif gga == 'pbesol': self.__xc = 'ps'
                else: self.__xc = gga

            # compute with extre parameters % 
            elif gga in ['soc','gw','hse']:
                 self.__xc = gga
                 if 'xc' in self.__tasks:
                     self.tasks['xc'].append(gga)
                 else:
                     self.tasks['xc'] = [gga]
       	
    @property
    def accelerate(self):
        return self.__accelerate


    @accelerate.setter
    def accelerate(self,value):
        from .tasks import VaspIncar
        if isinstance(value,bool):
            self.__accelerate = value
        elif isinstance(value,dict) or isinstance(value,VaspIncar):
            self.__accelerate = [VaspIncar('accelerate',value)]
        elif isinstance(value,list):
            acc = []
            for v in value:
                if isinstance(v,dict):
                    acc.append(VaspIncar('accelerate',v))
            if len(acc) != 0: 
                self.__accelerate = acc
            else:
                self.__accelerate = True
        else:
            raise ValueError('Invalid input for vasp.accelerate.')

   	
    def set_input(self, structure, stdout, overwrite=True, incar=None, **kwargs):
    
        """
        set INCAR/POSCAR/POTCAR/KPOINTS/additional_files 
        """
        from os.path import exists, join 
        from .tasks import VaspIncar

        if not exists(stdout): 
            overwrite = True 

        if not isinstance(incar,VaspIncar):
            incar = VaspIncar('input',incar)

        incar.update(kwargs)

        if overwrite is True:
            
            # POTCAR: set pseudopotential % 
            incar.update(self.set_potcar(structure.species_of_elements, stdout))  
            
            # KPOINTS: set kmesh % 
            incar.update(self.set_kpoints(structure, stdout, **incar))

            # VDW % 
            incar.update(self.set_vdw(structure.species_of_elements, stdout))

            # Magnetic moment % 
            # incar.update(self.set_magmom(structure,**incar))	

            # LDA+U % 
            # incar.update(self.set_ldau(structure))	

            # POSCAR: set poscar %  		
            self.write_poscar(structure, stdout, name='POSCAR')
    	
            # external file %
            self.set_externalfile(stdout)

            # INCAR: write incar %
            incar = self.set_incar(incar, stdout)    

        return incar

    # is ispin=2 or lsorbit=True % 
    def get_spin(self,incar):
       	 
        # magnetic property % 
        if 'lsorbit' in incar and 't' in str(incar['lsorbit']).lower():
            spin = True
        elif 'ispin' in incar:
            if incar['ispin'] == 1:
                spin = False
            elif incar['ispin'] == 2:
                spin = True
        elif 'ispin' in self.tasks.default: 
            if kwargs['ispin'] == 1:
                spin = False
            elif kwargs['ispin'] == 2:
                spin = True
        else:
            spin = False
        return spin


    # set_external file % 
    def set_externalfile(self, stdout=None):
        
        from os.path import join, exists, abspath 
        
        if not exists(abspath(stdout)): os.makedirs(stdout)

        if isinstance(self.external_files, list):
            for path in self.external_files:
                if not exists(abspath(path)): 
                    raise IOError ("No external file:"+self.external_files)
                else:
                    os.system('cp -r {0}  {1}'.format(path, stdout))	
        
        elif isinstance(self.external_files, str):
            if "vdw_kernel" in self.external_files:
                if not exists(abspath(self.external_files)):
                    raise IOError ("No external file:"+self.external_files)
                else:
                    os.system('cp -r {0}  {1}'.format(self.external_files, stdout))

    # set POTCAR % 
    def set_potcar(self, elements=None, stdout=None, name='POTCAR'):

        """
        Set the POTCAR according to the species of elements in structure.
        
        return dict{'ENMAX':enmax}
        """	
         
        import re, os 
        from os.path import join, exists, abspath 

        pot_dir = None
        div_pot = None
        if isinstance(self.potential,tuple):
            try:
                pot_dir, div_pot = self.potential
            except:
                raise IOError('Please set the pseudopotential by SetVasp.potential')
        elif isinstance(self.potential,str):
            pot_dir = self.potential

        enmax = -1.0
        lines = ''

        for e in elements:
            optional_pots =[i.rstrip() for i in os.popen("ls {0} | grep {1}".format(pot_dir,e)).readlines()]
            if div_pot and e in div_pot and div_pot[e] in optional_pots:
                pot = div_pot[e]
            elif len(optional_pots) > 0:
                for add in ['_3','_2','','_sv','_pv','_d','_s','_h']:
                    if e+add in optional_pots:
                        pot = e+add
                        break
            # read potcar %
            with open(join(pot_dir,pot, name),'r') as f: 
                line = f.readlines()
            lines += ''.join(line)  
            # update enmax %
            for l in line:
                keyword = re.findall(r'ENMAX\s*=\s*\d+\.\d+',l)
                if len(keyword): 
                    default_enmax = float(keyword[0].split()[-1])
                    if default_enmax > enmax:
                        enmax = default_enmax
                    break

        if not exists(abspath(stdout)): os.makedirs(stdout)

        self.write_potcar(lines, stdout)	 

        return {'enmax':enmax}

    def set_kpoints(self, structure=None, stdout=None, **kwargs):
        """
        """

        kpoints = {}
        if self.model == 'kspacing':
            if 'kspacing' in kwargs:
                pass
            else:
                kpoints = {'kspacing':self.kpoints}
        else:
            self.write_kpoints(structure, stdout) 
        
        return kpoints 


    def set_vdw(self, elements=None, stdout=None):
        """
        """
        try:
            vdw = self.__getattribute__('vdw')
        except:
            return {} 

        if vdw in ['B86', 'B88', 'DF2', 'rDF2', 
       		   'rPBE','optPBE', 'rVV10']:
            self.write_kernel(stdout)

        return self.vdw_parameters(elements)

    def set_incar(self, incar, stdout):

        # get enmax %
        if 'enmax' in incar:
            enmax = incar.pop('enmax') 
        else:
            enmax = 0.0

        # update params encut %
        if 'encut' not in incar:
            if self.cutoff >= enmax and self.cutoff > 300:
                incar['encut'] = self.cutoff  
            else:
                incar['encut'] = min(round(self.cutoff*enmax,4),520)	

        # get gga %
        if 'gga' in incar: 
            gga = incar['gga']
        elif hasattr(self,'xc_func'):
            gga = self.xc_func 
        elif 'gga' in self.task.default:
            gga = self.task.default['gga']
        else:
            gga = 'pe'

        # update params xc_func %
        if gga.lower() in ['soc','gw','hse']:
            incar.update(self.tasks.xc_func[gga])
        else:
            incar['gga'] = gga.upper()

        # inherits first if spin calculation %
        if self.get_spin(incar) is True:
            # set lwave and lcharg%
            if 'icharg' in incar and incar['icharg'] == 11:
                if 'lwave' not in incar :
                    incar['lwave'] = False
            elif 'lcharg' not in incar:
                incar['lcharg'] = True

            if 'lwave' not in incar :
                incar['lwave'] = False

        # set magmom %
        try:
            if incar['istart'] == 0 and incar['icharg'] not in [1,11]:
                incar.update(self.tasks.magnetic)
        except:
            pass

        # update default %        
        incar.downdate(self.tasks.default) 

        print(stdout+'\n',incar)
        self.write_incar(incar, stdout)		

        return incar
           
