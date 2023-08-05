# coding: utf-8
# Copyright (c) JUMP2 Development Team.
# Distributed under the terms of the JLU License.


#=================================================================
# This file is part of JUMP2.
#
# Copyright (C) 2017 Jilin University
#
#  Jump2 is a platform for high throughput calculation. It aims to 
#  make simple to organize and run large numbers of tasks on the 
#  superclusters and post-process the calculated results.
#  
#  Jump2 is a useful packages integrated the interfaces for ab initio 
#  programs, such as, VASP, Guassian, QE, Abinit and 
#  comprehensive workflows for automatically calculating by using 
#  simple parameters. Lots of methods to organize the structures 
#  for high throughput calculation are provided, such as alloy,
#  heterostructures, etc.The large number of data are appended in
#  the MySQL databases for further analysis by using machine 
#  learning.
#
#  Jump2 is free software. You can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published 
#  by the Free sofware Foundation, either version 3 of the License,
#  or (at your option) and later version.
# 
#  You should have recieved a copy of the GNU General Pulbic Lincense
#  along with Jump2. If not, see <https://www.gnu.org/licenses/>.
#=================================================================

"""
This module defines the classes relating to tasks pool.
"""


__author__ = "Xin-Gang Zhao"
__copyright__ = "Copyright 2017, The JUMP2"
__version__ = "1.0"
__maintainer__ = "JUMP2 team"
__email__ = "xgzhao@0201@gmail.com"
__status__ = "underdeveloped"

class __FileLock__(object):
    """
    class to control the single thread to I/O pool file.
    """

    def __init__(self):
        self.__handle = None

    def __lock__(self, name=None, lock_type='private'):
        """
        function to lock the pool file
        """
        import fcntl

        self.__handle = name
        #if self.__islock : return True

        private  = fcntl.LOCK_EX
        nonblock = fcntl.LOCK_NB
        share    = fcntl.LOCK_SH

        try:
            if lock_type == 'nonblock':
                fcntl.flock(self.__handle.fileno(), nonblock)

            elif lock_type == 'private':
                fcntl.flock(self.__handle.fileno(), private)

            elif lock_type == 'share':
                fcntl.flock(self.__handle.fileno(), share)

        except:
            pass

    def __release__(self):
        """
	function to realse the open file.
	"""
        import fcntl

        fcntl.flock(self.__handle, fcntl.LOCK_UN)
        self.__handle.close()
        self.__islock = False 

    def __getattr__(self,value):
        if '__islock' in value:
            return False
        else:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

class Pool(__FileLock__):
      
    """
    Pool is a interface for organizing the input data according to
        the program and structural factory, and output a name.pool
        file including all the info (OBJECTS) for calculations.

    tributes::
        functional: the main task to do;
        structure: the structure object; 

    functionals:

        save_pool: save the pool contained all the information
                    as you set;

        get_current_pools: obtain the current pool if exists;
        load_pool: get the detailed information in pool file;
        iter_pool: do loop the pool for different operation;
        check_pool: check the all pool status;
        update_pool: update pool according to the status;

    """


    def __init__(self, *args, **kwargs):

        super(Pool, self).__init__()
        self.__pool = {}

        self.__prior  = 10
        self.__name = 'JUMP2.pbs'
        self.__functional   = None
        self.__structure = None
        self.__id = -1
        self.__run = None
        self.__pid = -1

    @property
    def job_id(self):
        return self.__id

    @job_id.setter
    def job_id(self, value=None):
        import re

        if isinstance(value,int):
            self.__id = value

        if isinstance(value,str):
            try:
                self.__id = int(re.findall(r'\d+',value)[0])
            except:
                self.__id = 0

    @property
    def outdir(self):
        return self.__run

    @outdir.setter
    def outdir(self, *args):
        import os
        from os.path import normpath
        from copy import deepcopy
	
        abspath = os.getcwd()

        directory = []
        if len(args) == 0:
            self.__run = abspath
        elif isinstance(args[0], tuple):
            for p in args[0]:
                p = normpath(p)
                if '/' in p:
                    if p.startswith('./') or p.startswith('/'):
                        print("Warning:relative output directory is used....")
                        folder = p.split('/')[1:]
                    else:
                        folder = p.split('/')
                    for chd in folder:
                        directory.append(chd.strip())
                else:
                    directory.append(p)

        elif isinstance(args[0],str):
            p = normpath(args[0])
            if '/' in p:
                if p.startswith('./') or p.startswith('/'):
                    print("Warning:relative output directory is used....")
                    folder = p.split('/')[1:]
                else:
                    folder = p.split('/')
                for chd in folder:
                    directory.append(chd.strip())
            else:
                directory.append(p)

        self.__run = '/'.join(directory)
        self.__pool[self.__run] = {}
        self.__pool[self.__run]['prior'] = deepcopy(self.prior)
        self.__pool[self.__run]['status']  = 'wait'
        self.__pool[self.__run]['job_id'] = deepcopy(self.job_id)
        self.__pool[self.__run]['functional'] = deepcopy(self.functional) 

    @property 
    def prior(self):
        """
        Object of prior, range of integer number [0~10], the tasks 
            with maximum number would be lauched firstly.
            default is 0, all the tasks are equally to be submitted.
        """
        return self.__prior
 
    @prior.setter
    def prior(self, value=10):
        """
        Attribute to order the task:
        10: normal order;
        9-1: to restart the unfinished task,and the prior is
	    from low to high from 9-1; 
        0: task finished
        -1: task not finihsed but with error
        """
        try:
            value = int(value)
        except:
            pass
        if isinstance(value, int):
            self.__prior = value

    @property
    def functional(self):
        """
        Object of program, type ModuleFactory.
        """
        return self.__functional

    @functional.setter
    def functional(self, value):
        """
        note: now only VASP object is avaliable
        """
        self.__functional = value

    @property
    def mainkey(self):
        maink = {}
        for key,value in self.__pool.items():
            maink[key] = value['functional'].structure.get_format()

        return maink

   #@property 
   #def structure(self):
   #    """
   #    Object of Structure.
   #    """
   #    return self.__structure

   #@structure.setter
   #def structure(self, value):
   #    
   #    #from structure.structure import Structure 
   #    #if isinstance(value, Structure):
   #    #    self.__structure  = value
   #    self.__structure  = value
   #    #else:
   #    #    self.__structure = value  # under development % 
            
    def save(self, name=None, overwrite=True, *args, **kwargs):
        """
        Method aims to store input information in a binary file.

        args:
            pool_name:: string, name of output file;
            overwrite:: bool, overwrite the file or not;
        
        """

        from os.path import exists, dirname, abspath 
        import pickle

        pool = {}
        if len(kwargs) > 0:
            self.__pool.update(kwargs)

        if name is None:
            name = self.__name
        else:
            name = abspath(name)
	
        if exists(name):
            f = open(name, 'rb')
            try:
                self.__lock__(f)
                pool = pickle.load(f)
                #self.__release__()
            except:
                raise IOError ('cannot load '+name)

        # merged files %
        if len(args) > 0:
            for dat in args:
                if exists(dat):
                    try:
                        f = open(dat, 'rb')
                        self.__lock__(f)
                        self.__pool.update(pickle.load(f))
                        self.__release__()
                    except:
                        pass
	
        if overwrite is True:
            pool = self.__pool    # overwrite %
        else:
            pool.update(self.__pool) # update %
        try:
            f = open(name, 'wb') 
            self.__lock__(f)
            pickle.dump((pool), f)
        except:
            raise IOError ('cannot dump '+ name)


        self.__release__()  #
 
        del pool
   

    def merged(self, name=None, *args, **kwargs):
        """
        merge the files exists pool files
        """
        self.save(name, False, *args)

    def loader(self, name, *args, **kwargs):
        """
        load the pool with only one proccess %
        """

        import pickle

        #try:
        if True:
            f = open(name, 'rb')
            self.__lock__(f)
            self.pool =pickle.load(f)
        #except:
        #    raise IOError ('invalid '+name)

        return self
        #note please conbine the loader with __realse__
