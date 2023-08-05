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
This module defines the classes relating to basic parses.
"""


__author__ = "Xin-Gang Zhao"

class __ParseProcess(object):

    def __collect_parses__(self):
    
        #self.__jump2logo__()    # show the log %
        (options, args) =self.__get_parse__().parse_args()
 
        all_option = {}       # parameters %
        
        #file to store data for calculation % 
        if options.pool:
            all_option['pool'] = options.pool

        # fast data processing %
        if options.output:
            all_option['output'] = args 
            return all_option

        # vasp_tools %
        if options.vasp_tools:
            all_option['vasp_tools'] = args 
            return all_option

        #input examples % 
        if options.abtools:
            script = options.abtools
            all_option={'script':script}
	
        #parallel environments % 
        cluster = {}
        if options.cores:
            cluster['core'] = options.cores 
        if options.nodes:
            cluster['node'] = options.nodes
        if options.queue:
            cluster['queue'] = options.queue
        if options.project:
            cluster['project'] = options.project
    	
        if len(cluster) >0:
             all_option['cluster'] = cluster
    
        if options.maxjobs:
            all_option['maximum'] = options.maxjobs
        #run/output the required files for calc % 
        if options.submit:
            all_option['run'] = options.submit

        
        #overwrite/update the all the data %
        if options.overwrite:
            all_option['overwrite'] = options.overwrite
        #if options.update:
        #    all_option['update'] = options.update
        if options.restart:
            all_option['restart'] = options.restart
    
        if options.mysql:
            all_option['mysql'] = options.mysql

        if options.django:
            all_option['django'] = options.django

        #extract data % 
        if options.extract:
            all_option['extract'] = options.extract

        #backup files % 
        # if options.compress:
        #     all_option['tarfile'] = options.compress
        #store the data %
        # if options.append2db:
        #     all_option['append'] = options.append2db
    
        #check the status %
        if options.check:
            all_option['check'] = options.check
    
        #remote log/submit %
        # if options.sshlog:
        #     username = options.sshlog.split('@')[0]
        #     ssh_ip = options.sshlog.split('@')[1].split(':')[0]
        #     if ':' in options.sshlog:
        #         ssh_port = options.sshlog.split(':')[-1]
        #     else:
        #         ssh_port = 22
        #     all_option['ssh'] = {'user':username, 'ip':ssh_ip, 'port':ssh_port}  
    
        return all_option


    
    def __get_parse__(self):
    
        from optparse import OptionParser, OptionGroup
    
        parse = OptionParser('jump2 [options]  args')

        parse.set_defaults(\
                                abtools = None,
                                   pool = None, 
                                 submit = None,  
                            #    single = None,
                                project = None,
                              overwrite = None,
                                restart = None,
                                feature = None,
                                  cores = None,
                                  nodes = None, 
                                  queue = None,
                                maxjobs = None,
                            # append2db = None, 
                                extract = None,  
                                  check = None,   
                                  model = None,
                            #  compress = None,   
                            #    sshlog = None,   
                            #    update = None,
                             vasp_tools = None,
                                 output = None)   
    
        #parses for default commands
        
        group_run     = OptionGroup(parse, "Flags for preparing files for calculation:")
        group_extract = OptionGroup(parse, "Flags for extracting data from results:")
        group_check   = OptionGroup(parse, "Flags for checking the status of tasks:")
        group_cluster = OptionGroup(parse, "Flags for managing:")
        group_soft    = OptionGroup(parse, "Flags for start other soft:")
    
        group_run.add_option('-i', '--input', dest='abtools', action='store', 
                         metavar='FILE', default=None, choices=['vasp', 'win2k', 'abinit', 'pwscf', 'gaussian','plot'], 
                         help='Present a basic example for calculation.\n')

        group_run.add_option('-r', '--run', dest='submit', type='choice',
                         default=None, choices=['input', 'qsub', 'prepare','single'],
                         help='Submit the tasks according to the input data.\n')
    
        group_run.add_option('-f', '--file', dest='pool', action='store', 
                         type='string', default=None, help='Pool name for storing the calculating data.\n')
    
        #group_run.add_option('--single', dest='single', action='store', 
        #                 type='string', default=None, help='one task information for single projection.\n')
    
        group_run.add_option('--overwrite', dest='overwrite', action='store_true', 
                         default=False, help='Whether to overwrite files.\n')

        group_run.add_option('--restart', dest='restart', action='store_true', 
                         default=False, help='Whether to restart the uncompleted tasks from pool file.\n')

        #group_run.add_option('-u', '--update', dest='update_change', action='store_true', 
        #                 default=False, help='Update the changes/modification.\n')

        #group_run.add_option('-d', '--del', dest='delete', action='store', 
        #                 type='string', default=None, help='directory: delete the task from queue.\n')
    
        #group_extract.add_option('-s', '--save', dest='append2db', action='store_true', 
        #                 default=False, help='Store the extract data in to database.\n')

        group_extract.add_option('-o', '--output', dest='output', action='store_true', 
                         default=False,help='Output data from calculated result.\n')

        group_extract.add_option('-v', '--vasp', dest='vasp_tools', action='store_true', 
                         default=False,help='simple vasp tools for baise calculationst.\n')
        
        group_extract.add_option('-e', '--extract', dest='extract', action='store', type='choice',
                         choices=['log', 'custom', 'db', 'kpath', 'gap', 'band', 'dos', 'optics'], 
                         default=None, help='Extracting data from the calculated results.\n')

        #group_extract.add_option('-t', '--tar', dest='compress', action='store_true', 
        #                 default=False, help='backup the data to a tarfile named xx.tar.bz2\n')

        group_soft.add_option('--mysql', dest='mysql',action='store',type='choice',
                         choices=['initialize','start','shutdown'],default=None,
                         help='MySQL management module.\n')

        group_soft.add_option('--django',dest='django',action='store',type='choice',
                         choices=['initialize','makemigrations','migrate'],default=None,
                         help='Django management module.\n')

        group_cluster.add_option('--cores', dest='cores', action='store', 
                         type='int', default=None, help='How many codes to be used for one task.\n')
    
        group_cluster.add_option('--queue', dest='queue', action='store', 
                         type='string', default=None, help='Which queue for projecting tasks.\n')
    
        group_cluster.add_option('--num', dest='maxjobs', action='store', 
                         type='int', default=None, help='The maxmium number of jobs to be submit at once.\n')
    
        group_cluster.add_option('--nodes', dest='nodes', action='store', 
                         type='int', default=None, help='How many cluster to be used.\n')
    
        group_cluster.add_option('--project', dest='project', action='store', 
                         type='string', default=None, help='The project name you belong to.\n')

        #group_cluster.add_option('--ssh', dest='sshlog', action='store', type='string', 
        #                 default=None, help='remote manager the tasks, using --ssh=username@192.168.1.1:port\n')


        group_check.add_option('-c', '--check', dest='check', action='store', 
                         default=False, choices=['show', 'load', 'prepare', 'status','qstat','bjobs'],
                         help='Check status of tasks.\n')
    
        parse.add_option_group(group_run)
        parse.add_option_group(group_cluster)
        parse.add_option_group(group_extract)
        parse.add_option_group(group_check)
        parse.add_option_group(group_soft)

        return parse

    def __jump2logo__(self):
       pass 
      #print  """
    
      #    ==========================================================================================
      #    +                                                                                        +
      #    +                 JJ   UU      UU   MMM      MMM   PPPPPPPPP    @@@@@@@@@@               +
      #    +                 JJ   UU      UU   MM M    M MM   PP      PP   @@      @@               +
      #    +                 JJ   UU      UU   MM  M  M  MM   PP      PP           @@               +
      #    +          JJ     JJ   UU      UU   MM   MM   MM   PPPPPPPPP    @@@@@@@@@@               +
      #    +          JJ     JJ   UU      UU   MM   MM   MM   PP           @@                       +
      #    +          JJJJJJJJJ   UUUUUUUUUU   MM        MM   PP           @@@@@@@@@@               +
      #    +                                                                                        +
      #    + (C)opyright belongs to Jilin University, China, 05-01-2017. (Version 1.0)              +
      #    ==========================================================================================
      #       """
