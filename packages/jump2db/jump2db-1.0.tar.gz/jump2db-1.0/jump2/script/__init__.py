
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
This module defines the function for running jump2.
"""

__contributor__ = 'Xingang Zhao'
__edited_date__ = '2017.05.17'

def runjump2():

    from ..parse import __ParseProcess
    from ..compute import __LaunchTasks
    from ..analysis import __Analysis
    from .create import __CreateInput
    from .output import __OutputData
    from .vasptools import __Vasptools
    from .softmanage import __Mysql,__Django
    
    jump = __ParseProcess()
    #jump.__jump2logo__()
    parse = jump.__collect_parses__()
    print(parse)
   
    if len(parse) ==0:
        print('jp -h/--help')
        return
 
    if 'run' in parse:
         #__CheckStatus(parse)  # check all the tasks  % 
         __LaunchTasks(parse)   # launch unfinish task %  	

    if 'vasp_tools' in parse:
        fun = __Vasptools()
        fun.run(parse)	

    if 'output' in parse:
        fun = __OutputData()
        fun.run(parse)

    if 'append' in parse:
        __SaveData(parse)
        
    if 'extract' in parse:
        __Analysis(parse)

    if 'tarfile' in parse:
        __CompressData(parse)
	
    if 'check' in parse:
        try:
            from .check import __CheckStatus
        except:
            pass
        __CheckStatus(parse)

    if 'script' in parse:
        __CreateInput(parse)

    if 'mysql' in parse:
        __Mysql(parse)

    if 'django' in parse:
        __Django(parse)
