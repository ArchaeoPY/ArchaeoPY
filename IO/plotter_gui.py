import numpy as np
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cm as cm
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
import itertools


# import the MainWindow widget from the converted .ui files
from ArchaeoPY.GUI.mpl import Ui_MainWindow

#import ArchaeoPY modules
#import stats
class ArchaeoPYMainWindow(QtGui.QMainWindow, Ui_MainWindow):

        
        """Customization for Qt Designer created window"""
    
        def ClearPlot(self):
            self.mpl.canvas.ax.clear()
            self.mpl.canvas.draw()
            #Clears Legend
            self.legend.remove()
            self.legend_definitions()
            self.mpl.canvas.draw()
            
            
        def copy_to_clipboard(self):
            pixmap = QtGui.QPixmap.grabWidget(self.mpl.canvas)
            QtGui.QApplication.clipboard().setPixmap(pixmap)
            
        def openInputDialog(self):
            x_axis, result = QtGui.QInputDialog.getText(self, "X axis", "Specify units")
            if result:
                self.x_axis = x_axis
            y_axis, result = QtGui.QInputDialog.getText(self, "Y axis", "Specify units")
            if result:
                self.y_axis = y_axis
            self.ClearPlot()
            self.legend.remove()
            self.xval = self.data[self.data.dtype.names[self.xcombo.currentIndex()]]
            self.yval = self.data[self.data.dtype.names[self.ycombo.currentIndex()]]
            temp_scatter = self.mpl.canvas.ax.scatter(self.xval,self.yval, color=next(self.colors), marker=next(self.markers))
            self.mpl.canvas.ax.axis('auto')
            #self.mpl.canvas.ax.set_xlim(xmin=np.min(self.x), xmax=(np.max(self.x)))
            self.mpl.canvas.ax.set_ylim(ymin=np.min(self.yval), ymax=(np.max(self.yval)))
            self.mpl.canvas.ax.set_autoscale_on(True)
            self.mpl.canvas.ax.autoscale_view(True,True,True)
            self.mpl.canvas.ax.set_xlabel(self.x_axis, size = 15)
            self.mpl.canvas.ax.set_ylabel(self.y_axis, size=15)
            #self.mpl.canvas.ax.set_ylabel(self.ytitle, size = 15)
            #self.mpl.canvas.ax.set_title(self.title, size = 15)
            self.handles.append(temp_scatter)
            self.labels.append(self.data.dtype.names[self.ycombo.currentIndex()])
            self.legend = self.mpl.canvas.fig.legend(self.handles,self.labels,'upper right')
            self.mpl.canvas.draw()

        
        def Open_File(self):
            self.fname = QtGui.QFileDialog.getOpenFileName()
            #self.f = open(self.fname, 'rb')
            with open(self.fname, 'r') as f:
                num_cols = len(f.readline().split('	'))-1
                f.seek(0)
                self.data = np.genfromtxt(f, names=True, delimiter='	',dtype=None,filling_values = np.nan, usecols=(range(0,num_cols)))
            #print self.data
            self.x = self.data.dtype.names
            #print self.data[self.data.dtype.names[1]]
            #print self.data[self.data.dtype.names[2]]
            
            self.y = self.data.dtype.names
            self.xcombo.clear()
            self.xcombo.addItems(self.x)
            self.ycombo.clear()
            self.ycombo.addItems(self.y)
            
            #Clears Legend
            self.legend_definitions()
            
        '''
        def Save_Stats(self):
            self.f = open(self.fname, 'rb')
            data = np.genfromtxt(self.f, skip_header=1)
            fname = QtGui.QFileDialog.getSaveFileName(self, 'Save File', 
               '*.csv')            
            output_text = np.column_stack((self.x,self.y))
            np.savetxt(str(fname),output_text,fmt ='%1.2f',delimiter=',', header = self.header)                        
'''
        def Plot_Function(self):
            self.legend.remove()
            self.xval = self.data[self.data.dtype.names[self.xcombo.currentIndex()]]
            self.yval = self.data[self.data.dtype.names[self.ycombo.currentIndex()]]
            self.yval = self.yval - np.median(self.yval)
            temp_scatter = self.mpl.canvas.ax.scatter(self.xval,self.yval, color=next(self.colors), marker=next(self.markers))
            self.mpl.canvas.ax.axis('auto')
            #self.mpl.canvas.ax.set_xlim(xmin=np.min(self.x), xmax=(np.max(self.x)))
            self.mpl.canvas.ax.set_ylim(ymin=np.min(self.yval), ymax=(np.max(self.yval)))
            self.mpl.canvas.ax.set_autoscale_on(True)
            self.mpl.canvas.ax.autoscale_view(True,True,True)
            self.mpl.canvas.ax.set_xlabel('units', size = 15)
            self.mpl.canvas.ax.set_ylabel('units', size=15)
            #self.mpl.canvas.ax.set_ylabel(self.ytitle, size = 15)
            #self.mpl.canvas.ax.set_title(self.title, size = 15)
            self.handles.append(temp_scatter)
            self.labels.append(self.data.dtype.names[self.ycombo.currentIndex()])
            self.legend = self.mpl.canvas.fig.legend(self.handles,self.labels,'upper right')
            self.mpl.canvas.draw()

        
        def legend_definitions(self):
            self.handles = []
            self.labels = []
            
            self.colors = itertools.cycle(["b", "g", "r","c","m","y","b"])
            self.markers = itertools.cycle([".","D","p","*","+"])
            
            self.legend = self.mpl.canvas.fig.legend(self.handles,self.labels,'upper right')

        def Button_Definitions(self):
            self.firstrun=True
            self.Open_button = QtGui.QPushButton('Open', self)
            self.fname = self.Open_button.clicked.connect(self.Open_File)
            #self.fname = self.Open_button.clicked.connect(self.Plot_Function)
            self.Button_Layout.addWidget(self.Open_button)
            
            self.units_button = QtGui.QPushButton("Input Units", self)
            self.units_button.clicked.connect(self.openInputDialog)
            #self.connect(self.inputDlgBtn, QtCore.SIGNAL("clicked()"), self.openInputDialog)
            
            self.pushButton_plot.clicked.connect(self.Plot_Function)
            self.pushButton_clear.clicked.connect(self.ClearPlot)
            QtGui.QShortcut(QtGui.QKeySequence("Ctrl+P"),self, self.Plot_Function)
        


                    
        def __init__(self, parent = None):
            # initialization of the superclass
            super(ArchaeoPYMainWindow, self).__init__(parent)
            # setup the GUI --> function generated by pyuic4
            self.setupUi(self)
            #Adds a Matplotlib Toolbar to the display, clears the display and adds only the required buttons
            self.navi_toolbar = NavigationToolbar(self.mpl.canvas, self)
            self.navi_toolbar.clear()
    
        #Adds Buttons
            a = self.navi_toolbar.addAction(self.navi_toolbar._icon('home.png'), 'Home',
                                            self.navi_toolbar.home)
            #a.setToolTip('returns axes to original position')
            a = self.navi_toolbar.addAction(self.navi_toolbar._icon('move.png'), 'Pan',
                                            self.navi_toolbar.pan)
            a.setToolTip('Pan axes with left mouse, zoom with right')
            a = self.navi_toolbar.addAction(self.navi_toolbar._icon('zoom_to_rect.png'), 'Zoom',
                                            self.navi_toolbar.zoom)
            a.setToolTip('Zoom to Rectangle')
            a = self.navi_toolbar.addAction(self.navi_toolbar._icon('filesave.png'), 'Save',
                               self.navi_toolbar.save_figure)
            a.setToolTip('Save the figure')
            
            QtGui.QShortcut(QtGui.QKeySequence("Ctrl+C"),self, self.copy_to_clipboard)

            self.xcombo = QtGui.QComboBox()
            self.xcombo.addItems('X')
            self.lbl = QtGui.QLabel('X Values')
            self.lbl.setAlignment(QtCore.Qt.AlignHCenter)            
            self.toolbar_grid.addWidget(self.xcombo)
            self.toolbar_grid.addWidget(self.lbl)

            self.ycombo = QtGui.QComboBox()
            self.ycombo.addItems('Y')
            self.lbl = QtGui.QLabel('Y values')
            self.lbl.setAlignment(QtCore.Qt.AlignHCenter)            
            self.toolbar_grid.addWidget(self.ycombo)
            self.toolbar_grid.addWidget(self.lbl)
            


            
            #self.xlabel = QtGui.QInputDialog.getText(self, 'X-axis Label')
            
            #Button_layout is a QT desginer Grid Layout.
            self.toolbar_grid.addWidget(self.navi_toolbar)
            self.Button_Definitions()
            #self.plot_options() 
            
if __name__=='__main__':
    #Creates Main UI window
    app = QtGui.QApplication(sys.argv)
    
    app.processEvents()
    
    #Creates Window Form     
    form = ArchaeoPYMainWindow()
    
    #display form and focus
    form.show()
    #if sys.platform == "darwin":
    form.raise_()
    
    #Something to do with the App & Cleanup?
    app.exec_()
    #atexit.register(form.cleanup)