#===============================================================
#
#
#===============================================================
import shutil
from setuptools import find_packages, setup
from os.path import exists,join,relpath
import os
import stat

#required packages.

#setup (install_requires=['phononpy == 1.14.2'])
#setup (install_requires=['ipython >= 2.0'])
#setup (install_requires=['django  >= 1.7'])
#setup (install_requires=['python >= 2.7.0, <2.8'])
#setup (install_requires=['numpy   >= 1.6.0'])


HOME = os.environ['HOME']
JUMP2PATH = HOME+'/.jump2'
PYTHONPATH = os.popen('which python').readline()

# copy jp with RWX %
if not exists(join(HOME,'.local')):
    os.makedirs(join(HOME,'.local'))
if not exists(join(HOME,'.local/bin')):
    os.makedirs(join(HOME,'.local/bin'))

with open(HOME+'/.local/bin/jp','w') as f:
    f.write('#!'+PYTHONPATH)
    with open('source/jp','r') as g:
        for line in g:
            f.write(line)
os.chmod(HOME+'/.local/bin/jp',stat.S_IRWXU)    

# copy .jump2 to HOME %
if exists(join(HOME,'.jump2')):
    shutil.rmtree(join(HOME,'.jump2'))
shutil.copytree('source/copy',join(HOME,'.jump2'))

# add .local/bin to $PATH %
PATH = os.environ['PATH']
PATHs = list(set(PATH.split(':')))
path = HOME+'/.local/bin'
if path not in PATHs:
    with open(HOME+'/.bashrc','a') as f:
        f.write('\nPATH={0}:$PATH\n'.format(path))
    os.system('source ~/.bashrc')

# jump2 packages.
#JUMP2 = 'module'
JUMP2 = 'jump2'
PACKAGES = [JUMP2] + ['%s.%s' % (JUMP2, i) for i in find_packages(JUMP2)]
SOURCE = []
for path, dirs, files in os.walk('source'):
    for f in files:
        SOURCE.append(join(relpath(path,os.getcwd()),f))

setup(name = 'jump2db',
      version = '1.0',
      license = 'Jilin University',
      description = 'Python Package for HTP calculation.',
      author = 'Xin-Gang Zhao',
      author_email = 'az351250965@gmail.com',
      url = 'http://tdos.xyz',
      packages = PACKAGES,
      data_files = SOURCE)

