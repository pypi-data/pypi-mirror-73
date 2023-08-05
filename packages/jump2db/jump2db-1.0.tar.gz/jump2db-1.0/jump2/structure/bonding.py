import numpy as np

class BondAtom(object):
   
    def __init__(self,kernel,atoms,lengths):
        self.kernel = kernel
        self.bonding_atom = atoms
        self.bonding_length = lengths

    def get_bondlen(self,value):
        if value == 'mean':
            return self.meanbond
        elif value == 'min':
            return self.minbond

    def __repr__(self):
        return self.bonding_print

    @property
    def minbond(self):
        return np.min(self.bonding_length)

    @property
    def meanbond(self):
        return np.mean(self.bonding_length)

    @property
    def environment(self):
        env = {}
        for atom in self.bonding_atom:
            if atom not in env:
                env[atom] = 1
            else :
                env[atom] += 1
        envstr = ''
        for atom in np.sort(env.keys()):
            if env[atom] >1:
                envstr = envstr+atom+str(env[atom])
            else:
                envstr += atom
        return envstr

    @property
    def bonding_print(self):
        prints = []
        prints.append('\nAtom:{0}  num:{1}  '.format(self.kernel,len(self.bonding_length)))
        for i,atom in enumerate(self.bonding_atom):
            prints.append('{0} : {1:.4f}'.format(atom,self.bonding_length[i]))
        return ' '.join(prints)

class Bonding(object):

    def __init__(self,dataset,name='POSCAR',**kwargs):
        self.name = name
        self.bondenv = dataset

    def get_env(self,bondtype='mean',kernel=[]):
        env = {}
        bond = {}
        for atom in self.bondenv:
            if kernel and atom.kernel not in kernel: continue
            key = atom.kernel+'-'+atom.environment
            if key not in env:
                env[key] = 1
                bond[key] = atom.get_bondlen(bondtype)
            else:
                env[key] += 1
                if bondtype == 'mean':
                    bond[key] = (bond[key]+atom.meanbond)/2
                elif bondtype == 'min':
                    bond[key] = np.min(bond[key],atom.minbond)

        envstr = [self.name]
        for key in env.keys():
            envstr.append('{0} : num = {1}  {2}bond = {3:.4f}'.format(key,env[key],bondtype,bond[key]))
        return '\n'.join(envstr)

    def __repr__(self):
        return self.get_env()

class Bonding_without_kernel(object):

    def __init__(self,dataset,orient,otype='orient',name='POSCAR',**kwargs):
        self.name = name
        self.type = otype
        self.orient = orient
        self.bondenv = dataset

    def get_env(self,bondtype='mean',kernel=[]):
        env = {}
        bond = {}
        for atom1,atom2,length in self.bondenv:
            if kernel and atom1 not in kernel: continue
            key = atom1+'-'+atom2
            if key not in env:
                env[key] = 1
                bond[key] = [length]
            else:
                env[key] += 1
                bond[key].append(length)

        for key in bond.keys():
            if bondtype == 'mean':
                bond[key] = np.mean(bond[key])
            elif bondtype == 'min':
                bond[key] = np.min(bond[key])

        envstr = [self.name+'-'+self.type]
        envstr.append('{1} : [{0[0]:.3f},{0[1]:.3f},{0[2]:.3f}]'.format(self.orient,self.type))
        for key in env.keys():
            envstr.append('{0} : num = {1}  {2}bond = {3:.4f}'.format(key,env[key],bondtype,bond[key]))
        return '\n'.join(envstr)

    def __repr__(self):
        return self.get_env()

