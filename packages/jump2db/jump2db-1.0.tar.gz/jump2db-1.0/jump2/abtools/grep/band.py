from .outcar import GrepOutcar
import numpy as np
import os
import re

class GrepBand(GrepOutcar):
    def __init__(self):
        pass

    def _get_band(self,path):
        # if gw band %
        ialgo = self.ialgo(path)
        if ialgo == 4:
            return self._get_gw_band(path)
        ispin = self.ispin(path)
        nkpts = self.nkpts(path)
        nband = self.nbands(path)
        banddat = self.grep_band(path,nband)
        assert len(banddat) == ispin*nkpts*nband
        bands = []
        for dat in banddat:
            value = dat.split()
            if len(value)!= 3: continue
            bands.append(value[1:])
        bands = np.array(bands,dtype=float).reshape(ispin,nkpts,nband,2)
        return bands

    def _get_gw_band(self,path,last=True):
        gw_nelm = self.gw_nelm(path)
        assert gw_nelm > 0
        ispin = self.ispin(path)
        nkpts = self.nkpts(path)
        nband = self.nbands(path)+1
        banddat = self.grep_band(path,nband)
        assert len(banddat) == gw_nelm*ispin*nkpts*(nband)
        bands = []
        if last is True: 
            for i,dat in enumerate(banddat[-ispin*nkpts*nband:]):
                value = dat.split()
                if len(value)!= 7: 
                    continue
                bands.append([value[2],value[-1]])
            bands = np.array(bands,dtype=float).reshape(ispin,nkpts,nband-1,2)
        return bands

    def _get_kpoint(self,path,weight=False):
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

    def _get_band_insert(self,path):
        with open(os.path.join(path,'KPOINTS')) as f:
            f.readline()   
            band_insert = int(f.readline())
        return band_insert

    def _get_kpath(self,path):
        with open(os.path.join(path,'KPOINTS')) as f:
            f.readline()   
            nkpt = int(f.readline())
            model = f.readline().strip()
            if model.startswith(('L','l')):
                kpath = []
                for i in f:
                    kpoint = re.findall(r"[-]?\d\.\d+",i.split('!')[0])
                    if len(kpoint) == 3 and '#' not in i.split('!')[0]:
                        kpath.append(re.sub('\W+','',i.split('!')[1]))
        assert (len(kpath) & 1) == 0
        kpath_total = []
        kpath_part = [kpath[0]]
        for i,k in enumerate(kpath[1::2],1):
            if len(kpath) == 2*i:
                kpath_part.append(k)
                kpath_total.append(kpath_part)
            elif k == kpath[2*i]:
                kpath_part.append(k)
            else: 
                kpath_part.append(k)           
                kpath_total.append(kpath_part)     
                kpath_part = [kpath[2*i]]
        return kpath_total
 
    def _get_cbid(self,path,bands=None):
        if not isinstance(bands,np.ndarray):
            bands = self._get_band(path)
        nelect = int(self.nelect(path)/2)
        cbids = []
        for bands_ispin in bands:
            for index in np.arange(nelect,bands_ispin.shape[1]):
                if max(bands_ispin[:,index,1]) < 0.001:
                    cbids.append(index)
                    break
        return cbids

    def _get_emass(self,path,axis=None,name=['cbm','vbm'],fit_range=3,bands=None,kpoints=None):
        from scipy.optimize import curve_fit
        import scipy.constants as sc
        if not isinstance(bands,np.ndarray):
            bands = self._get_band(path)
        if not isinstance(kpoints,np.ndarray):
            kpoints = self._get_kpoint(path)
        rec_vector = self.reciprocal_lattice_vectors(path)*sc.pi*2
        kstep = np.linalg.norm((kpoints[-1]-kpoints[0])/(len(kpoints)-1)*rec_vector)/sc.angstrom
        xkpt=range(1,2*(fit_range+1))*kstep
        cbids = self._get_cbid(path=path,bands=bands)
        mod=lambda x,a,b,c:a*x**2 + b*x + c

        for cbid,bands_ispin in zip(cbids,bands):
            emass = {}
            if 'cbm' in name:
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
                # if isinstance(self.params,dict):
                #     self.params['cbm-'+axis]=min(cb)
            if 'vbm' in name:
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
                # if isinstance(self.params,dict):
                #     self.params['vbm-'+axis]=max(vb)
            return emass

    def _get_cbmvbm(self,path,bands,kpoints):          
        cbids = self._get_cbid(path,bands=bands)
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

    def set_kpath(self,band):
        import re
        # search next %
        def head(k,band):
            knext=[]
            bandn=[]
            bandpop=[]
            for d in band:
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
            klen = [len(k) for k in sort_kpath] 
            if len(klen) < kklen:
                kklen =len(klen)
            else:
                kid = np.argmax(klen)
                sorted_kpath.append(sort_kpath.pop(kid))
                klen.pop(kid)
                kklen = len(klen)
        sorted_kpath.append(sort_kpath[0]) 
        return sorted_kpath

    def str2latex(self,kpt):
        latex = ['alpha','beta','gamma','delta','epsilon','varepsilon','zeta','eta',
                 'theta','vartheta','iota','kappa','lambda','mu','nu','xi','pi','varpi',
                 'rho','varrho','sigma','varsigma','tau','upsilon','phi','varphi',
                 'chi','psi','omega']
        if kpt.lower() in latex:
            return '\\'+kpt.capitalize()
        else:
            return kpt

class GrepProcar(GrepBand):
    def __init__(self):
        pass

    def _procar_info(self,path):
        if not os.path.exists(os.path.join(path,'PROCAR')): 
            super()
            raise IOError("File 'PROCAR' not exists!") 
        else:       
            with open(os.path.join(path,'PROCAR'),'r') as f:
                f.readline()
                line = f.readline()
        return line

    def nkpts(self,path):
        if os.path.exists(os.path.join(path,'PROCAR')):            
            return int(self._procar_info(path).split()[3])
        else:
            return super().nkpts(path)

    def nbands(self,path):
        if os.path.exists(os.path.join(path,'PROCAR')):            
            return int(self._procar_info(path).split()[7])
        else:
            return super().nbands(path)

    def nions(self,path):
        if os.path.exists(os.path.join(path,'PROCAR')):            
            return int(self._procar_info(path).split()[11])
        else:
            return sum([i[1] for i in self.atominfo(path)])

    def _get_kpoint(self,path,weight=False):
        nkpts = self.nkpts(path)
        kpointdat=self.grep_kpoint_procar(path,nkpts)
        kpoints = []
        if weight:
            for dat in kpointdat:
                kpoints.append(dat.split()[3:6].append(dat.split()[8]))
        else:
            for dat in kpointdat:
                kpoints.append(dat.split()[3:6])
        return np.array(kpoints,dtype=float)

    def _get_bands(self,path):
        nband = self.nbands(path)
        nkpts = self.nkpts(path)
        ispin = self.ispin(path)
        banddat = self.grep_band_procar(path)
        assert len(banddat) == ispin*nkpts*nband        
        bands = []
        band = []
        num = 1
        for line in banddat:
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
        return bands

    def _get_procar(self,path):
        nband = self.nbands(path)
        nkpts = self.nkpts(path)
        ispin = self.ispin(path)
        nions = self.nions(path)
        procardat = self.grep_procar(path,nions)
        procar = []
        for line in procardat:
            value = line.split()[1:]
            procar.append(value)
        if ispin == 1:
            assert len(procar) == nkpts*nband*(nions+1)
            procar = np.array(procar,dtype=float).reshape(1,nkpts,nband,nions+1,-1)
        elif ispin == 2:
            assert len(procar) == 2*nkpts*nband*(nions+1)
            procar = np.array(procar,dtype=float).reshape(2,nkpts,nband,nions+1,-1)
        return procar
        
