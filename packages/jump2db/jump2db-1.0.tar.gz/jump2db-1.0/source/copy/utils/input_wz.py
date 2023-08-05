from jump2.abtools.vasp.setvasp import SetVasp
from jump2.structure import read 
from jump2.compute.prepare import Prepare


def jump_input(name=None,*args, **kwargs):

    vasp=SetVasp()
    try:	
        vasp.params.update(kwargs) 
    except:
        pass 
	
    #program
    #vasp.program={'standard':'vasp_std', 'nonlinear':'vasp_ncl', 'gamma':'vasp_gam'} 
    vasp.program='/share/apps/vasp/vasp5.4.1/bin/vasp_std'
    
    # task % 
    #vasp.tasks   = 'shape volume ions band carrier dos optics gap emass'
    #vasp.tasks   = 'shape volume ions scf band emass phonon'
    vasp.tasks   = 'scf band emass'
    
    # params test (if neccessary)% 
    #vasp.converge= True         # test the converge parameters, 
            		    # energy, force,, cutoff, 
            	            # and kpoints % 
    #vasp.example = 'POSCAR_exp' # example for test % 
    # 
    vasp.potential = '/home/kzhou/usr/paw_pbe'
    
    
    #vasp.constrain = True       # whether to consider the Force on cell or not % 
    vasp.xc_func = 'pbe'        # 'pbe pbesol hse gw'
    
    # add vdw % 
    #vasp.vdw     = 'b86'         # 'B86 B88 DF2 D2' 
    #vasp.external_files = '../../../../gdalpian/results/xingang/vdw_kernel.bindat' # 
    
    vasp.force   = 1e-2         # force convergence  
    vasp.energy  = 1e-6         # energy convergence
    vasp.cutoff  = 1.3          #  encut setting 
    
    # k-mesh % 
    #vasp.kpoints = 'Gamma', [6,6,6]    
    #vasp.kpoints = 2000                
    #vasp.kpoints = 'G', '6 6 6'      
    #vasp.kpoints = 'M', '4 4 4'
    #vasp.kpoints = 'emass-x',50,'line',' 0.0 0.0 0.0 ! G\n 0.5 0.0 0.0 ! X'
    vasp.kpoints = 0.25
    #vasp.kpath = 30,'G-X: 0.0 0.0 0.0 ! G\n 0.5 0.0 0.0 ! X'
    #vasp.kpath = ('Gamma-R: 0.00000000       0.00000000       0.00000000 ! \Gamma \n  0.50000000       0.00000000       0.00000000 ! R',
    #              'Gamma-X: 0.00000000       0.00000000       0.00000000 ! \Gamma \n  0.00000000       0.50000000       0.00000000 ! X',
    #              'M-Gamma: 0.50000000       0.50000000       0.00000000 ! M \n  0.00000000       0.00000000       0.00000000 ! \Gamma',
    #              'R-X: 0.50000000       0.00000000       0.00000000 ! R \n  0.00000000       0.50000000       0.00000000 ! X',
    #              'X-M: 0.00000000       0.50000000       0.00000000 ! X \n  0.50000000       0.50000000       0.00000000 ! M')
    #vasp.emass_insert = 50

    #vasp.analysis = True
    #==================================================
    #    add a loop for calcualte a lot of structures #
    #==================================================	
    pool=Prepare.pool(vasp)
    pool.set_structure('test',operation=operation)
    pool.save('jptest.dat',overwrite=True)
    Prepare.cluster()
    Prepare.incar(vasp.tasks)
    

 
def operation(structure):
    return structure
