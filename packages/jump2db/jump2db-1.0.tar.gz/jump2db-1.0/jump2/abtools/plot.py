import matplotlib 
matplotlib.use('agg')
import matplotlib.pyplot as plt
import jump2.abtools.globalvar as gl
import numpy as np
import os

# Updatp global variables %
LABEL = 20
TITLE = 25
LEGEND = 18
DOSEMIN = -4
DOSEMAX = 4
DOSLIMIT = 0.04
BANDEMIN = -2
BANDEMAX = 2
BANDDIR = 'bandplot'
DOSDIR = 'dosplot'
colormap=['g','b','y','m','orange','c','cyan','yellow','violet','brown',\
          'lime','deepskyblue','gold','darkorchid','greenyellow','r']
if __name__ != '__main__':
    LABEL = gl.get('LABEL')
    TITLE = gl.get('TITLE')
    LEGEND = gl.get('LEGEND')
    DOSEMIN = gl.get('DOSEMIN')
    DOSEMAX = gl.get('DOSEMAX')
    DOSLIMIT = gl.get('DOSLIMIT')
    BANDEMIN = gl.get('BANDEMIN')
    BANDEMAX = gl.get('BANDEMAX')

class Jump2plot(object):
    def init(self):
        self.__path = None

    @property
    def kpath(self):
        return getattr(self,'_kpath',None)

    @kpath.setter
    def kpath(self,value):
        if isinstance(value,tuple):
            self._kpath = value
        else:
            raise TypeError("'tuple' type need by kpath in Jump2plot Class")
     

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self,value=None):
        from os.path import exists,join,isdir
        plotpath = []
        if exists(value) and isdir(value):
            if exists(join(value,'.status')):
                plotpath.append(value)
            else:
                for dir in os.listdir(value):
                    if exists(join(value,dir,'.status')):
                        plotpath.append(join(value,dir))
        else:
            print('PathError: Invalid directory')

        if len(plotpath) == 0:
            if exists(join(value,'OUTCAR')):
                plotpath.append(value)
            else:
                for dir in os.listdir(value):
                    if exists(join(value,dir,'OUTCAR')):
                        plotpath.append(join(value,dir))
        print(plotpath)
        self.__path = plotpath 

    def set_color(self,number=0):
        def colors(i):
            while True:
                yield colormap[i]
                i+=1
        return colors(number)

    def figure(self,type='simple'):
        if type == 'simple':
            fig = plt.figure(figsize=(12,12),dpi=100)
        elif type == 'band':
            fig = plt.figure(figsize=(12,12),dpi=100)
            plt.tick_params(labelsize=LABEL)
            plt.axhline(linewidth=2.2,color='r',linestyle='--')
            plt.xticks([])
            plt.ylim(BANDEMIN,BANDEMAX)
        elif type == 'dos':
            fig = plt.figure(figsize=(12,6),dpi=100)
            plt.tick_params(labelsize=LABEL)
            plt.axvline(linewidth=2.2,color='r',linestyle='--')
            plt.xlabel("Energy (ev)",fontsize=TITLE)
            plt.ylabel(u'$PDOS\ (states/eV/\AA^{3})$', fontsize=TITLE)
            plt.xlim(DOSEMIN,DOSEMAX)
            plt.ylim(0,DOSLIMIT)

        return fig

    def plotfatband(self):
        self.plotband(type='fatband')

    def plotband(self,type=None):
        from os.path import basename,exists
        success = 0
        errors = []
        # assert path or paths %
        if len(self.path) == 0:
            print('No valid band-calculation from input')
        elif len(self.path) == 1:
            rootdir = os.getcwd() 
        else:
            rootdir = BANDDIR
            if not exists(rootdir):
                os.makedirs(rootdir)
        
        # start plot %
        for dir in self.path:
            if type == 'fatband':
                status = self.plot_fat_band(dir) 
            else:
                status = self.plot_band(dir)
            if status:
                plt.tight_layout()
                plt.savefig(rootdir+'/'+basename(dir)+'.png')
                plt.close()
                success += 1
            #except:
            #    errors.append(dir)

        # statistics %
        print('success band-plot: %s' %success)
        #if len(errors) > 0 :
        #    print('plot failed in next dirs:')
        #    print('  '+ '\n'.join(errors))

    def plot_fat_band(self,path):
        '''
        plot band-figure base on PROCAR
        '''
        from jump2.abtools.grep import Jump2band
        jb = Jump2band.fatband(path,kpath=self.kpath)
        print(jb.__class__)
        fig = self.figure('band')
        color = self.set_color()

        # grep main datas %
        bands=jb.get_bands() 
        procar,info,label=jb.get_pmax_procar()
        kpath=jb.plot_kpath() 
        if hasattr(jb,'scfdir') and os.path.exists(jb.scfdir):
            rec_vector = jb.reciprocal_lattice_vectors(jb.scfdir)
            kpoints,nkpt = jb.get_kpoints(isnkpt=True)
        else:
            rec_vector = jb.reciprocal_lattice_vectors(jb.stdin)
            kpoints,nkpt = jb.get_kpoints(isnkpt=True)

        # create colormap and legend%
        c1 = next(color)
        colormap = np.zeros(len(label),dtype=str)
        linemap = []
        for i in range(len(label)):
            c = next(color)
            colormap[i]=c 
            if np.sum(info == i) > nkpt:
                pl,=plt.plot([0,1],[0,1],c=c,label=label[i])
                linemap.append(pl)
        plt.legend(fontsize=LEGEND,loc=1)
        for line in linemap:
            line.remove()

        # set x axis % 
        xkpt=[0]
        for i in range(1,len(kpoints)):
            delta=np.linalg.norm(np.dot(rec_vector,kpoints[i]-kpoints[i-1]))
            if i%nkpt == 0 :
                plt.axvline(xkpt[i-1],c='black')
                delta=0
            xkpt.append(delta+xkpt[-1])
        xkpt=np.array(xkpt)

        # plot kpoint symbols %
        for i in range(len(kpath)):
            if i == 0:
                plt.text(xkpt[0],BANDEMIN*1.01,kpath[i],ha='center',va='top',fontsize=LABEL)
            else:
                plt.text(xkpt[i*nkpt-1],BANDEMIN*1.01,kpath[i],ha='center',va='top',fontsize=LABEL)

        # plot band.png %
        cv = jb.get_cbmvbm(bands)
        for i,bands_ispin in enumerate(bands):
            if 'nogap' in cv and cv['nogap'] == True:
                ybands=bands_ispin[...,0]-self.get_fermi()
            else:
                ybands=bands_ispin[...,0]-cv['vbm']['energy']
            plt.plot(xkpt,ybands,c=c1)
            for nband in range(len(ybands[0])):
                plt.scatter(xkpt,ybands[:,nband],color=colormap[info[i,:,nband]])

        # add bandgap %
        if 'nogap' not in cv:
             xvbm = xkpt[cv['vbm']['id']]
             xcbm = xkpt[cv['cbm']['id']]
             Ecbm = cv['cbm']['energy']-cv['vbm']['energy']
             plt.plot([max(0,xcbm-xkpt[-1]/100),min(xkpt[-1],xcbm+xkpt[-1]/100)],[Ecbm,Ecbm],color='r') 
             plt.plot([xcbm,xcbm],[0,Ecbm],c='r',lw=2)
             xtext=[xcbm+xkpt[-1]/100,xcbm-xkpt[-1]/6][xcbm>xkpt[-1]*2/3]
             plt.text(xtext,Ecbm/2,'{:.3f} eV'.format(Ecbm),fontsize=LEGEND)

        plt.xlim(0,xkpt[-1])
        plt.tight_layout()
        return True

    def plot_band(self,path):
        '''
        plot band-figure base on OUTCAR
        '''
        # Initializes the data retrieval module & pyplot & colormap %
        from jump2.abtools.grep import Jump2band
        jb = Jump2band(path,kpath=self.kpath)
        print(jb.__class__)
        print(jb.kpath)
        fig = self.figure('band')
        color = self.set_color()

        # grep main datas %
        bands=jb.get_bands() 
        kpath=jb.plot_kpath() 
        if hasattr(jb,'scfdir') and os.path.exists(jb.scfdir):
            rec_vector = jb.reciprocal_lattice_vectors(jb.scfdir)
            kpoints,nkpt = jb.get_kpoints(isnkpt=True)
        else:
            rec_vector = jb.reciprocal_lattice_vectors(jb.stdin)
            kpoints,nkpt = jb.get_kpoints(isnkpt=True)

        print(nkpt)
        # set x axis % 
        xkpt=[0]
        for i in range(1,len(kpoints)):
            delta=np.linalg.norm(np.dot(rec_vector,kpoints[i]-kpoints[i-1]))
            if i%nkpt == 0 :
                plt.axvline(xkpt[i-1],c='black')
                delta=0
            xkpt.append(delta+xkpt[-1])
        xkpt=np.array(xkpt)

        # plot kpoint symbols %
        for i in range(len(kpath)):
            if i == 0:
                plt.text(xkpt[0],BANDEMIN*1.01,kpath[i],ha='center',va='top',fontsize=LABEL)
            else:
                plt.text(xkpt[i*nkpt-1],BANDEMIN*1.01,kpath[i],ha='center',va='top',fontsize=LABEL)

        # plot band.png %
        cv = jb.get_cbmvbm(bands)
        for bands_ispin in bands:
            c = next(color)
            if 'nogap' in cv and cv['nogap'] == True:
                ybands=bands_ispin[...,0]-jb.get_fermi()
            else:
                ybands=bands_ispin[...,0]-cv['vbm']['energy']
            plt.plot(xkpt,ybands,c=c)
        # add bandgap %
        if 'nogap' not in cv:
            xvbm = xkpt[cv['vbm']['id']]
            xcbm = xkpt[cv['cbm']['id']]
            Ecbm = cv['cbm']['energy']-cv['vbm']['energy']
            plt.scatter([xvbm],[0],color='r',s=40)
            plt.plot([max(0,xcbm-xkpt[-1]/100),min(xkpt[-1],xcbm+xkpt[-1]/100)],[Ecbm,Ecbm],color='r') 
            plt.plot([xcbm,xcbm],[0,Ecbm],c='r',lw=2)
            xtext=[xcbm+xkpt[-1]/100,xcbm-xkpt[-1]/6][xcbm>xkpt[-1]*2/3]
            plt.text(xtext,Ecbm/2,'{:.3f} eV'.format(Ecbm),fontsize=LEGEND)

        plt.xlim(0,xkpt[-1])
        plt.tight_layout()
        return True

    def plotdos(self):
        from os.path import basename,exists
        success = 0
        errors = []
        # assert path or paths %
        if len(self.path) == 0:
            print('No valid dos-calculation from input')
        elif len(self.path) == 1:
            rootdir = os.getcwd() 
        else:
            rootdir = DOSDIR
            if not exists(rootdir):
                os.makedirs(rootdir)
        
        # start plot %
        for dir in self.path:
            try:
                status = self.plot_dos(dir)
                if status:
                    plt.tight_layout()
                    plt.savefig(rootdir+'/'+basename(dir)+'.png')
                    plt.close()
                    success += 1
            except:
                errors.append(dir)

        # statistics %
        print('success dos-plot: %s' %success)
        if len(errors) > 0 :
            print('plot failed in next dirs:')
            print('  '+ '\n'.join(errors))

    def plot_dos(self,path=None,rotate=False):
        from jump2.abtools.grep import Jump2dos
        jd = Jump2dos(path)
        fig = self.figure('dos')
        color = self.set_color()
        dos_energy,dos=jd.get_dos()
        # initial plt setting %
        volume = jd.volume(jd.stdin)
        atominfo  = jd.atominfo(jd.stdin)
#        linestyles={'s':':','p':'-','d':'--','f':'-.'}
        imin,imax = sum(dos_energy<DOSEMIN),sum(dos_energy<DOSEMAX)

        # plot %
        tmp = 0
        for element,num in atominfo:
            dos_atom=np.sum(dos[tmp:tmp+num],axis=0)
            tmp += num
            if jd.spin == 1:
                doslimit = 0
                dos_data=dos_atom
                for k in range(3):
                    if max(dos_data[k][imin:imax]/volume) < 0.003:continue
                    label=element+'-'+jd.orbits[k]
                    if rotate:
                        y,x=dos_energy,dos_data[k]/volume
                    else:
                        x,y=dos_energy,dos_data[k]/volume
                    plt.plot(x,y,linewidth=2.2,label=label)#,linestyle=linestyles[orbits[k]],label=label,c=next(color))
            elif jd.spin == 2:
                doslimit = -DOSLIMIT
                spin=['up','down']
                plt.axhline(linewidth=1, color='black', linestyle='--')
                for s,dos_data in zip(spin,dos_atom):
                    for k in range(len(jd.orbits)):
                        if max(abs(dos_data[k][imin:imax]/volume)) < 0.003:continue
                        label=element+'-'+self.orbits[k]+'-'+s
                        if rotate:
                            y,x=dos_energy,dos_data[k]/volume
                        else:
                            x,y=dos_energy,dos_data[k]/volume
                        plt.plot(x,y,linewidth=2.2,label=label)#,linestyle=linestyles[orbits[k]],label=label,c=next(color))
        plt.legend(fontsize=LEGEND,loc=1)
        return True

if __name__ == '__main__':
    a = Jump2plot()
    a.path = os.getcwd()
    a.plotfatband()
    #a.plotdos()
                
        
