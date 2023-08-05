from os.path import dirname,realpath,abspath
from os import listdir
import importlib

def get_diy_moudles():
    moudles = []
    for moudle in listdir(get_diy_path()):
        if moudle.endswith('.py'):
            moudles.append(moudle.split('.')[0])
    return moudles

def get_diy_path():
    return abspath(dirname(realpath(__file__)))

def import_diy_moudle(moudle_name):
    if moudle_name not in get_diy_moudles():
        raise ImportError("Moudle not exists")
    else:
        diy_module = importlib.import_module('jump2.abtools.diyflow.'+moudle_name)
        diy_class = getattr(diy_module,moudle_name.capitalize())
        return diy_class
