from jump2.abtools.vasp.vaspflow import VaspFlow

class MiniFlow(VaspFlow):

    def __init__(self, vasp=None, stdin=None, rootdir=None, *args, **kwargs):

        # from .tasks import VaspTask
        # from .setvasp import SetVasp 
        from os.path import dirname,join
        from jump2.compute.__cluster__ import __Script__
    
        self.stdin = stdin
        self.rootdir = rootdir
        self.json = join(dirname(dirname(rootdir)),'.diyinput')
        self.cluster = __Script__(dirname(dirname(rootdir)))
	
    def diy_calculator(self, vasp, stdout, stdin=None, **kwargs):
        
        print('Default calculator.')

    @classmethod
    def write_json(self,path,**params):
        '''
        Write mobility parameters in .diyinput
        '''
        import json
        from os.path import exists,join
 
        json_file = join(path,'.diyinput')
        json_dict = {}
        if exists(json_file):
            try:
                with open(json_file,'r') as f:
                    json_dict = json.load(f)
            except:
                pass
     
        for diy_name in params: 
            if isinstance(params[diy_name],dict):
                if diy_name not in json_dict:
                    json_dict[diy_name] = params[diy_name]
                else:
                    for key in params[diy_name]:
                        if key not in json_dict[diy_name]:
                            json_dict[diy_name][key] = params[diy_name][key]

        with open(json_file,'w') as f:
            f.write(json.dumps(json_dict,indent=3)) 
  

