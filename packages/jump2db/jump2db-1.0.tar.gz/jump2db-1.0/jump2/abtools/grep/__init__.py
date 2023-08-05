__all__ = ['Jump2grep','Jump2band','Jump2dos','Jump2optic']
import numpy as np
import re
import os
from .outcar import GrepOutcar
from .band import GrepBand,GrepProcar
from .dos import GrepDos
from .optic import GrepOptic

def get_real_dir():
    from os.path import dirname,realpath,abspath
    return abspath(dirname(realpath(__file__)))

def get_parent_dir():
    from os.path import dirname,realpath,abspath
    return abspath(dirname(dirname(realpath(__file__))))

class Jump2grep(GrepOutcar):
    def __init__(self,stdin):
        self.stdin = os.path.normcase(stdin)

    def grep(self,value):
        func = getattr(self,value)
        return func(self.stdin)

class _fatband(GrepProcar):

    def __init__(self,stdin,kpath=None):
        from os.path import join,exists
        stdin = os.path.normcase(stdin)
        # set kpath part1 %
        if isinstance(kpath,list):
            self.kpath = self.set_kpath(kpath)
        elif isinstance(kpath,tuple):
            self.kpath = [kpath] 
        elif isinstance(kpath,str):
            pass
        else:
            self.kpath = None

        # set single or multi %
        if exists(join(stdin,'OUTCAR')):
            self.stdin = stdin          
        elif exists(join(stdin,'nonscf','fatband')):
            self.stdin = join(stdin,'nonscf','fatband')
            self.scfdir = join(stdin,'scf')
            if exists(join(stdin,'nonscf','fatband','OUTCAR')):
                pass
            else:
                self.banddir = []
                for i in os.listdir(self.stdin):
                    if '-' in i and exists(join(self.stdin,i,'OUTCAR')):
                        self.banddir.append(i)
                if len(self.banddir) == 0:  
                    raise IOError("Band calculation files not exists!")
        else:
            raise IOError("Band calculation files not exists!")

    def get_procar(self):
        # single %
        if hasattr(self,'banddir'):
            procar = []
            for k in self.kpath:
                for i in range(len(k)-1):
                    dirname = k[i].lstrip('\\')+'-'+k[i+1].lstrip('\\')
                    procar.append(self._get_procar(os.path.join(self.stdin,dirname)))
            shape = procar[0].shape
            procar = np.stack(procar,axis=1).reshape(shape[0],-1,shape[2],shape[3],shape[4])
            return procar
        # multi %
        else:
            return self._get_procar(self.stdin)

    def get_tot_procar(self):
        procar = self.get_procar()
        return procar[...,-1,-1]

    def get_emax_procar(self):
        procar = self.get_procar()
        tot_procar = procar[...,-1,-1]
        nm = np.max(tot_procar)
        atominfo = self.atominfo(getattr(self,'scfdir',self.stdin))
        tmp = 0
        data = []
        labels = []
        info = np.zeros(procar.shape[:3])
        value = np.zeros(procar.shape[:3])
        for atom,num in atominfo:
            # total %
            data.append(np.sum(procar[...,tmp:tmp+num,-1],axis=3))
            labels.append(atom)
        data = np.stack(data,axis=3)

        for i in range(procar.shape[0]):
            for j in range(procar.shape[1]):
                for k in range(procar.shape[2]):
                    value[i][j][k] = np.max(data[i,j,k])/nm
                    info[i][j][k] = np.argmax(data[i,j,k])

        return value,info,labels

    def get_pmax_procar(self):
        procar = self.get_procar()
        tot_procar = procar[...,-1,-1]
        nm = np.max(tot_procar)
        atominfo = self.atominfo(getattr(self,'scfdir',self.stdin))
        tmp = 0
        data = []
        labels = []
        info = np.zeros(procar.shape[:3])
        value = np.zeros(procar.shape[:3])
        for atom,num in atominfo:
            # s obrit %
            data.append(np.sum(procar[...,tmp:tmp+num,0],axis=3))
            labels.append(atom+'-s')
            # p obrit %
            data.append(np.sum(procar[...,tmp:tmp+num,1:4],axis=(3,4)))
            labels.append(atom+'-p')
            # d obrit %
            data.append(np.sum(procar[...,tmp:tmp+num,4:9],axis=(3,4)))
            labels.append(atom+'-d')
        data = np.stack(data,axis=3)

        for i in range(procar.shape[0]):
            for j in range(procar.shape[1]):
                for k in range(procar.shape[2]):
                    value[i][j][k] = np.max(data[i,j,k])/nm
                    info[i][j][k] = np.argmax(data[i,j,k])

        info = info.astype(int)
        return value,info,labels

class Jump2band(GrepBand):

    def __init__(self,stdin,kpath=None):
        from os.path import join,exists
        stdin = os.path.normcase(stdin)
        # set kpath part1 %
        if isinstance(kpath,list):
            self.kpath = self.set_kpath(kpath)
        elif isinstance(kpath,tuple):
            self.kpath = [kpath] 

        # set single or multi %
        if exists(join(stdin,'OUTCAR')):
            self.stdin = stdin          
        elif exists(join(stdin,'nonscf','band')):
            self.stdin = join(stdin,'nonscf','band')
            self.scfdir = join(stdin,'scf')
            self.emassdir = join(stdin,'nonscf','emass')
            if exists(join(stdin,'nonscf','band','OUTCAR')):
                self.__class__ = _Jump2band_single
            else:
                self.banddir = []
                for i in os.listdir(self.stdin):
                    if '-' in i and exists(join(self.stdin,i,'OUTCAR')):
                        self.banddir.append(i)
                if len(self.banddir):
                    self.__class__ = _Jump2band_multi    
                else:
                    raise IOError("Band calculation files not exists!")
        else:
            raise IOError("Band calculation files not exists!")
        # final autoset kpath %
        if kpath is None:
            try:
                self.kpath = self.get_kpath()
            except:
                if self.__class__ != Jump2band:
                    raise IOError("KPOINTS files not exists!") 

    @classmethod
    def fatband(cls,stdin,kpath=None):
        # set single or multi %
        from os.path import join,exists        
        if exists(join(stdin,'OUTCAR')):
            classmodel = 'base'
        elif exists(join(stdin,'nonscf','band')):
            scfdir = join(stdin,'scf')
            stdin = join(stdin,'nonscf','band')
            if exists(join(stdin,'OUTCAR')):
                cls = _Jump2band_single                
                classmodel = 'single'
            else:
                banddir = []
                for i in os.listdir(stdin):
                    if '-' in i and exists(join(stdin,i,'OUTCAR')):
                        banddir.append(i)
                if len(banddir):
                    cls = _Jump2band_multi
                    classmodel = 'multi'
                else:
                    raise IOError("Band calculation files not exists!")
        else:
            raise IOError("Band calculation files not exists!")
        # define fatband class
        class Jump2fatband(_fatband,cls):
            def __init__(self):
                self.kpath = None
                self.stdin = None

        jf = Jump2fatband()
        # set paths %
        jf.stdin = stdin
        if classmodel == 'single':
            jf.scfdir = scfdir
        elif classmodel == 'multi':
            jf.scfdir = scfdir
            jf.banddir = banddir        
        # set kpath %
        if isinstance(kpath,list):
            jf.kpath = jf.set_kpath(kpath)
        elif isinstance(kpath,tuple):
            jf.kpath = [kpath] 
        elif kpath is None:
            jf.kpath = jf.get_kpath()

        return jf

    def get_bands(self):
        return self._get_band(self.stdin)

    def get_kpath(self):
        return self._get_kpath(self.stdin)

    def get_kpoints(self,isnkpt=False):
        if isnkpt:
            return self._get_kpoint(self.stdin),self._get_band_insert(self.stdin)
        else:
            return self._get_kpoint(self.stdin)

    def get_fermi(self):
        return self.fermi_energy(self.stdin)  

    def get_cbmvbm(self,bands=None,kpoints=None):
        if not isinstance(bands,np.ndarray):
            bands = self.get_bands()
        if not isinstance(kpoints,np.ndarray):
            kpoints = self.get_kpoints()
        return self._get_cbmvbm(path=getattr(self,'scfdir',self.stdin),bands=bands,kpoints=kpoints)

    def get_force_cbmvbm(self,path):
        from os.path import exists,isdir,join
        if exists(path) and exists(join(path,'OUTCAR')):
            bands = self._get_band(path)
            kpoints = self._get_kpoint(path)
            return self._get_cbmvbm(path,bands,kpoints)
        else:
            bands = []
            kpoints = []
            for dir in os.listdir(path):
                subdir = join(path,dir)
                if isdir(subdir) and exists(join(subdir,'OUTCAR')):
                    bands.append(self._get_band(subdir))
                    kpoints.append(self._get_kpoint(subdir))
            shape = bands[0].shape
            bands = np.stack(bands,axis=1).reshape(shape[0],-1,shape[2],shape[3])
            kpoints = np.array(kpoints).reshape(-1,3)    
            return self._get_cbmvbm(subdir,bands,kpoints) 

    def get_bandgap(self,isdirect=False,bands=None):
        if not isinstance(bands,np.ndarray):
            bands = self.get_bands()
        cbids = self._get_cbid(path=getattr(self,'scfdir',self.stdin),bands=bands)
        for cbid,bands_ispin in zip(cbids,bands):
            cb = bands_ispin[:,cbid,0]
            vb = bands_ispin[:,cbid-1,0]
            gap = np.around(np.min(cb)-np.max(vb),4)
            if gap <= 0:
                return 0,False
            if np.argmin(cb) == np.argmax(vb):
                direct = True
            else:
                direct = False
            if direct:
                return gap,True
            elif isdirect:
                return np.around(np.min(cb-vb),4),False
            else:
                return gap,False

    def get_force_emass(self,path,fit_range=3):
        '''
        get Electron effective mass
        '''
        from os.path import exists,isdir,join
        axis = 'unknown'
        name = ['cbm','vbm']

        if exists(path) and exists(join(path,'OUTCAR')):
            bands = self._get_band(path)
            kpoints = self._get_kpoint(path)
            tmp=self._get_cbmvbm(path,bands,kpoints)
            emass = self._get_emass(path,axis,name,fit_range,bands=bands,kpoints=kpoints)
            tmp['cbm']['emass'] = emass['cbm-unknown']
            tmp['vbm']['emass'] = emass['vbm-unknown']
            return tmp
        else:
            cbm = []
            vbm = []
            # nogap = False
            for dir in os.listdir(path):
                subdir = join(path,dir)
                if isdir(subdir) and exists(join(subdir,'OUTCAR')):
                    bands = self._get_band(subdir)
                    kpoints = self._get_kpoint(subdir)
                    tmp=self._get_cbmvbm(subdir,bands,kpoints)
                    emass = self._get_emass(subdir,axis,name,fit_range,bands=bands,kpoints=kpoints)
                    tmp['cbm']['emass'] = emass['cbm-unknown']
                    tmp['vbm']['emass'] = emass['vbm-unknown']
                    cbm.append(tmp['cbm'])
                    vbm.append(tmp['vbm'])
            cvdata = {'cbm':cbm[np.argmin([item["energy"] for item in cbm])],
                      'vbm':vbm[np.argmax([item["energy"] for item in vbm])]}
            return cvdata

    def get_locpot(self,axis='z'):
        if getattr(self,'scfdir',False) and os.path.exists(self.scfdir):
            locpot = self.locpot(self.scfdir,axis)
            vaccum_level = locpot[0]
            return vaccum_level
        else:
            raise IOError("scf path not exist or function is not supported")

    def plot_kpath(self):
        kpath = []
        def str2latex(kpt):
            latex = ['alpha','beta','gamma','delta','epsilon','varepsilon','zeta','eta',
                     'theta','vartheta','iota','kappa','lambda','mu','nu','xi','pi','varpi',
                     'rho','varrho','sigma','varsigma','tau','upsilon','phi','varphi',
                     'chi','psi','omega']
            if kpt.lower() in latex:
                return '\\'+kpt.capitalize()
            else:
                return kpt

        def kprint(k1,k2=None):
            if len(k1) > 1:
                k1 = str2latex(k1)
                if '\\' in k1: k1='$'+k1
                else: k1 = '${0}_{1}'.format(k1[0],k1[1:])
            if k2:
                if len(k2) > 1:
                    k2 = str2latex(k2)
                    if k1[0]!='$': k1='$'+k1
                    if '\\' in k2: k1='{0}|{1}'.format(k1,k2)
                    else: k1 = '{0}|{1}_{2}'.format(k1,k2[0],k2[1:])
                else: k1='{0}|{1}'.format(k1,k2)
            if k1[0] == '$': k1=k1+'$'
            kpath.append(k1)

        for index,kp in enumerate(self.kpath):
            if index == 0: kprint(kp[0])
            for k in kp[1:-1]:
                kprint(k)
            if index < len(self.kpath)-1:
                kprint(kp[-1],self.kpath[index+1][0])
            else: 
                kprint(kp[-1])
        return kpath  

class _Jump2band_single(Jump2band):

    def __init__(self,stdin,kpath=None):
        from os.path import join
        self.scfdir = join(stdin,'scf')
        self.stdin = join(stdin,'nonscf','band')

        if isinstance(kpath,list):
            self.kpath = self.set_kpath(kpath)
        elif isinstance(kpath,tuple):
            self.kpath = [kpath] 
        elif kpath is None:
            self.kpath = self.get_kpath()

class _Jump2band_multi(Jump2band):

    def __init__(self,stdin,kpath=None):
        from os.path import join,exists
        # super().__init__(stdin,kpath)
        self.stdin = join(stdin,'nonscf','band')
        self.scfdir = join(stdin,'scf')
        self.emassdir = join(stdin,'nonscf','emass')
        self.banddir = []
        for i in os.listdir(self.stdin):
            if '-' in i and exists(join(self.stdin,i,'OUTCAR')):
                self.banddir.append(i)

        if isinstance(kpath,list):
            self.kpath = self.set_kpath(kpath)
        elif isinstance(kpath,tuple):
            self.kpath = [kpath] 
        elif kpath is None:
            self.kpath = self.get_kpath()


    def get_kpath(self,auto=False):
        try:
            from jump2.abtools.brillouin_zone import HighSymmetryKpath
        except:
            print('Import HighSymmetryKpath moudle failed!')
            return self.set_kpath(self.banddir)
            
        cell = self.get_cell(os.path.join(self.stdin,self.banddir[0]))
        bz = HighSymmetryKpath()
        kpoint = bz.get_HSKP(cell)
        banddir = self.banddir
        for i,kpts in enumerate(kpoint['Path']):
            for j in range(len(kpts)-1):
                A_B = kpts[j].strip('\\')+'-'+kpts[j+1].strip('\\')
                if A_B not in banddir:
                    return self.set_kpath(self.banddir)
                else:
                    banddir.remove(A_B)
            if len(banddir) == 0:
                break
        return kpoint['Path'][:i+1]

    def get_bands(self):
        bands = []
        for k in self.kpath:
            for i in range(len(k)-1):
                dirname = k[i].lstrip('\\')+'-'+k[i+1].lstrip('\\')
                bands.append(self._get_band(os.path.join(self.stdin,dirname)))
        shape = bands[0].shape
        bands = np.stack(bands,axis=1).reshape(shape[0],-1,shape[2],shape[3])
        return bands

    def get_fermi(self):
        efermi = []
        for k in self.kpath:
            for i in range(len(k)-1):
                dirname = k[i].lstrip('\\')+'-'+k[i+1].lstrip('\\')
                efermi.append(self.fermi_energy(os.path.join(self.stdin,dirname)))
        return max(efermi)

    def get_kpoints_with_weight(self):
        kpoints = []
        for k in self.kpath:
            for i in range(len(k)-1):
                dirname = k[i].lstrip('\\')+'-'+k[i+1].lstrip('\\')
                kpoints.append(self._get_kpoint(os.path.join(self.stdin,dirname)))
        return np.array(kpoints).reshape(-1,4) 

    def get_kpoints(self,isnkpt=False):
        kpoints = []
        for k in self.kpath:
            for i in range(len(k)-1):
                dirname = k[i].lstrip('\\')+'-'+k[i+1].lstrip('\\')
                kpoints.append(self._get_kpoint(os.path.join(self.stdin,dirname)))
        if isnkpt:
            return np.array(kpoints).reshape(-1,3),kpoints[0].shape[0]
        else:
            return np.array(kpoints).reshape(-1,3) 
        
    def get_emass(self,fit_range=3):
        '''
        get Electron effective mass
        emass_path : /noncsf/emass/x-cbm or  /noncsf/emass/x-cbm-vbm
        '''
        emass = {}
        for dir in os.listdir(self.emassdir):
            emass_path = os.path.join(self.emassdir,dir)
            # axis: x,y,z ; name: [cbm,vbm]
            axis = dir.split('-')[0]
            name = dir.split('-')[1:]
            emass.update(self._get_emass(emass_path,axis,name,fit_range))        
        return emass

class Jump2dos(GrepDos):
    
    def __init__(self,stdin):
        from os.path import join,exists
        # set single or multi %
        if exists(join(stdin,'OUTCAR')):
            self.stdin = stdin          
        elif exists(join(stdin,'nonscf','dos')):
            self.stdin = join(stdin,'nonscf','dos')
            self.scfdir = join(stdin,'scf')
        else:
            raise IOError("Dos calculation files not exists!")

    def get_force_dos(self,path):
        dos = self._get_dos(path)
        return self.get_dos(dos=dos)

    def get_fermi(self):
        return self.fermi_energy(self.stdin)

    def get_dos(self,dos=None):
        if not isinstance(dos,np.ndarray):
            dos=self._get_dos(self.stdin)
        dos_energy = dos[0,:,0]-self.get_fermi()
        dos_shape = dos.shape[-1]
        if dos_shape == 10:
            # self.dostype = 'pdos'
            self.spin = 1
            self.orbits=['s','p','d']
            dos_s = dos[:,:,1]
            dos_p = np.sum(dos[:,:,2:5],axis=2)
            dos_d = np.sum(dos[:,:,5:],axis=2)
            dos = np.stack((dos_s,dos_p,dos_d),axis=1)
        elif dos_shape == 4:
            # self.dostype = 'tdos'
            self.spin = 1
            self.orbits=['s','p','d']
            dos_s = dos[:,:,1]
            dos_p = dos[:,:,2]
            dos_d = dos[:,:,3]
            dos = np.stack((dos_s,dos_p,dos_d),axis=1)
        elif dos_shape == 7:
            # self.dostype = 'tdos-ispin'
            self.spin = 2
            self.orbits=['s','p','d']
            dos_s = dos[:,:,1]
            dos_p = dos[:,:,3]
            dos_d = dos[:,:,5]
            dos_up = np.stack((dos_s,dos_p,dos_d),axis=1)
            dos_s = dos[:,:,2]
            dos_p = dos[:,:,4]
            dos_d = dos[:,:,6]
            dos_down = np.stack((dos_s,dos_p,dos_d),axis=1)*-1
            dos = np.stack((dos_up,dos_down),axis=1)
        elif dos_shape == 19:
            # self.dostype = 'pdos-ispin'
            self.spin = 2
            self.orbits=['s','p','d']
            dos_s = dos[:,:,1]
            dos_p = np.sum(dos[:,:,(3,5,7)],axis=2)
            dos_d = np.sum(dos[:,:,(9,11,13,15,17)],axis=2)
            dos_up = np.stack((dos_s,dos_p,dos_d),axis=1)
            dos_s = dos[:,:,2]
            dos_p = np.sum(dos[:,:,(4,6,8)],axis=2)
            dos_d = np.sum(dos[:,:,(10,12,14,16,18)],axis=2)
            dos_down = np.stack((dos_s,dos_p,dos_d),axis=1)*-1
            dos = np.stack((dos_up,dos_down),axis=1)
        else:
            raise ("Code not support this DOSCAR!")
        return dos_energy,dos

class Jump2optic(GrepOptic):
    
    def __init__(self,stdin):
        from os.path import join,exists
        # set single or multi %
        if exists(join(stdin,'OUTCAR')):
            self.stdin = stdin          
        elif exists(join(stdin,'nonscf','dielectric')):
            self.stdin = join(stdin,'nonscf','dielectric')
            self.scfdir = join(stdin,'scf')
        else:
            raise IOError("optic calculation files not exists!")

    def get_dielectric_ionic(self):
        diel = self.dielectric_ionic(self.stdin)
        return np.mean(np.linalg.eig(diel)[0])

    def get_dielectric(self):
        diel = self.dielectric(self.stdin)
        return np.mean(np.linalg.eig(diel)[0])
