import numpy as np
import sys
import os

from PyQt4 import QtCore
from PyQt4 import QtGui
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar

# import the MainWindow widget from the converted .ui files
from ArchaeoPY.GUI.mpl import Ui_MainWindow

#import geoplot load module
from geoplot import Load_Comp, Load_Geoplot_CMD

class ArchaeoPYMainWindow(QtGui.QMainWindow, Ui_MainWindow):

        
        """Customization for Qt Designer created window"""
    
        def ClearPlot(self):
            self.mpl.canvas.ax.clear()
            self.mpl.canvas.draw()
            
        def copy_to_clipboard(self):
            pixmap = QtGui.QPixmap.grabWidget(self.mpl.canvas)
            QtGui.QApplication.clipboard().setPixmap(pixmap)
           
            
        def Open_Geoplot(self):
            self.fname = QtGui.QFileDialog.getOpenFileName()
            print self.fname
            split = os.path.splitext(self.fname)
            self.cmdname = split[0] + '.CMD'
            grid_length,grid_width,sample_interval,traverse_interval = Load_Geoplot_CMD(self.cmdname)
            self.TravL_val.setValue(grid_length)
            self.GridL_val.setValue(grid_width)
            self.TravI_val.setValue(sample_interval)
            self.GridI_val.setValue(traverse_interval)
            
        def Plot_Function(self):
            #Get values from Options Grid
            grid_length = self.TravL_val.value()
            grid_width = self.GridL_val.value()
            sample_interval = self.TravI_val.value()
            traverse_interval = self.GridI_val.value()

            self.output = Load_Comp(self.fname,grid_length,grid_width,sample_interval,traverse_interval)
            self.mpl.canvas.ax.clear()
            print np.shape(self.output)
            self.mpl.canvas.ax.imshow(self.output,cmap=plt.cm.Greys,extent=[0,grid_length,grid_width,0], aspect='equal',interpolation='none',vmin = self.neg_val.value(), vmax = self.pos_val.value())                        
            self.mpl.canvas.draw()

         
 #reordered fields to match layout on window, to allow "tab" when navigating                
        def plot_options(self):

            self.neg_label = QtGui.QLabel('Neg Value', self)
            self.neg_val = QtGui.QDoubleSpinBox(self)
            self.neg_val.setRange(-2047, 2047)
            self.neg_val.setValue(-1)
            
            self.pos_label = QtGui.QLabel('Pos Value', self)            
            self.pos_val = QtGui.QDoubleSpinBox(self)
            self.pos_val.setRange(-2047, 2047)
            self.pos_val.setValue(2)
            
            self.TravL_label = QtGui.QLabel('Trav Length', self)
            self.TravL_val = QtGui.QDoubleSpinBox(self)
            self.TravL_val.setRange(0, 1000)
            self.TravL_val.setValue(30)
            
            self.TravI_label = QtGui.QLabel('Sample Interval', self)
            self.TravI_val = QtGui.QDoubleSpinBox(self)
            self.TravI_val.setValue(0.25)
            
            self.GridL_label = QtGui.QLabel('Grid Width', self)
            self.GridL_val = QtGui.QDoubleSpinBox(self)
            self.GridL_val.setRange(0, 1000)
            self.GridL_val.setValue(30)
            
            self.GridI_label = QtGui.QLabel('Traverse Interval', self)
            self.GridI_val = QtGui.QDoubleSpinBox(self)
            self.GridI_val.setValue(1)
            
            self.TravL_label = QtGui.QLabel('Trav Length', self)
            self.TravL_val = QtGui.QDoubleSpinBox(self)
            self.TravL_val.setRange(0, 1000)
            self.TravL_val.setValue(30)
                    
            self.TravI_label = QtGui.QLabel('Sample Interval', self)
            self.TravI_val = QtGui.QDoubleSpinBox(self)
            self.TravI_val.setValue(0.25)

            self.neg_label = QtGui.QLabel('Neg Value', self)
            self.neg_val = QtGui.QDoubleSpinBox(self)
            self.neg_val.setRange(-2000, 2000)
            self.neg_val.setValue(-1)
                    
            self.pos_label = QtGui.QLabel('Pos Value', self)            
            self.pos_val = QtGui.QDoubleSpinBox(self)
            self.pos_val.setRange(-2000, 2000)
            self.pos_val.setValue(2)

            self.Grid_horizontal_Layout_1.addWidget(self.TravL_label)
            self.Grid_horizontal_Layout_1.addWidget(self.TravL_val)
            self.Grid_horizontal_Layout_1.addWidget(self.TravI_label)
            self.Grid_horizontal_Layout_1.addWidget(self.TravI_val)
            
            self.Grid_horizontal_Layout_2.addWidget(self.GridL_label)
            self.Grid_horizontal_Layout_2.addWidget(self.GridL_val)
            self.Grid_horizontal_Layout_2.addWidget(self.GridI_label)
            self.Grid_horizontal_Layout_2.addWidget(self.GridI_val)
                
            self.Grid_horizontal_Layout_3 = QtGui.QHBoxLayout()
            self.Grid_horizontal_Layout_3.setObjectName("Grid_horizontal_Layout_3")
            self.Options_Grid.addLayout(self.Grid_horizontal_Layout_3, 2, 0, 1, 1)
        
            self.Grid_horizontal_Layout_3.addWidget(self.neg_label)
            self.Grid_horizontal_Layout_3.addWidget(self.neg_val)
            self.Grid_horizontal_Layout_3.addWidget(self.pos_label)
            self.Grid_horizontal_Layout_3.addWidget(self.pos_val)
        
                
        def Button_Definitions(self):
            self.firstrun=True
            
            self.Open_button = QtGui.QPushButton('Open', self)
            self.fname = self.Open_button.clicked.connect(self.Open_Geoplot)
            self.Button_Layout.addWidget(self.Open_button)
          
            self.pushButton_plot.clicked.connect(self.Plot_Function)
            self.pushButton_clear.clicked.connect(self.ClearPlot)
            QtGui.QShortcut(QtGui.QKeySequence("Ctrl+P"),self, self.Plot_Function)

            QtGui.QShortcut(QtGui.QKeySequence("Ctrl+C"),self, self.copy_to_clipboard)
   
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
    
            #Button_layout is a QT desginer Grid Layout.
            self.toolbar_grid.addWidget(self.navi_toolbar)
            self.Button_Definitions()
            self.plot_options()

        #Low and High Pass filters
            #Calculations required
            """
            fc = 0.1  # Cutoff frequency as a fraction of the sample rate (in (Load_comp)).
            b = 0.08  # Transition band, as a fraction of the sample rate (in (Load_comp)).
            N = int(np.ceil((4 / b)))
            if not N % 2: N += 1  # Make sure that N is odd.
            n = np.arange(Load_comp)
 
             # Compute a low-pass filter (windowed sinc filter)
             h = np.sinc(2 * fc * (n - (N - 1) / 2.))
             # Compute Blackman window.
                 w = 0.42 - 0.5 * np.cos(2 * np.pi * n / (N - 1)) + \
                     0.08 * np.cos(4 * np.pi * n / (N - 1))
                 # or just: w = np.blackman(N)
             h = h * w
             h = h / np.sum(h)
 
             # Create a high-pass filter from the low-pass filter through spectral inversion.
             h = -h
             h[(N - 1) / 2] += 1
             """
             #adding buttons
"""             
             a = self.navi_toolbar.addAction(self.navi_toolbar._icon('NAME OF ICON.png'), 'Low Pass',
                                            self.navi_toolbar.X)
             a = self.navi_toolbar.addAction(self.navi_toolbar._icon('NAME OF ICON.png'), 'High Pass',
                                            self.navi_toolbar.X)
             """
            
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
    atexit.register(form.cleanup)