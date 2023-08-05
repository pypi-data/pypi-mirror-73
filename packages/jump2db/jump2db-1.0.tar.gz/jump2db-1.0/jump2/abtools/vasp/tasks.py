from collections import UserDict
class VaspIncar(UserDict):
   
    def __init__(self,name='',dict=None,finish=False):
        UserDict.__init__(self,dict)
        self.__name = name
        self.finish = finish

    @property
    def name(self):
        return self.__name

    def downdate(self,dict):
        for key in dict:
            if key not in self.data:
                self.data[key] = dict[key]

__Task__ = ['dos','band','partchg','fatband','optics','emass', \
            'carrier','hse_gap','gw_gap','dielectric','md']
__xc__ = ['soc','hse','gw']

class VaspTask(object):

    def __init__(self, *args, **kwargs):
        self.__optimize = None
        self.__scf = None
        self.__nonscf = None
        self.__properties = None
        self.__diyflow = None
        self.__xc = None

    @classmethod
    def minitask(cls,task):
        from jump2.abtools.diyflow import get_diy_moudles
        taskdict = {}
        # optimization % 
        opt=''
        for key in ['ions', 'shape', 'volume']:
            if key in task:
                opt += key[0]
        if len(opt):
            taskdict['opt'] = opt
 
        # scf %
        if 'scf' in task: 
            taskdict['scf'] = ''

        # nonscf %
        nonscf = []
        for key in __Task__:
            if key in task:
                nonscf.append(key)
        if len(nonscf):
            taskdict['nonscf'] = nonscf

        # xc_func %
        xc = []
        for key in __xc__:
            if key in task:
                xc.append(key)
        if len(xc):
            taskdict['xc'] = xc

        # add diy-task if it exists in floder ~/abtools/diyflow
        diyflow = []
        for moudle in get_diy_moudles():
            if moudle in task:
                diyflow.append(moudle)
        if len(diyflow):
            taskdict['diyflow'] = diyflow
        
        return taskdict
        
    @classmethod
    def fulltask(cls,task,rootdir):
        import json
        from os.path import dirname, join, relpath 

        submit_dir = dirname(dirname(rootdir))
        try:
            with open(join(submit_dir,'.incar')) as f:
                default = json.load(f)
        except:   
            with open(join(os.environ['HOME'], '.jump2','env','incar.json')) as f:
                default = json.load(f)

        vt = VaspTask()
        # default %
        if 'default' in default:
            vt.__default = VaspIncar('default',default['default'])
        else:
            raise ValueError("Default parameters is necessary in incar !")

        # optimization % 
        if 'opt' in task:
            isif={'i':2, 'isv':3, 'is':4,'s':5, 'sv':6, 'v':7, 'iv':-1} 
            params = {'isif':isif[task['opt']], 'nsw':50, 'ibrion':2}
            if 'optimize' in default:
                params.update(default['optimize'])
            vt.__optimize = VaspIncar('optimize',params)
 
        # scf % 
        if 'scf' in task:
            params = {'isif':2, 'nsw':0, 'ibrion':-1}
            if 'scf' in default:
                params.update(default['scf'])
            vt.__scf = VaspIncar('scf',params)

        # xc_func %
        if 'xc' in task:
            xc = {}
            for t in task['xc']:
                if t not in __xc__: continue
                elif t in default:
                    xc[t] = VaspIncar(t,default[t])
                else:
                    xc[t] = VaspIncar(t)

            vt.__xc = VaspIncar('xcfunc',xc,finish=True)


        # property %
        if 'nonscf' in task and len(task['nonscf']):
            nonscf = {}

            if 'xc' in task and 'optics' not in task['xc']:
                nonscf['optics'] = VaspIncar('optics',default['optics'],finish=True)
         
            if 'band' not in task['nonscf']:
                nonscf['band'] = VaspIncar('band',default['band'],finish=True)
         
            for t in task['nonscf']:
                if t not in __Task__: continue
                elif t in default:
                    nonscf[t] = VaspIncar(t,default[t])
                else:
                    nonscf[t] = VaspIncar(t)

            vt.__properties = VaspIncar('nonscf',nonscf) 

        # magnetic %
        try:
            with open(join(submit_dir,'.magnetic')) as f:
                mag_dict = json.load(f)
            for mag,value in mag_dict: 
                path = mag.split()[0]
                if path == relpath(rootdir,submit_dir) and len(value):
                    vt.__magnetic == VaspIncar('magnetic',{'magmom':value}) 
                    break
        except:   
            pass

        # save diy-task into params['diy'] if it exists in floder ~/abtools/diyflow
        if 'diyflow' in task and len(task['diyflow']):
            vt.__diyflow = VaspIncar('diyflow')
            for t in task['diyflow']:
                vt.__diyflow[t] = VaspIncar(t)

        return vt

    @property
    def optimize(self):
        return self.__optimize

    @optimize.setter
    def optimize(self,value=None):
        self.__optimize = value 

    @property
    def scf(self):
        return self.__scf

    @scf.setter 
    def scf(self, value=True):
        self.__scf = value 

    @property
    def nonscf(self):
        return self.__properties 

    @nonscf.setter
    def nonscf(self, value=False):
        self.__properties = value 

    @property
    def diyflow(self):
        return self.__diyflow 

    @diyflow.setter
    def diyflow(self, value=False):
        self.__diyflow = value 

    @property
    def default(self):
        return self.__default

    @property
    def xc_func(self):
        return self.__xc

    @property
    def magnetic(self):
        if not hasattr(self,'__magnetic'):
            self.__magnetic == VaspIncar('magnetic',{'magmom':'1*1000'}) 
        return self.__magnetic

    def set_energy(self,energy):    
        try:
            energy = float(energy)    # energy % 
            self.default['ediff'] = energy 
        except:
            pass

    def set_force(self,force):    
        try:
            force = float(force)    # force % 
            if force < 0.01: 
                if self.default['ediff'] >= 1E-5:
                    self.default['ediffg'] = -0.01
                else:
                    self.default['ediffg'] = -force
        except:
            pass



