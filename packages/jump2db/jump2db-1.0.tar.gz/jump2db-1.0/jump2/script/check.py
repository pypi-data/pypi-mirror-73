#!/usr/bin/python   
# -*- coding: utf-8 -*-
from jump2.abtools.vasp.check import CheckStatus
from jump2.compute.pool import Pool

class __CheckStatus(object):

    def __init__(self, params=None, *args, **kwargs):
        import os
        if 'pool' in params:
            self.poolname = os.path.abspath(params['pool']) 
            # show task status in form %
            if params['check']  == 'show':
                self.__form()

            # update poolfile base on .status %
            elif params['check']  == 'load':
                self.__load()

            # update .status %
            elif params['check'] == 'status':
                self.__status()

            elif params['check']  == 'prepare':
                self.__submit()

            if params['check']  in ['qstat','bjobs']:
                self.__qstat(params['check'],params['pool'])

        else:
            if params['check'] in ['qstat','bjobs']:
                self.__qstat(params['check'])
            else:
                raise ("Please add -f [poolname]")
        
    def __status(self):
        import os
        from pprint import pprint
        pool = Pool().loader(self.poolname).pool
        CS = CheckStatus()
        success = 0
        
        for root,func in pool.items():
            file = os.path.join(root,'.status')
            tasks = self.create_tasks(func['functional'].tasks)
            status=CS.rebuild_status(root,tasks)
            for task in sorted(status):
                CS.write_status(root,status=status[task],task=task,rel=False)
            print(root)
            #pprint(status)
            success+=1
            if pool[root]['prior'] == 10 and len(status) > 0:
                pool[root]['prior'] = 9
        Pool().save(self.poolname,**pool)

        print('success: %s' %success)
                

    def __load(self):
        pool = Pool().loader(self.poolname).pool
        CS = CheckStatus()
        
        for key,func in pool.items():
            tasks = self.create_tasks(func['functional'].tasks)
            key2,finish_tasks = CS.load_status(key)
            print(key2,finish_tasks)
            status = 'finish'
            for task in tasks:
                if task in finish_tasks:
                    if finish_tasks[task] is True:
                        continue
                    else:
                        status = 'wait'
                        break
                else:
                    status = 'wait'
                    break
            if pool[key]['status'] != 'finish' and status == 'finish':
                pool[key]['status'] = 'finish'
                print("load pool:",key)
        Pool().save(self.poolname,**pool)

    def __submit(self):

        pool = Pool().loader(self.poolname).pool
        for i in pool.keys():
            if pool[i]['status'] == 'running':
                print('flush pool :',i)
                pool[i]['status'] = 'wait'
                pool[i]['prior'] = 10
                pool[i]['job_id'] = -1
        Pool().save(self.poolname,**pool)

    def __qstat(self,order,jobid=None):
        from jump2.compute.manager import TaskManager
        import os
        
        cwd = os.getcwd()

        if order == 'qstat':
            tm = TaskManager('pbs') 

        elif order == 'bjobs':
            tm = TaskManager('lsf') 

        if jobid and jobid.isdigit():
            abspath = tm.get_task_by_id(jobid)
            if len(abspath) > 30 and abspath.startswith(cwd):
                print(jobid,':', abspath[len(cwd)+1:])
            else:
                print(jobid,':',abspath)

        else:
            job_dict = tm.get_task_by_user()
            if len(job_dict) != 0:
                for jobid,path in job_dict.items():
                    if len(path) > 30 and path.startswith(cwd):
                        print(jobid,':', path[len(cwd)+1:])
                    else:
                        print(jobid,':',path)
        

    def __form(self):
        from copy import deepcopy
        from collections import OrderedDict
        CS = CheckStatus()

        tmp = OrderedDict()
        tmp['job_id'] = ''
        tmp['prior'] = ''
        tmp['status'] = ''
        #tmp['relax'] = ''
        tmp['scf'] = ''
        __defaultDict__ = tmp


        pool = Pool().loader(self.poolname).pool
        totallist = []
        for stdout,value in pool.items():
            tasks = self.create_tasks(value.pop('functional').tasks)
            __updateDict__ = {i:'--' for i in tasks}
            tmp = deepcopy(__defaultDict__)
            tmp.update(value)   
            if value['status'] in ['finish','running'] or value['prior'] < 10:
                line,status=CS.load_status(stdout)
                __updateDict__.update(status)
            tmp.update(__updateDict__)
            tmp['path'] = stdout
            totallist.append(tmp)

        timingInfo = totallist
        keyHeader = timingInfo[0].keys()
        keyMaxLen = {}

        for item in timingInfo:
            for i,h in enumerate(keyHeader):
                maxLen = max(len(h), len(str(item[h])))
                if keyMaxLen.get(h, None):
                    maxLen = max(maxLen, keyMaxLen[h])
                keyMaxLen[h] = maxLen

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
        
        print('\033[0;32;40mJump2 Tasks Check Mode\033[0m')

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
 
 
    def create_tasks(self,task_dict):
        tasks = []
        if isinstance(task_dict,dict):
            if 'opt' in task_dict:
                tasks.append('relax')
            if 'scf' in task_dict:
                tasks.append('scf')
            if 'nonscf' in task_dict:
                tasks.extend(task_dict['nonscf'])
            if 'diyflow' in task_dict:
                tasks.extend(task_dict['diyflow'])
        else:
            from jump2.abtools.vasp.tasks import VaspTask
            if isinstance(task_dict,VaspTask):
                if task_dict.optimize is not None:
                    tasks.append('relax')
                if task_dict.scf is not None:
                    tasks.append('scf')
                if task_dict.nonscf is not None:
                    for i in task_dict.nonscf:
                        tasks.append(i)
                if task_dict.diyflow is not None:
                    for i in task_dict.diyflow:
                        tasks.append(i)
        return tasks
