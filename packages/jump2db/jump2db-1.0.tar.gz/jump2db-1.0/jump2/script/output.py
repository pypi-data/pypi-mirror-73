import os
import numpy as np
from jump2.abtools.grep import GrepOutcar


__task_dict__ = {'dielectric':('dielectric','dielectric_ionic'),
                 'cbvb':('bandgap','vbm-kpoint','cbm-kpoint'),
                 'bandgap':('bandgap','isdirect'),
                 'emass':('cb-emass','vb-emass')}

class __OutputData(GrepOutcar):

    def __init__(self,*args,**kwargs):
        self.__plot = False
        self.__csv = False
        self.__sort = False
        self.__form = False
        self.__path = None

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self,value=None):
        from os.path import exists,join,isdir,isfile,dirname
        paths = []
        if exists(value) and isdir(value):
            if exists(join(value,'.status')):
                paths.append(value)
            elif exists(join(value,'OUTCAR')):
                paths.append(value)
            else:
                for dir in os.listdir(value):
                    if exists(join(value,dir,'.status')):
                        paths.append(join(value,dir))
        elif isfile(value):
            import pickle
            try:
                root = dirname(value)
                with open(value,'rb') as f:
                    pool=pickle.load(f)
                for dir in pool.keys():
                    if exists(join(root,dir,'.status')):
                        paths.append(join(root,dir))
            except:
                print('PathError: Invalid poolfile')
                
        else:
            print('PathError: Invalid directory')
        self.__path = paths
        print('Total = %s' %len(paths))

    def set_params(self,params=None):
        self.tasks = []
        for i in params:
            if i == 'plot':
                self.__plot = True
            elif i == 'csv':
                self.__csv = True
            elif i == 'sort':
                self.__sort = True
            elif i == 'form':
                self.__form = True
            else:
                self.tasks.append(i)

    def run(self,params,path=None,**kwargs):
        # update params %
        self.set_params(params['output'])
        if 'pool' in params:
            self.path = params['pool']
        elif path == None:
            self.path = os.getcwd()
        elif os.path.exists(path):
            self.path = path
        else:
            print('Warning! Invalid input path')

        # load datas %
        if len(self.tasks):
            dataset = self.getdatas()
        else:
            print('Warning! No vaild task was found')

        # run main_project %
        if self.__plot:
            self.plot(dataset)
        if self.__csv:
            self.csv(dataset)
        elif self.__sort:
            self.sort(dataset)
        elif self.__plot is False or self.__form:
            self.form(dataset)

    def getdatas(self):
        dataset = {}
        for task in self.tasks:
            # check whether vaild task %
            state = self.find_task_belong(task)

            # Invaild task %
            if state == 0:
                print('Invaild_task: %s' %task)
                continue
        
            # Vaild task %
            dat = []
            success = 0
            func = getattr(self,task)
            # run all path %
            for path in self.path:
                try:
                    scfdir = os.path.join(path,'scf')
                    # GrepOutcar moudle %
                    if state == 2 and os.path.exists(scfdir)  :
                        dat.append(func(scfdir))
                    # local moudle %
                    else:
                        dat.append(func(path))
                    success+=1
                except:
                    print('IOError: read %s task-%s failed' %(path,task))
                    dat.append(None) 
                
            # conclusion %
            print('%s success = %d' %(task,success))
            if state == 1:
                labels = __task_dict__[task]
                for j,label in enumerate(labels): 
                    dataset[label] = []
                for i,v in enumerate(dat):
                    if v is None:
                        for j,label in enumerate(labels):  dataset[label].append(np.nan)
                    elif isinstance(v,tuple):
                        assert len(v) == len(labels)
                        for j,label in enumerate(labels):  dataset[label].append(v[j])
            elif state == 2:
                 dataset[task] = dat

        return dataset

    def find_task_belong(self, meth_name):
        '''check whether task belong to main_class or sub_class
           return 0 : Invalid task
           return 1 : belong to main_class, path use main_director
           return 2 : belong to sub_class, path use stdin/scf'''

        for ty in type(self).mro():
            if meth_name in ty.__dict__:
                if ty == type(self):
                    return 1
                else:
                    return 2
        return 0 

            
    def dielectric(self,path):
        '''dielectric dielectric_ionic'''
        from jump2.abtools.grep import Jump2optic
        jp = Jump2optic(path)
        diel_e = jp.get_dielectric()
        diel_ion = jp.get_dielectric_ionic()
        return diel_e,diel_ion

    def cbvb(self,path):
        '''cbvb data'''
        from jump2.abtools.grep import Jump2band
        jp = Jump2band(path)
        cbmvbm = jp.get_cbmvbm()
        bandgap = np.around(cbmvbm['cbm']['energy'] - cbmvbm['vbm']['energy'],4)
        cbm_kpoint = '{0[0]}, {0[1]}, {0[2]}'.format(cbmvbm['cbm']['kpoint'])
        vbm_kpoint = '{0[0]}, {0[1]}, {0[2]}'.format(cbmvbm['vbm']['kpoint'])
        return bandgap,cbm_kpoint,vbm_kpoint

    def bandgap(self,path):
        '''bandgap isdirect'''
        from jump2.abtools.grep import Jump2band
        jp = Jump2band(path)
        return jp.get_bandgap()

    def emass(self,path):
        '''cb-emass vb-emass'''
        from jump2.abtools.grep import Jump2band
        jp = Jump2band(path)
        emass = jp.get_emass()
        cbm_emass = np.around(np.cbrt(emass['cbm-x']*emass['cbm-y']*emass['cbm-z']),3)
        vbm_emass = np.around(np.cbrt(emass['vbm-x']*emass['vbm-y']*emass['vbm-z']),3)
        return cbm_emass,vbm_emass

    def csv(self,dataset):
        from os.path import split
        if len(self.path) > 1:
            filename = split(split(self.path[0])[0])[-1]+'.csv'
        else:
            filename = split(self.path[0])[-1]+'.csv'
        dat = np.stack(dataset.values(),axis=1).astype(str)
        with open(filename,'w') as f:
            f.write('path,'+','.join(dataset.keys())+'\n')
            for i,path in enumerate(self.path):
                f.write(split(path)[-1]+','+','.join(dat[i])+'\n')

    def plot(self,dataset):
        '''
        simple plot model 
        plot up to 2 properties
        x-axis is sorted-index, only plot datas not None 
        if index <= 10 , x_params is path
        else, plot hist
        '''
        from os.path import split
        import matplotlib
        matplotlib.use('agg')
        import matplotlib.pyplot as plt
        import pandas as pd
        path = np.array([split(p)[-1] for p in self.path])
        # task 1 %
        task = dataset.keys()[0]
        index = np.where(~pd.isna(dataset[task]))
        xlen = len(index[0])
        if xlen > 10:
            pass
        elif xlen <= 10 and xlen > 0:
            fig,ax1=plt.subplots(figsize=(6,6))
            plt.figure(figsize=(6,6))
            plt.plot(range(xlen),np.array(dataset[task])[index],'o',c='b')
            plt.xticks(range(xlen),path[index],rotation=30)
        # task 2 %
        if len(dataset.keys()) > 1:
            task = dataset.keys()[1]
            index = np.where(~pd.isna(dataset[task]))
            xlen = len(index[0])
            if xlen > 10:
                pass
            elif xlen <= 10 and xlen > 0:
                ax2 = ax1.twinx()
                plt.plot(range(xlen),np.array(dataset[task])[index],'^',c='orange')
                plt.xticks(range(xlen),path[index],rotation=30)
        plt.savefig('output.png')           

    def sort(self,dataset):
        from os.path import split
        def title(task):
            print('\n+'+'-'*(len(task)+12)+'+')
            print('| Property: %s |' %task)
            print('+'+'-'*(len(task)+12)+'+')

        for task in dataset.keys():
            title(task)
            for i,v in zip(np.argsort(dataset[task]),np.sort(dataset[task])):
                print(' %s, %s' %(split(self.path[i])[-1],v))

    def form(self,dataset):
        import pandas as pd
        from os.path import split
        # init lists %
        timingInfo = []
        keyHeader = ['path']
        keyMaxLen = {'path':4}
        for key in dataset.keys():
            keyHeader.append(key)
            keyMaxLen[key] = len(key)
        for i,path in enumerate(self.path):
            p = split(path)[-1]
            tmp = {'path':p}
            keyMaxLen['path'] = max(keyMaxLen['path'],len(p))
            for task in dataset.keys():
                v = dataset[task][i]
                if pd.isna(v): 
                    tmp[task] = '--'
                    keyMaxLen[task] = max(keyMaxLen[task],2)
                else:
                    tmp[task] = str(v)
                    keyMaxLen[task] = max(keyMaxLen[task],len(str(v)))
            timingInfo.append(tmp)
        del dataset

        def printGroup(group):
            for item in group:
                for i,h in enumerate(keyHeader):
                    itemLen = keyMaxLen.get(h, str(h)) + 4
                    s = str(item[h]).center(itemLen, '-' if item[h] == '-' else ' ')

                    icon = '|'
                    if item[h] == '-':
                        icon = '+'

                    s = (icon if i == 0 else '') + s[1:len(s)] + icon
                    print(s,end='')
                print('')

        tag = {}
        for i,h in enumerate(keyHeader):
            tag[h] = '-'
        timingInfo.insert(0, tag)
        timingInfo.append(tag)
        printGroup([tag])

        for i,h in enumerate(keyHeader):
            itemLen = keyMaxLen.get(h, str(h)) + 4
            s = h.center(itemLen)
            s = ('|' if i == 0 else '') + s[1:len(s)] + '|'
            print(s,end='')
        print('')

        printGroup(timingInfo)
