import os
from .vaspflow import VaspFlow

class CorrectingFlow(VaspFlow):

    def __init__(self,root):
        from jump2.compute.__cluster__ import __Script__
        from os.path import dirname,abspath
        self.rootdir = abspath(root)
        self.cluster = __Script__(dirname(dirname(self.rootdir))) 

    def calculator(self, error, vasp, stdout, stdin=None, origin_incar={}, **kwargs):

        from jump2.structure import read
        from os.path import exists,join,getsize
        from .check import CheckStatus
        from .tasks import VaspIncar
        from copy import deepcopy
        import shutil
        import json

        # continue calcultions %
        check = CheckStatus()
        stdin = check.discrete(stdin,stdout)
        self.origin_stdout = stdout
        vasp = deepcopy(vasp)

        # get_correct_params %
        incar = VaspIncar('debug',self.analysis(error, stdin))
        incar.downdate(origin_incar)

        # makedirs %
        debug_root = join(self.rootdir,'debug')
        stdout = join(self.rootdir,'debug','tmp')
        if not exists(debug_root): os.makedirs(debug_root)
        if not exists(stdout): os.makedirs(stdout)

        #if stdin is not None:
        if stdin != None :
                
            # POSCAR update %
            try:
                vasp.structure = read(join(stdin,'CONTCAR'))
            except:
                try:
                    vasp.structure = read(join(stdin,'POSCAR'))
                except:
                    pass

            # copy chgcar %
            if exists(join(stdin,'CHGCAR')) and getsize(join(stdin,'CHGCAR')):
                if 'icharg' not in incar:
                    incar['icharg'] = 1
                elif incar['icharg'] == 11:
                    raise IOError('CHGCAR not exists!')
            else:
                incar['icharg'] = 2

            if incar['icharg'] == 1 or incar['icharg'] == 11:
                shutil.copyfile(join(stdin,'CHGCAR'),join(stdout,'CHGCAR'))
                shutil.copyfile(join(stdin,'CHG'),join(stdout,'CHG'))

            # copy wavecar %
            if exists(join(stdin,'WAVECAR')) and getsize(join(stdin,'WAVECAR')):
                if 'istart' not in incar:
                    incar['istart'] = 1
            else:
                incar['istart'] = 0

            if incar['istart'] == 1:
                shutil.copyfile(join(stdin,'WAVECAR'),join(stdout,'WAVECAR'))


        vasp.set_input(vasp.structure, stdout, True, incar)

        # update vasp program %
        if isinstance(vasp.program, dict):
            if 'lsorbit' in incar or'LSORBIT' in incar:
                program = vasp.program['nolinear']
            else:
                program = vasp.program['standard']
        else:
            program = vasp.program

        self.run(stdout, program=program)
        return stdout,incar

    def analysis(self, error, stdin):
        import re
        import json
        from os.path import join
        from jump2.abtools.grep import Jump2grep
        from .monitor import Writelog 

        # get_tasktype %
        if stdin is not None:
            jg = Jump2grep(stdin)

        # read_error_params from error.json %
        debug_json = join(os.environ['HOME'],'.jump2','env','error.json')
        with open(debug_json,'r') as f: 
            debug_set = json.load(f)
        params = debug_set[error][1]

        # hopeless %
        if len(params) == 0:
            status = os.popen('lsof {}|grep mpirun'.format(join(self.origin_stdout,'pbs.log'))).readline()
            if status:
                os.popen('kill %s' %status.split()[1])  
            Writelog('Error!','killed program for error %s' %error)
            os._exit(0)

        # analysis_error_params %
        for key,value in params.items():
            if isinstance(value,int) or isinstance(value,float):
                pass
            elif isinstance(value,str) or isinstance(value,unicode):
                if value.lower() == 'true':
                    params[key] = True
                elif value.lower() == 'false':
                    params[key] = False
                elif '+' in value or '-' in value or '*' in value or '/' in value:
                    t = re.findall(r'[A-Za-z]+',value)
                    for tag in t:
                        value = value.replace(tag,str(jg.grep(tag.lower())),1)
                    params[key] = eval(value)

        return params
