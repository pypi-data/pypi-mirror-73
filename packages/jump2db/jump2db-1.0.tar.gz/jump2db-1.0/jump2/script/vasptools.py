import os
import numpy as np


class __Vasptools():

    def __init__(self,*args,**kwargs):
        self.potdir = os.environ['HOME']+"/usr/paw_pbe/" 
        self.syspath = set()
        self.files = set()
        self.__potcar = False
        self.__standard = False
        self.__kpath = False
        self.__backup = False
        self.__clean = False
        self.__json = False

    def tasks(self,params):
        from os.path import exists,join,isfile
        for i in params:
            if i.lower() == 'potcar':
                self.__potcar = True
            elif i.lower() == 'kpath':
                self.__kpath = True
            elif i.lower() == 'standard':
                self.__standard = True
            elif i.lower() == 'backup':
                self.__backup = True
            elif i.lower() == 'clean':
                self.__clean = True
            elif i.lower() == 'json':
                self.__json = True
            else:
                for dir in self.syspath:
                    if isfile(join(dir,i)):
                        self.files.add((dir,i))

    def load_pool(self,poolfile):
        from os.path import join,isdir,isfile,dirname,abspath
        if isfile(poolfile):
            import pickle
            try:
                root = abspath(dirname(poolfile))
                with open(poolfile,'rb') as f:
                    pool=pickle.load(f)
                for dir in pool.keys():
                    if isfile(join(root,dir,'.status')):
                        self.syspath.add(join(root,dir))
            except:
                print('PathError: Invalid poolfile')

        elif isdir(poolfile):
            root = abspath(poolfile)
            if isfile(join(root,'.status')) or isfile(join(root,'POSCAR')):
                self.syspath.add(root)
            else:
                for dir in os.listdir(root):
                    if isfile(join(root,dir,'.status')) or isfile(join(root,dir,'POSCAR')):
                        self.syspath.add(join(root,dir))
                
        else:
            print('PathError: Invalid directory')


    def seek_structure(self):
        '''
        support filetype: poscar, contcar, .xyz, .vasp, .mol, .cif
        '''
        from jump2.structure import read
        structure_set = {}
        # seek from self.files %
        for path,filename in self.files:
            if filename.endswith('.cif'):
                ftype='cif'
            elif filename.endswith('.xyz'):
                ftype='xyz'
            elif filename.endswith('.mol'):
                ftype='mol'
            elif filename.endswith('.vasp'):
                ftype = 'poscar'
            elif 'CONTCAR' in os.path.basename(filename):
                ftype='poscar'
            elif 'POSCAR' in os.path.basename(filename):
                ftype='poscar'
            else:
                continue

            try: 
                file = os.path.join(path,filename)
                structure_set[file] = read(file,ftype)
            except:
                pass

        # try again: seek from self.syspath %
        if len(structure_set) == 0 and len(self.syspath) == 1:
            for filename in os.listdir(list(self.syspath)[0]):
                abspath = os.path.join(list(self.syspath)[0],filename)
                if filename.endswith('.cif'):
                    ftype='cif'
                elif filename.endswith('.xyz'):
                    ftype='xyz'
                elif filename.endswith('.mol'):
                    ftype='mol'
                elif filename.endswith('.vasp'):
                    ftype = 'poscar'
                elif os.path.isfile(abspath) and ('CONTCAR' in filename or 'POSCAR' in filename):
                    ftype='poscar'
                else:
                    continue
                
                try: 
                    structure_set[abspath] = read(abspath,ftype)
                except:
                    pass

        # raise Error % 
        if len(structure_set) == 0:
            raise ValueError("Seek structure files failed.") 

        return structure_set

    def run(self,params,**kwargs):
        ''' main project'''
        import time
        start =time.clock()

        # initialize path %
        self.syspath.add(os.getcwd())
        if 'pool' in params:
            self.load_pool(params['pool'])

        # update params %
        self.tasks(params['vasp_tools'])
        # run tasks %
        if self.__standard:
            self.standard()
        elif self.__potcar:
            self.write_potcar()
        elif self.__backup:
            self.backup()
        elif self.__kpath:
            self.kpath()
        elif self.__clean:
            self.clean()
        elif self.__json:
            self.incar2json()
        end = time.clock()
        print('Running time: %s Seconds'%(round(end-start,4)))

    def clean(self):
        from os.path import isfile,join

        def remove(root,files):
            num = 0
            for f in files:
                if f in ['INCAR','POSCAR','POTCAR','OPTCELL','KPOINTS']:
                    continue
                elif '.' in f and f.split('.')[-1] in ['x','py','dat','pbs']:
                    continue
                else:
                    num += 1
                    os.remove(join(root,f))
            return num

        while(True):
            in_content = input("Notice that you are deleting files. Type Y/N to continue: ")
            if in_content.lower()[0] == "y":
                break
            if in_content.lower()[0] == "n":
                return 0
            else:
                print("Invalid input. Please try again.")

        num = 0
        for path in self.syspath:
            if not isfile(join(path,'OUTCAR')) and not isfile(join(path,'.status')): 
                continue
            for root,dirs,files in os.walk(path):
                if 'OUTCAR' in files:
                    num += remove(root,files)
            
        print("clean finished. %s files were deleted" %num)

    def incar2json(self):
        import json

        incar_dict = {}
        for path,file in self.files:
            if 'incar' in file.lower():
                ip = os.path.join(path,file)
                incar_dict[ip] = self.incar2dict(ip)

        incar_json = json.dumps(incar_dict,indent=3)
        print(incar_json)

    def incar2dict(self,path):
        tmp_dict = {}
        with open(path,'r') as f:
            for line in f:
                if line.lstrip()[0] == "#":  continue
                label,value = line.split('=')[:2]
                tmp_dict[label.strip()] = value.strip()
        return tmp_dict
            

    def backup(self):
        import shutil

        if len(self.files) == 0:
            raise ValueError("Requires filename as an input parameter.")

        fdict = {}
        for path,filename in self.files:
            if filename not in fdict.keys():
                fdict[filename] = savedir = os.path.join(os.getcwd(),filename.replace('/','_'))
                if not os.path.exists(savedir):
                    os.makedirs(savedir)
            originfile = os.path.join(path,filename)
            copyfile = os.path.join(fdict[filename],os.path.basename(path)) 
            shutil.copyfile(originfile,copyfile)
            
        print("backup finished")

    def standard(self):

        from jump2.abtools.vasp.vaspio import VaspIO
        vaspio = VaspIO()
        # try read all possible structure models %
        structures = self.seek_structure()

        num = 0
        for p,v in structures.items():
            vaspio.write_poscar(v,p)
            num += 1
                
        print("standard successed : %s" %num)

    def kpath(self):
        # try read all possible structure models %
        structures = self.seek_structure()

        num = 0
        for p,v in structures.items():
            self.print_kpath(p,v)
            num += 1
                
        print("kpath successed : %s" %num)


    def write_potcar(self):
        # try read all possible structure models %
        structures = self.seek_structure()
        extradir = False
        num = 0

        if len(self.syspath) == 1 and len(structures) > 1:
            extradir = os.path.join(list(self.syspath)[0],'potcar')
            if not os.path.isdir(extradir):
                os.makedirs(extradir)
            print("Save potcar in %s" %extradir)

        for path,struct in structures.items():
            elements = struct.species_of_elements
            pot = []

            for e in elements:
                optional_pots =[i.rstrip() for i in os.popen("ls {0} | grep {1}".format(self.potdir,e)).readlines()]
                if len(optional_pots) > 0:
                    for add in ['_3','_2','','_sv','_pv','_d','_s','_h']:
                        if e+add in optional_pots:
                            pot.append(os.path.join(self.potdir, e+add, 'POTCAR'))
                            break
  
            assert len(pot) == len(elements)
            dir,file = os.path.split(path)
            if extradir:
                order = 'cat {0} > {1}'.format(' '.join(pot),os.path.join(extradir,file))
            else:
                order = 'cat {0} > {1}'.format(' '.join(pot),os.path.join(dir,'POTCAR'))
            os.popen(order)
            num += 1

        print("poscar successed : %s" %num)

    def print_kpath(self,path,structure):
        import numpy as np
        from jump2.abtools.brillouin_zone import HighSymmetryKpath
        from jump2.structure import read
        structure = read(path)
        bz = HighSymmetryKpath()
        kpoint = bz.get_HSKP(structure.bandStructure())
        kpath = {'all':[], 'suggest':[]}
        count = 0
        tmp = []
        for p in kpoint['Path']:
            if len(tmp) > 0 and sum([i-int(i) for i in (np.array(\
                          kpoint['Kpoints'][p[0]])+tmp)]) < 0.001:
                count -= 1
            for i in range(len(p)-1):
                k1 = '{0[0]:>16.8f} {0[1]:>16.8f} {0[2]:>16.8f} ! {1}'.format(\
                     kpoint['Kpoints'][p[i]], p[i])
 
                k2 = '{0[0]:>16.8f} {0[1]:>16.8f} {0[2]:>16.8f} ! {1}'.format(\
                     kpoint['Kpoints'][p[i+1]], p[i+1])
 
                A = p[i].strip('\\')
                B = p[i+1].strip('\\')
                string = r"{0}-{1}:{2}\n{3}".format(A,B,k1,k2)
                kpath['all'].append(string)
                if count == 0: kpath['suggest'].append(string)
                if 'Gamma' in p[i+1]: B = 'Gamma'
            tmp = np.array(kpoint['Kpoints'][p[-1]])
            count += 1
 
        if len(kpath['suggest']) >= 5:
            kpt_dict = kpath['suggest']
        else:
            kpt_dict = kpath['all']
 
        print(path,' SG: {0}({1})  PG: {2}'.format(bz.spacegroup,bz.sgnum,bz.pointgroup))
        for value in kpt_dict:
            print("\"%s\"," %value)

