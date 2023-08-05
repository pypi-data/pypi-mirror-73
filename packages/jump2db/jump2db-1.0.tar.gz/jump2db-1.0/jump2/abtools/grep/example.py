from __init__ import *
import os

class Jump2out():

    def __init__(self):
        pass

    def analysis_grep(self,scfdir):
        # GrepOutcar %
        jg = Jump2grep(scfdir)
        print("ispin :",jg.ispin(scfdir))
        print("force :",jg.force(scfdir))
        for i in jg.atominfo(scfdir):
            print(i)

        # Jump2Grep %
        properties = ['nkdim', 'nedos', 'nbands', 'nkpts', 'istart', 'icharg', 'ispin', 'nelm', 'nsw', 'lmaxmix', # int type %
                    'ibrion', 'nfree', 'isif', 'isym', 'pstress', 'nelect', 'ismear', 'ialgo', 'lorbit', # int type %
                    'lsorbit', 'lwave', 'lcharg', 'lvtot', 'lelf', # bool type %
                    'encut', 'ediff', 'ediffg', 'cshift', 'potim', 'emin', 'emax', 'sigma', 'free_energy', # float type %
                    'energy_without_entropy', 'volume', 'fermi_energy', 'max_force', # float type %
                    'date', 'datetime', 'vasp_version', 'point_group', 'prec', 'gga', # str type %
                     'length_of_vector', 'force', 'direct_lattice_vectors', 'reciprocal_lattice_vectors'] # ndarray type %

        jg.stdin = scfdir
        for p in properties:
            print(p,":",jg.grep(p))

    def analysis_band_jump2(self,path):
        jb = Jump2band(path)
        print("classname",jb.__class__)
        print("kpath",jb.kpath)
        print("scfdir",jb.scfdir)
        print("nkpts :",jb.nkpts(jb.scfdir))
        print("E-fermi",jb.get_fermi())
        print("Kpoints.shape",jb.get_kpoints().shape)
        print("bands.shape",jb.get_bands().shape)
        print("vaccum_level :",jb.get_locpot())
        print("bandgap :",jb.get_bandgap())
        print("cbmvbm :",jb.get_cbmvbm())
        print("emass :",jb.get_emass())

    def analysis_dos(self,path):
        jd = Jump2dos(rootdir)
        print("E-fermi :",jd.get_fermi())
        dos_energy,dos = jd.get_dos()
        # dos_energy,dos = jd.get_force_dos(jd.stdin)
        print("dos_energy.shape",dos_energy.shape)
        print("dos.shape",dos.shape)

    def analysis_optic(self,path):
        jop = Jump2optic(rootdir)
        print('dielectric_ionic :',jop.get_dielectric_ionic())
        print('dielectric :',jop.get_dielectric())

    def analysis_fatband(self,path):
        jf = Jump2band.fatband(rootdir) 
        print('nions :',jf.nions(jf.stdin))
        print('nkpts :',jf.nkpts(jf.stdin))
        print("kpoints.shape :",jf.get_kpoints().shape)
        print("bands.shape :",jf.get_bands().shape)
        print("procar.shape :",jf.get_procar().shape)
        print("tot_procar.shape :",jf.get_tot_procar().shape)
        value,info,labels = jf.get_emax_procar()
        print("emax_procar.shapes :",value.shape,info.shape,labels)
        # value,info,labels = jf.get_pmax_procar()
        # print("pmax_procar.shape :",jf.get_pmax_procar())

# root = os.getcwd().split('src')[0]
# rootdir = os.path.normcase(root+"example/ex_band")
# scfdir = os.path.normcase(root+"example/ex_band/scf")
# banddir = os.path.normcase(root+"example/ex_band/nonscf/band")
# emassdir = os.path.normcase(root+"example/ex_band/nonscf/emass")
# banddir_single =  os.path.normcase(root+"example/ex_band/nonscf/band/W-K")
rootdir = os.path.normcase("c:/Users/JLUzk/Desktop/example/ex_band")
scfdir = os.path.normcase("c:/Users/JLUzk/Desktop/example/ex_band/scf")
banddir = os.path.normcase("c:/Users/JLUzk/Desktop/example/ex_band/nonscf/band")
fatbanddir = os.path.normcase("c:/Users/JLUzk/Desktop/example/ex_band/nonscf/fatband")
jo = Jump2out()

# Jump2grep %
# jo.analysis_grep(scfdir)
 
# Jump2band-multi%
# jo.analysis_band_jump2(rootdir)

# Jump2band-single%
# ab = Jump2band(banddir_single)
# print("classname",ab.__class__)
# print("kpath",ab.kpath)
# print("nkpts :",ab.nkpts(scfdir))
# print("E-fermi",ab.get_fermi())
# print("kpoints.shape",ab.get_kpoints().shape)
# print("bands.shape",ab.get_bands().shape)
# print("bandgap :",ab.get_bandgap())
# print("cbmvbm :",ab.get_cbmvbm())
# print("force_cbmvbm :",ab.get_force_cbmvbm(banddir))
# print("force_emass :",ab.get_force_emass(emassdir))

# Jump2dos %
# jo.analysis_dos(rootdir)

# Jump2optic %
# jo.analysis_optic(rootdir)

# Jump2fatband %
jo.analysis_fatband(rootdir)


