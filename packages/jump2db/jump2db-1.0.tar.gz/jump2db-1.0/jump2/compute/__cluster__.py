import os

class __Script__(object):

    def __init__(self,root=None, params=None,  *args, **kwargs):

        self.name = 'JUMP2.pbs' 
        self.__parses = None
        self.__load__(root,params)


    def __load__(self,root=None,model='sub',params=None):
        '''
        load cluster configuration
        params:
        root: correct calculation path
        model: loadtype
            sub: config from correct path, ./.cluster
            default: config from jump2env path, ~/.jump2
        params: update config params
        '''
        from os.path import exists, join, expanduser
        import json
        # set configuration path & model %
        if model == 'default':
            cluster = join(os.environ['HOME'],'.jump2/env/pbs.json')
        elif root and exists(join(root,'.cluster')):
            cluster = join(root,'.cluster')
        else:
            model == 'default'
            cluster = join(expanduser('~'),'.jump2/env/pbs.json')
            print('Model changed. File %s not exists!' %model)
       
        # load configuration file% 
        try:
            with open(cluster,'r')  as f:
                self.__parses = json.load(f)
        except:
            if model != 'default':
                os.system('mv {0} {0}.error '.format(cluster))
                print('Warning! Please check the json format is correct!')
                return self.__load__(model='default',params=params)
            else:
                raise IOError('Warning! Invalid default cluster configuration.')

        # update parameter %
        if params:        
            self.__parses.update(params)

    def __dump__(self, root=None, params={}):
        import json
        from copy import deepcopy

        path = os.path.join(root,'.cluster')
        json_dict = deepcopy(self.__parses)
        json_dict.update(params)
        with open(path,'w') as f:
            f.write(json.dumps(json_dict,indent = 3))
        del json_dict

    def submit(self, pool=None, outdir=None, overwrite=False):
	
        self.__script(pool, outdir) 
        #self.index = os.popen(self.cmd+'subscript | tail -1').readline()
        self.index = os.popen(self.cmd+'pbsscript | tail -1').readline()

    @property
    def index(self):
        return self.__id 

    @index.setter
    def index(self, value=None):
        import re
        self.__id = re.findall(r'\d+', value)
    
    def __script(self, name, outdir):

        from os.path import dirname 
        from jump2 import compute

        try:
            hostname = os.environ['HOSTNAME'] 
            username = os.environ['USER']
        except:
            raise IOError ('Please set the hostname and username')	
        script = dirname(compute.__file__)

        with open('pbsscript', 'w') as f:
            if self.__parses['manager'] == 'PBS':	
                f.write('#!/bin/bash --login\n')
                f.write('#PBS -N {0}\n'.format(self.name))
                f.write('#PBS -q {0}\n'.format(self.queue))
                if self.project is not None:
                    f.write('#PBS -A {0}\n'.format(self.project))
                f.write('#PBS -l nodes={0}:ppn={1}\n'.format(self.nodes,self.cores))
                #if self.cores is not None:
                #    f.write('#PBS -l ppn={0}\n'.format(self.cores))
                if self.feature is not None:
                    f.write('#PBS -l feature={0}\n'.format(self.feature))
                f.write('#PBS -l walltime={0}\n'.format(self.walltime))
                f.write('#PBS -e .error\n')
                f.write('#PBS -o .output\n')
                f.write('\n')

                for line in self.env:
                    f.write(line+'\n')
                f.write('\n')
	        
                f.write('cd $PBS_O_WORKDIR\n')	
                f.write('python {0}/manager.py {1} {2} {3} {4} >.running\n'.format(script,name,outdir, hostname, username))
                f.write('\n')  		

            elif self.__parses['manager'] == 'LSF':	
                f.write('#!/usr/bin/bash\n')
                f.write('#BSUB -q {0}\n'.format(self.queue))
                f.write('#BSUB -app {0}\n'.format(self.app))
                f.write('#BSUB -a {0}\n'.format(self.lsfmpi))
                f.write('#BSUB -J {0}\n'.format(self.name))
                f.write('#BSUB -n {0}\n'.format(self.nodes*self.cores))
                f.write('#BSUB -R "span[ptile={0}]" -R "cu[usablecuslots={0}]"\n'.format(self.cores))
                f.write('#BSUB -e .error\n')
                f.write('#BSUB -o .output\n')
                f.write('\n')

                for line in self.env:
                    f.write(line+'\n')
                f.write('\n')
	        
                f.write('python {0}/manager.py {1} {2} {3} {4} >.running\n'.format(script,name,outdir, hostname, username))
                f.write('\n')  		

            elif self.__parses['manager'] == 'SLURM':	
                f.write('#!/bin/bash -l\n')
                f.write('#SBATCH --output=.running\n')
                f.write('#SBATCH -J {0}\n'.format(self.name))
                f.write('#SBATCH -p {0}\n'.format(self.queue))
                if self.project is not None:
                    f.write('#SBATCH -A {0}\n'.format(self.project))
                f.write('#SBATCH -N {0}\n'.format(self.nodes))
                if self.gpu is not None:
                    f.write("#SBATCH --gres=gpu:{0}\n".format(self.gpu))
                if self.cores is not None:
                    f.write('#SBATCH --ntasks-per-node={0}\n'.format(self.cores))
                f.write('#SBATCH -t {0}\n\n'.format(self.walltime))

                if self.env is not None:
                    f.write('{0}\n\n'.format(self.env))
                
                f.write('python {0}/manager.py {1} {2} {3} {4}>.running\n'.format(script,name,outdir, hostname, username))
        	#f.write('jump2 --single {0} --overwrite={0}\n'.format(path))
        	#f.write('jump2 -r qsub -f {0} --num=1\n'.format('test'))


    @property
    def walltime(self):
        return self.__parses['walltime']
    @property 
    def queue(self):
        return self.__parses['queue']
    @property
    def mpi(self):
        return self.__parses['mpi']   
    @property
    def cores(self):
        return self.__parses['cores']
    @property 
    def nodes(self):
        return self.__parses['nodes']
    @property
    def account(self):
        return self.__parses['account']
    @property
    def cmd(self):
        return self.__parses['cmd']  
    @property
    def app(self):
        return self.__parses['app']  
    @property
    def lsfmpi(self):
        return self.__parses['lsfmpi']  
    
    @property
    def feature(self):
        if 'feature' in self.__parses:
            return self.__parses['feature']
        else: return None
    @property
    def project(self):
        if 'project' in self.__parses:
            return self.__parses['project']
        else:
            return None  
    @property
    def env(self):
        if 'env' in self.__parses:
            return self.__parses['env']
        else:
            return None  
    @property
    def gpu(self):
        if 'gnu' in self.__parses:
            return self.__parses['gpu'] 
        else:
            return None  

    @property
    def restart(self):
        if 'restart' in self.__parses:
            return self.__parses['restart'] 
        else:
            return False 
    @restart.setter
    def restart(self,value):
        if isinstance(value,bool):
            self.__parses['restart'] = value

    @property
    def overwrite(self):
        if 'overwrite' in self.__parses:
            return self.__parses['overwrite'] 
        else:
            return False 
    @overwrite.setter
    def overwrite(self,value):
        if isinstance(value,bool):
            self.__parses['overwrite'] = value

    @property
    def maximum(self):
        if 'maximum' in self.__parses:
            return self.__parses['maximum'] 
        else:
            self.__parses['maxinum'] = 10
            return 10 
    @maximum.setter
    def maximum(self,value):
        if isinstance(value,int):
            self.__parses['maximum'] = value
       

#class Resource(ClusterPBS):
#
#    def __init__(self, *args, **kwargs):
#        
#        super(Resource, self).__init__()
#
#    def resource(self):
#
#        path = self.stdin
#
#from .. import TaskManger
#
#class AutoQueue(TaskManger):
#    
#    def __init__(self,queue=None, **kwargs):
#     
#         if queue is None:
#             self.__auto_select_queue()
#
#    def __auto_select_queue(self):
#        
#         return self.queue 
#     
