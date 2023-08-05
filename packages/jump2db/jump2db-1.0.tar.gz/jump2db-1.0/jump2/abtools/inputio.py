from yammbo.yammboio import YammboIO
from qe.qeio import QeIO
from win2k.win2kio import Win2kIO
from guassian.guassianio import GuassianIO
from gulp.gulpio import GulpIO
from vasp.vaspio import VaspIO
class InputFiles(VaspIO,GuassianIO,GulpIO,Win2kIO,QeIO):
    pass
