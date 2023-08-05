
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
from .analysis import __Analysis
from jump2.abtools.vasp.check import CheckStatus

def GrepModule(module='basic',path=None,soft='vasp'):

    if module == 'basic' or module.lower() == 'outcar':
        from ..abtools.grep import Jump2grep
        return Jump2grep(path) 
    
    elif band in module.lower():
        from ..abtools.grep import Jump2band
        return Jump2band(path) 

    elif dos in module.lower():
        from ..abtools.grep import Jump2dos
        return Jump2dos(path) 

    elif optic in module.lower():
        from ..abtools.grep import Jump2optic
        return Jump2optic(path)














