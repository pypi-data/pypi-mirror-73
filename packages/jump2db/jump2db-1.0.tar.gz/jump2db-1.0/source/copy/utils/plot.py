# -*- coding: utf-8 -*-
import jump2.abtools.globalvar as gl

# Update global variables %
LABEL = 20
TITLE = 25
LEGEND = 18
DOSEMIN = -4
DOSEMAX = 4
DOSLIMIT = 0.04
BANDEMIN = -2
BANDEMAX = 2
# Passing global variables %
gl._init()
gl.sets(globals())

import os
from jump2.abtools.plot import Jump2plot
class Diyplot(Jump2plot):
    def init(self):
        super(Jump2plot,self).__init__()

    def figure(self,type='simple'):
        import matplotlib.pyplot as plt
        import matplotlib 
        matplotlib.use('agg')
        if type == 'simple':
            fig = plt.figure(figsize=(12,12),dpi=100)
        elif type == 'band':
            fig = plt.figure(figsize=(12,12),dpi=100)
            plt.tick_params(labelsize=LABEL)
            plt.axhline(linewidth=2.2,color='r',linestyle='--')
            plt.xticks([])
            plt.ylim(BANDEMIN,BANDEMAX)
        elif type == 'dos':
            fig = plt.figure(figsize=(12,6),dpi=100)
            plt.tick_params(labelsize=LABEL)
            plt.axvline(linewidth=2.2,color='r',linestyle='--')
            plt.xlabel("Energy (ev)",fontsize=TITLE)
            plt.ylabel(u'$PDOS\ (states/eV/\AA^{3})$', fontsize=TITLE)
            plt.xlim(DOSEMIN,DOSEMAX)
            plt.ylim(0,DOSLIMIT)

if __name__ == '__main__':
    dp = Diyplot()
    dp.path = os.getcwd()
    dp.plotband()
