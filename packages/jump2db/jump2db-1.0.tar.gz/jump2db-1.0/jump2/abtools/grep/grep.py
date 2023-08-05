import numpy as np
import os
import re
        
class GrepOutcar(object):

    def __init__(self):
        pass

    def easysearch(self,path,keyword):
        line = os.popen("grep -a {0} {1}/OUTCAR|tail -1".format(keyword,path)).readline()
        result = re.findall(r"{0}\s*=\s*([-]?\d+)".format(keyword),line)[0]
        return int(result)

    def floatsearch(self,path,keyword,site='head'):
        line = os.popen("grep -a {0} {1}/OUTCAR|{2} -1".format(keyword,path,site)).readline()
        result = re.findall(r"{0}\s*=\s*([-|\.|\w]+)".format(keyword),line)[0]
        return float(result)

    def boolsearch(self,path,keyword):
        line = os.popen("grep -a {0} {1}/OUTCAR|tail -1".format(keyword,path)).readline()
        result = re.findall(r"{0}\s*=\s*(T|F)".format(keyword),line)[0]
        return result


    # int %
    def nkdim(self,path):
        return self.easysearch(path,'NKDIM')
  
    def nedos(self,path):
        return self.easysearch(path,'NEDOS')
  
    def nbands(self,path):
        return self.easysearch(path,'NBANDS')
  
    def nkpts(self,path):
        return self.easysearch(path,'NKPTS')
  
    def istart(self,path):
        return self.easysearch(path,'ISTART')
  
    def icharg(self,path):
        return self.easysearch(path,'ICHARG')
  
    def ispin(self,path):
        return self.easysearch(path,'ISPIN')

    def nelm(self,path):
        return self.easysearch(path,'NELM')

    def nsw(self,path):
        return self.easysearch(path,'NSW')

    def lmaxmix(self,path):
        return self.easysearch(path,'LMAXMIX')

    def ibrion(self,path):
        return self.easysearch(path,'IBRION')

    def nfree(self,path):
        return self.easysearch(path,'NFREE')

    def isif(self,path):
        return self.easysearch(path,'ISIF')

    def isym(self,path):
        return self.easysearch(path,'ISYM')

    def pstress(self,path):
        return self.easysearch(path,'PSTRESS')

    def nelect(self,path):
        return self.easysearch(path,'NELECT')

    def ismear(self,path):
        return self.easysearch(path,'ISMEAR')

    def ialgo(self,path):
        return self.easysearch(path,'IALGO')

    def lorbit(self,path):
        return self.easysearch(path,'LORBIT')
    
    # bool %
    def lsorbit(self,path):
        return self.boolsearch(path,'LSORBIT')
  
    def lwave(self,path):
        return self.boolsearch(path,'LWAVE')
  
    def lcharg(self,path):
        return self.boolsearch(path,'LCHARG')
  
    def lvtot(self,path):
        return self.boolsearch(path,'LVTOT')
  
    def lelf(self,path):
        return self.boolsearch(path,'LELF')

  
    # float % 
    def encut(self,path):
        return self.floatsearch(path,'ENCUT')
  
    def ediff(self,path):
        return self.floatsearch(path,'EDIFF')

    def ediffg(self,path):
        return self.floatsearch(path,'EDIFFG')

    def cshift(self,path):
        return self.floatsearch(path,'CSHIFT')

    def potim(self,path):
        return self.floatsearch(path,'POTIM')

    def emin(self,path):
        return self.floatsearch(path,'EMIN')

    def emax(self,path):
        return self.floatsearch(path,'EMAX')

    def sigma(self,path):
        return self.floatsearch(path,'SIGMA')

    def free_energy(self,path):
        return self.floatsearch(path,'TOTEN','tail')

    def energy_without_entropy(self,path):
        return self.floatsearch(path,'entropy','tail')

    # others %
    def date(self,path):
        line = os.popen("grep 'date ' {0}/OUTCAR|head -1".format(path)).readline()
        result = re.findall(r"(\d{4}.\d{1,2}.\d{1,2})",line)[0]
        return result

    def datetime(self,path):
        line = os.popen("grep 'date ' {0}/OUTCAR|head -1".format(path)).readline()
        result = re.findall(r"(\d{1,2}:\d{1,2})",line)[0]
        return result
  
    def vasp_version(self,path):
        line = os.popen('grep vasp {0}/OUTCAR|head -1'.format(path)).readline()
        result = re.findall(r"vasp\.(\d+[\.\d+]+)\s",line)[0]
        return result
  
    def point_group(self,path):
        line = os.popen("grep 'The point group' {0}/OUTCAR|tail -1".format(path)).readline()
        result = re.findall(r"([A-Z]_[a-z0-9]+)",line)[0]
        return result
  
    def prec(self,path):
        line = os.popen('grep PREC {0}/OUTCAR|tail -1'.format(path)).readline()
        result = re.findall(r"PREC\s*=\s*(\w+)",line)[0]
        return result
  
    def gga(self,path):
        line = os.popen('grep GGA {0}/OUTCAR|tail -1'.format(path)).readline()
        result = re.findall(r"GGA\s*=\s*(\S+)",line)[0]
        if result== '--': return 'PE'
        return result

    def volume(self,path):
        line = os.popen("grep 'volume of cell' {0}/OUTCAR|tail -1".format(path)).readline()
        result = re.findall(r"volume of cell\s*:\s*(\S+)",line)[0]
        return float(result)

    def fermi_energy(self,path):
        line = os.popen('grep E-fermi {0}/OUTCAR|tail -1'.format(path)).readline()
        result = re.findall(r"E-fermi\s*:\s*([-]?\d+\.\d+)",line)[0]
        return float(result)

    def force(self,path,unit='kb'):
        if unit == 'kb':
            line = os.popen("grep -A14 'FORCE on cell' {0}/OUTCAR | tail -1".format(path)).readline()
            return np.array(line.split()[2:],dtype=float)
        else :
            line = os.popen("grep -A13 'FORCE on cell' {0}/OUTCAR | tail -1".format(path)).readline()
            return np.array(line.split()[1:],dtype=float)

    def max_force(self,path,unit='kb'):
        if len(self.force(path,unit)):
            return np.max(np.abs(self.force(path,unit)))
        else: 
            return None
        
  
    def lattice_vectors(self,path,status='end'):
        if status == 'end':
            lines = os.popen("grep -A4 'direct lattice vectors' {0}/OUTCAR | tail -4".format(path)).readlines()
        else:
            lines = os.popen("grep -A4 'direct lattice vectors' {0}/OUTCAR | head -5 | tail -4".format(path)).readlines()

        datas = []
        for line in lines:
           data = re.findall(r"[-]?\d\.\d+",line)
           if  len(data) == 6:
               datas.append(data)
        return np.array(datas,dtype=float)
  
    def direct_lattice_vectors(self,path,status='end'):
        return self.lattice_vectors(path,status)[:,:3]

    def reciprocal_lattice_vectors(self,path,status='end'):
        return self.lattice_vectors(path,status)[:,3:]

    def length_of_vector(self,path,status='end'):
        if status == 'end':
            line = os.popen("grep -A1 'length of vectors' {0}/OUTCAR | tail -1".format(path)).readline()
        else:
            line = os.popen("grep -A1 'length of vectors' {0}/OUTCAR | head -2 | tail -1".format(path)).readline()
        return np.array(re.findall(r"\d+\.\d+",line),dtype=float)

    def atominfo(self,path):
        atom = os.popen("head -6 {0}/POSCAR | tail -1".format(path)).readline().split()
        atom_num = os.popen("head -7 {0}/POSCAR | tail -1".format(path)).readline().split()
        atom_num = map(int,atom_num) 
        return zip(atom,atom_num)

    def cell(self,path):
        with open(os.path.join(path,'POSCAR')) as f:
            text=f.readlines()
            lattice=[]
            for line in text[2:5]:
                lattice.append(line.split())
            lattice = np.array(lattice,dtype='float')
            number = np.array(text[6].split(),dtype='int')
            atom=[]
            for i,num in enumerate(number):
                atom.extend([i]*num)
            atom=np.array(atom,dtype='int')
            position=[]
            for line in text[8:8+len(atom)]:
                position.append(line.split())
            position = np.array(position,dtype='float')
        return lattice,position,atom 

    def locpot(self,path,axis=None):
        with open(os.path.join(path,'LOCPOT')) as f:
            text=f.readlines()
        skip=sum(np.array(text[6].split(),dtype=int))
        shape=np.array(text[9+skip].split(),dtype=int)
        data=[]
        for line in text[10+skip:] :
            data.extend(line.split())
        data=np.array(data,dtype=float).reshape(shape[::-1]).transpose(2,1,0)
        if axis == None:
            return data
        if axis == 'x':
            return np.mean(np.mean(data,axis=1),1)
        if axis == 'y':
            return np.mean(np.mean(data,axis=1),0)
        if axis == 'z':
            return np.mean(np.mean(data,axis=0),0)


class Vasp_grep(GrepOutcar):
    def __init__(self,stdin):
        self.stdin = stdin

    def grep(self,value):
        func = getattr(self,value)
        return func(self.stdin)

class Subband(GrepOutcar):
    def __init__(self):
        pass

    def get_band(self,path):
        ispin = self.ispin(path)
        nkpts = self.nkpts(path)
        nband = self.nbands(path)
        banddat = self.grep_band(path,nband)
        assert len(banddat) == ispin*nkpts*(nband+2)-1
        bands = []
        for dat in banddat:
            value = dat.split()
            if len(value)!= 3: continue
            bands.append(value[1:])
        bands = np.array(bands,dtype=float).reshape(ispin,nkpts,nband,2)
        return bands

    def get_kpoint(self,path,weight=False):
        nkpts = self.nkpts(path)
        kpointdat=self.grep_kpoint(path,nkpts)
        kpoints = []
        if weight:
            for dat in kpointdat:
                kpoints.append(dat.split()[:4])
        else:
            for dat in kpointdat:
                kpoints.append(dat.split()[:3])
        return np.array(kpoints,dtype=float)
            
    def grep_kpoint(self,path,nkpts):
        return os.popen("grep -A {0} 'k-points in reciprocal' {1}/OUTCAR|tail -{0}".format(nkpts,path)).readlines()

    def grep_band(self,path,nbands):
        return os.popen("grep -A {0} occupation {1}/OUTCAR".format(nbands,path)).readlines()

    def get_cbvb(self,path,bands=None):
        if not isinstance(bands,np.ndarray):
            bands = self.get_band(path)
        nelect = self.nelect(path)/2
        cbids = []
        for bands_ispin in bands:
            for index in np.arange(nelect,bands_ispin.shape[1]):
                if max(bands_ispin[:,index,1]) < 0.001:
                    cbids.append(index)
                    break
        return cbids


class Jump2band(Subband):

    def __init__(self,stdin,kpath=None):
        self.expath = os.path.join(stdin,'scf')
        self.stdin = os.path.join(stdin,'nonscf','band')
        self.empath = os.path.join(stdin,'nonscf','emass')
        self.params = {}
        if isinstance(kpath,list):
            self.kpath = self.set_kpath(kpath)
        elif isinstance(kpath,tuple):
            self.kpath = [kpath] 
        elif isinstance(kpath,str):
            pass
        else:
            self.kpath = self.get_kpath()

    def get_emass_cbmvbm(self,type='mean'):
        '''
        self.params = {'cbm-x':3.3443, 'vbm-x':0.4442}
        return: {'cbm':3.3443, 'vbm':0.4442}
        get mean
        '''
        trans = {}
        if isinstance(self.params,dict) and type=='mean':
            for key,value in self.params.items():
                if 'cbm' in k or 'vbm' in k:
                    k = key.split('-')[0]
                else: 
                    continue
                if k not in trans:
                    trans[k] = value
                else:
                    trans[k] = round((trans[k]+value)/2,4)
            return trans
        

    def get_locpot(self):
        #plt.plot(np.arange(len(locpot)),locpot)
        #plt.savefig('locpot.png')
        locpot = self.locpot(self.expath,axis='z')
        vaccum_level = locpot[0]
        return vaccum_level

    def get_bands(self):
        bands = []
        for k in self.kpath:
            for i in range(len(k)-1):
                dirname = k[i].lstrip('\\')+'-'+k[i+1].lstrip('\\')
                bands.append(self.get_band(os.path.join(self.stdin,dirname)))
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

    def get_kpoints(self,isnkpt=False):
        kpoints = []
        for k in self.kpath:
            for i in range(len(k)-1):
                dirname = k[i].lstrip('\\')+'-'+k[i+1].lstrip('\\')
                kpoints.append(self.get_kpoint(os.path.join(self.stdin,dirname)))
        if isnkpt:
            return np.array(kpoints).reshape(-1,3),kpoints[0].shape[0]
        else:
            return np.array(kpoints).reshape(-1,3) 

    def plot_kpath(self):
        kpath = []
        def kprint(k1,k2=None):
            if len(k1) > 1:
                if '\\' in k1: k1='$'+k1
                elif 'Gamma' in k1 or 'Lambda' in k1 or 'Sigma' in k1 or 'Delta' in k1: k1='$\\'+k1
                else: k1 = '${0}_{1}'.format(k1[0],k1[1:])
            if k2:
                if len(k2) > 1:
                    if k[0]!='$': k1='$'+k1
                    if '\\' in k2: k1='{0}|{1}'.format(k1,k2)
                    elif 'Gamma' in k2 or 'Lambda' in k2 or 'Sigma' in k2 or 'Delta' in k2: k1='{0}|\\{1}'.format(k1,k2)
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

    def get_cbvb(self,bands=None):
        if not isinstance(bands,np.ndarray):
            bands = self.get_bands()
        nelect = self.nelect(self.expath)/2
        cbids = []
        for bands_ispin in bands:
            for index in np.arange(nelect,bands_ispin.shape[1]):
                if max(bands_ispin[:,index,1]) < 0.001:
                    cbids.append(index)
                    break
        return cbids

    def get_bandgap(self,isdirect=False):
        bands = self.get_bands()
        kpoints = self.get_kpoints()
        cbids = self.get_cbvb(bands)
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

    def get_force_cbmvbm(self,path):
        from os.path import exists,isdir,join
        if exists(path) and exists(join(path,'OUTCAR')):
            bands = self.get_band(path)
            kpoints = self.get_kpoint(path)
        else:
            for dir in os.listdir(path):
                bands = []
                kpoints = []
                subdir = join(path,dir)
                if isdir(subdir) and exists(join(subdir,'OUTCAR')):
                    bands.append(self.get_band(subdir))
                    kpoints.append(self.get_kpoint(subdir))
                    shape = bands[0].shape
            bands = np.stack(bands,axis=1).reshape(shape[0],-1,shape[2],shape[3])
            kpoints = np.array(kpoints).reshape(-1,3)           
        cbids = self.get_cbvb(bands)
        for cbid,bands_ispin in zip(cbids,bands):
            cb = bands_ispin[:,cbid,0]
            cbm = {'id':np.argmin(cb),
                   'energy':np.min(cb),
                   'kpoint':kpoints[np.argmin(cb)]}
            vb = bands_ispin[:,cbid-1,0]
            vbm = {'id':np.argmax(vb),
                   'energy':np.max(vb),
                   'kpoint':kpoints[np.argmax(vb)]}
            cvdata={'cbm':cbm,'vbm':vbm}
            if cbm['energy'] < vbm['energy']: cvdata['nogap'] = True
            return cvdata

    def get_cbmvbm(self,bands=None,kpoints=None):
        if not isinstance(bands,np.ndarray):
            bands = self.get_bands()
        if not isinstance(kpoints,np.ndarray):
            kpoints = self.get_kpoints()
        cbids = self.get_cbvb(bands)
        for cbid,bands_ispin in zip(cbids,bands):
            cb = bands_ispin[:,cbid,0]
            cbm = {'id':np.argmin(cb),
                   'energy':np.min(cb),
                   'kpoint':kpoints[np.argmin(cb)]}
            vb = bands_ispin[:,cbid-1,0]
            vbm = {'id':np.argmax(vb),
                   'energy':np.max(vb),
                   'kpoint':kpoints[np.argmax(vb)]}
            cvdata={'cbm':cbm,'vbm':vbm}
            if cbm['energy'] < vbm['energy']: cvdata['nogap'] = True
            return cvdata

    def get_single_emass(self,path,axis,etype=['cbm','vbm'],fit_range=3):
        from scipy.optimize import curve_fit
        import scipy.constants as sc
        bands=self.get_band(path)
        kpoints=self.get_kpoint(path)
        rec_vector = self.reciprocal_lattice_vectors(self.expath)*sc.pi*2
        kstep = np.linalg.norm((kpoints[-1]-kpoints[0])/(len(kpoints)-1)*rec_vector)/sc.angstrom
        xkpt=range(1,2*(fit_range+1))*kstep
        cbids = self.get_cbvb(bands)
        mod=lambda x,a,b,c:a*x**2 + b*x + c

        for cbid,bands_ispin in zip(cbids,bands):
            emass = {}
            if 'cbm' in etype:
                cb = bands_ispin[:,cbid,0]
                index = np.argmin(cb)
                if index < fit_range:
                     massband=cb[:2*fit_range+1]*sc.e
                elif  index >= len(kpoints) - fit_range:
                    massband=cb[-2*fit_range-1:]*sc.e
                else:
                    massband=cb[index-fit_range:index+fit_range+1]*sc.e
                a,b,c = curve_fit(mod,xkpt,massband)[0]
                emass['cbm'+'-'+axis]=np.around(sc.hbar**2/(2*a)/sc.electron_mass,4)
                if self.emass_cbvb:
                    self.params['cbm-'+axis]=min(cb)
            if 'vbm' in etype:
                vb = bands_ispin[:,cbid-1,0]
                index = np.argmax(vb)
                if index < fit_range:
                     massband=vb[:2*fit_range+1]*sc.e
                elif  index >= len(kpoints) - fit_range:
                    massband=vb[-2*fit_range-1:]*sc.e
                else:
                    massband=vb[index-fit_range:index+fit_range+1]*sc.e
                a,b,c = curve_fit(mod,xkpt,massband)[0]
                emass['vbm'+'-'+axis]=np.around(sc.hbar**2/(-2*a)/sc.electron_mass,4)
                if self.emass_cbvb:
                    self.params['vbm-'+axis]=max(vb)
            return emass

    def get_emass(self,bands=None,fit_range=3):
        emass = {}
        if self.emass_cbvb:
            self.params = {}
        for dir in os.listdir(self.empath):
            emass_path = os.path.join(self.empath,dir)
            keys = dir.split('-')
            emass.update(self.get_single_emass(emass_path,keys[0],keys[1:],fit_range))

        return emass

    def set_kpath(self,band):
        import re
        # search next %
        def head(k,band):
            knext=[]
            bandn=[]
            bandpop=[]
            for i,d in enumerate(band):
                if re.search('^%s-'%k,d):
                    knext.append(d.split('-')[1])
                    bandpop.append(d)
                else:
                    bandn.append(d)
            if len(knext) == 1:
                return knext[0],bandn
            else:
                return None,band
        # search last %
        def tail(k,band):
            klast=[]
            bandn=[]
            for d in band:
                if re.search('-%s$'%k,d):
                    klast.append(d.split('-')[0])
                else:
                    bandn.append(d)
            if len(klast) == 1:
                return klast[0],bandn
            else:
                return None,band
        sort_kpath=[]
        while len(band):
            init = band.pop(-1)
            kpath = init.split('-')
            klen = len(band)
            while klen:
                # search next %
                knext,band = head(kpath[-1],band)
                if knext:
                    kpath.append(knext)
                # search last %
                klast,band = tail(kpath[0],band)
                if klast:
                    kpath.insert(0,klast)
                if len(band) == klen:
                    break
                else:
                    klen=len(band)
            sort_kpath.append(kpath)
        klen = [len(k) for k in sort_kpath] 
        kklen = len(klen)
        sorted_kpath=[]
        while kklen > 1:
            kid = np.argsort(klen)[-1]
            init = sort_kpath[kid]
            for k in np.argsort(klen)[::-1][1:]:
                if sort_kpath[k][0] == init[-1]:
                    sort_kpath[kid].extend(sort_kpath.pop(k)[1:])
                    break
                if sort_kpath[k][-1] == init[0]:
                    sort_kpath[k].extend(sort_kpath.pop(kid)[1:])
                    break
                if init[0] == init[-1]:
                    if init.count(sort_kpath[k][0]):
                        index = init.index(sort_kpath[k][0])
                        sort_kpath[kid] = init[index:]
                        sort_kpath[kid].extend(init[1:index+1])
                        sort_kpath[kid].extend(sort_kpath.pop(k)[1:])
                        break
                    if init.count(sort_kpath[k][-1]):
                        index = init.index(sort_kpath[k][0])
                        sort_kpath[kid] = init[index:]
                        sort_kpath[kid].extend(init[1:index+1])
                        sort_kpath[k].extend(sort_kpath.pop(kid)[1:])
                        break
            klen = [len(k) for k in sort_kpath] 
            if len(klen) < kklen:
                kklen =len(klen)
            else:
                kid = np.argmax(klen)
                sorted_kpath.append(sort_kpath.pop(kid))
                klen.pop(kid)
                kklen = len(klen)
        sorted_kpath.append(sort_kpath[0]) 
        return sort_kpath

    def get_kpath(self):
        try:
            current_kpath = os.listdir(os.path.join(self.stdin))
            current_cell = self.cell(os.path.join(self.stdin,current_kpath[0]))
        except:
            print('Please make sure the band_calculation of {0} finished'.format(self.stdin))
            raise
        try:
            from brillouin_zone import HighSymmetryKpath
        except:
            return self.set_kpath(current_kpath) 
        bz = HighSymmetryKpath()
        kpoint = bz.get_HSKP(current_cell)
        kpath_number = 1
        tmp = 0
        for i,kpts in enumerate(kpoint['Path']):
            if len(kpts)+tmp-1 == len(current_kpath):
                kpath_number = i 
                break
            else:
                tmp += len(kpts)-1
        return kpoint['Path'][:kpath_number+1]

class Subdos(GrepOutcar):
 
    def __init__(self):
        pass
 
    def fermi_energy(self,path):
        line = os.popen("head -6 {0}/DOSCAR | tail -1".format(path)).readline() 
        return float(line.split()[3])

    def emin(self,path):
        line = os.popen("head -6 {0}/DOSCAR | tail -1".format(path)).readline() 
        return float(line.split()[1])

    def emax(self,path):
        line = os.popen("head -6 {0}/DOSCAR | tail -1".format(path)).readline() 
        return float(line.split()[0])

    def nedos(self,path):
        line = os.popen("head -6 {0}/DOSCAR | tail -1".format(path)).readline() 
        return int(line.split()[2])

    def get_single_dos(self,path):
        nedos = self.nedos(path)
        doses = []        
        with open(path+'/DOSCAR','r') as f:
            for i in range(nedos+6): 
                f.readline()
            while f.readline():
                dos=[]
                for i in range(nedos):
                    dos.append(f.readline().split())
                doses.append(dos)
            doses = np.array(doses,dtype=float)
        return doses
                

class Jump2dos(Subdos):
    
    def __init__(self,stdin):
        self.expath = os.path.join(stdin,'scf')
        self.stdin = os.path.join(stdin,'nonscf','dos')

    def get_fermi(self):
        return self.fermi_energy(self.stdin)

    def get_dos(self,dos=None):
        if dos == None:
            dos=self.get_single_dos(self.stdin)
        dos_energy = dos[0,:,0]-self.get_fermi()
        dos_shape = dos.shape[-1]
        if dos_shape == 10:
            dostype = 'pdos'
            self.spin = 1
            self.orbits=['s','p','d']
            dos_s = dos[:,:,1]
            dos_p = np.sum(dos[:,:,2:5],axis=2)
            dos_d = np.sum(dos[:,:,5:],axis=2)
            dos = np.stack((dos_s,dos_p,dos_d),axis=1)
        elif dos_shape == 4:
            dostype = 'tdos'
            self.spin = 1
            self.orbits=['s','p','d']
            dos_s = dos[:,:,1]
            dos_p = dos[:,:,2]
            dos_d = dos[:,:,3]
            dos = np.stack((dos_s,dos_p,dos_d),axis=1)
        elif dos_shape == 7:
            dostype = 'tdos-ispin'
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
            dostype = 'pdos-ispin'
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


class Jump2fatband(GrepProcar):

    def __init__(self,path):        
        self.expath = os.path.join(stdin,'scf')
        self.stdin = os.path.join(stdin,'nonscf','fatband')
        self.params = None
        if isinstance(kpath,list):
            self.kpath = self.set_kpath(kpath)
        elif isinstance(kpath,tuple):
            self.kpath = [kpath] 
        elif isinstance(kpath,str):
            pass
        else:
            self.kpath = self.get_kpath()

        # self.nkpts = None
        # self.nband = None
        # self.nions = None
        # self.kpoints = None
        # self.bands = None
        # self.procar = None
        # self.path = None

    def get_data(self,path):
        if not os.path.exists(os.path.join(path,'PROCAR')): 
            raise IOError("File 'PROCAR' not exists!") 
        else:
            self.expath = path
            self.path = path
        line = os.popen("head -2 {0}/PROCAR|tail -1".format(path)).readline()
        value = line.split()
        ispin = self.ispin(path)
        self.nkpts = nkpts = int(value[3])
        self.nband = nband = int(value[7]) 
        self.nions = nions = int(value[11])

        # kpoints %
        lines = os.popen("grep ^' k-point' {0}/PROCAR ".format(path)).readlines()
        kpoints = []
        for line in lines[:nkpts]:
            kpoints.append(line.split()[3:6])
        kpoints = np.array(kpoints,dtype=float)
        assert kpoints.shape == (nkpts,3)

        # bands %
        lines = os.popen("grep ^'band' {0}/PROCAR ".format(path)).readlines()
        bands = []
        band = []
        num = 1
        for line in lines:
            value = line.split()
            index = int(value[1])
            energy = float(value[4])
            occ = float(value[7])
            band.append([energy,occ])
            if index == nband:
                bands.append(band)
                band = []
                num +=1
                if num > nkpts:
                    break
        bands = np.array(bands,dtype=float)
        if ispin == 1:
            assert bands.shape == (nkpts,nband,2)
            bands = bands.reshape(1,nkpts,nband,2)
        elif ispin == 2:
            assert bands.shape == (nkpts*2,nband,2)
            bands = bands.reshape(2,nkpts,nband,2)
        else:
            raise KeyError("Invalid ispin value")

        # procar %
        lines = os.popen("grep -A{1} ^'ion' {0}/PROCAR ".format(path,nions+1)).readlines()
        procar = []
        num = 0
        for line in lines:
            if num > nions+1:
                num = -1
            elif num > 0:
                value = line.split()[1:]
                procar.append(value)
            num += 1
        if ispin == 1:
            assert len(procar) == nkpts*nband*(nions+1)
            procar = np.array(procar,dtype=float).reshape(1,nkpts,nband,nions+1,-1)
        elif ipsin == 2:
            assert len(procar) == 2*nkpts*nband*(nions+1)
            procar = np.array(procar,dtype=float).reshape(2,nkpts,nband,nions+1,-1)
        
        self.kpoints = kpoints
        self.bands = bands
        self.procar = procar

    def get_bands(self,path):
        if path != self.path or self.bands is None:
            self.get_data(path)
        return self.bands

    def get_kpoints(self,path=None,isnkpt=False,**kwargs):
        if (path and path != self.path) or self.kpoints is None:
            self.get_data(path)
        if isnkpt:
            return self.kpoints,self.nkpts
        else:
            return self.kpoints

    def get_procar(self,path):
        if path !=path or self.procar is None:
            self.get_data(path)
        return self.procar

    def get_tot_procar(self,path):
        procar = self.get_procar(path)
        return procar[...,-1,-1]

    def get_emax_procar(self,path):
        procar = self.get_procar(path)
        tot_procar = self.get_tot_procar(path)
        nm = np.max(tot_procar)
        atominfo = self.atominfo(path)
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


    def get_pmax_procar(self,path):
        procar = self.get_procar(path)
        tot_procar = self.get_tot_procar(path)
        nm = np.max(tot_procar)
        atominfo = self.atominfo(path)
        tmp = 0
        data = []
        labels = []
        info = np.zeros(procar.shape[:3])
        value = np.zeros(procar.shape[:3])
        for atom,num in atominfo:
            # s obrit %
            data.append(np.sum(procar[...,tmp:tmp+num,1],axis=3))
            labels.append(atom+'-s')
            # s obrit %
            data.append(np.sum(procar[...,tmp:tmp+num,2:5],axis=(3,4)))
            labels.append(atom+'-p')
            # s obrit %
            data.append(np.sum(procar[...,tmp:tmp+num,6:11],axis=(3,4)))
            labels.append(atom+'-d')
        data = np.stack(data,axis=3)

        for i in range(procar.shape[0]):
            for j in range(procar.shape[1]):
                for k in range(procar.shape[2]):
                    value[i][j][k] = np.max(data[i,j,k])/nm
                    info[i][j][k] = np.argmax(data[i,j,k])

        return value,info,labels

class Suboptic(GrepOutcar):
 
    def __init__(self):
        pass

    def dielectric_ionic(self,path):
        lines = os.popen("grep -A4 'MACROSCOPIC STATIC DIELECTRIC TENSOR IONIC CONTRIBUTION' {0}/OUTCAR|tail -3".format(path)).readlines()
        diel = []
        for line in lines:
            diel.append(line.split())
        return np.array(diel,dtype=float)

    def dielectric(self,path):
        lines = os.popen("grep -A4 'MACROSCOPIC STATIC DIELECTRIC TENSOR (including local field effects in DFT)' {0}/OUTCAR|tail -3".format(path)).readlines()
        diel = []
        for line in lines:
            diel.append(line.split())
        return np.array(diel,dtype=float)

class Jump2optic(Suboptic):
    
    def __init__(self,stdin):
        self.expath = os.path.join(stdin,'scf')
        self.dielpath = os.path.join(stdin,'nonscf','dielectric')

    def get_dielectric_ionic(self):
        diel = self.dielectric_ionic(self.dielpath)
        return np.mean(np.linalg.eig(diel)[0])

    def get_dielectric(self):
        diel = self.dielectric(self.dielpath)
        return np.mean(np.linalg.eig(diel)[0])
