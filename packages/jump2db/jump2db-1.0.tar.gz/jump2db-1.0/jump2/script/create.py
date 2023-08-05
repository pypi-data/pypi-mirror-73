import os
import shutil

class __CreateInput(object):
    
    def __init__(self,parse):

        if parse['script'] == 'vasp':
            self.__vasp__()

        if parse['script'] == 'plot':
            self.__plot__()

    def __plot__(self):
        copyfile = ['plot.py']
        home = os.environ['HOME']+'/.jump2/utils/'
        path = os.getcwd()
        for file in copyfile:
            shutil.copy(home+file,path)

    def __vasp__(self):
        copyfile = ['input.py']
        home = os.environ['HOME']+'/.jump2/utils/'
        path = os.getcwd()
        for file in copyfile:
            shutil.copy(home+file,path)
