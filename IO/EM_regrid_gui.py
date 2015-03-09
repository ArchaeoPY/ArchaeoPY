import numpy as np
import sys
#from PyQt4 import QtCore
from PyQt4 import QtGui
#import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab
#import matplotlib.cm as cm
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
#import itertools
#from pandas import *
#from matplotlib.mlab import griddata
#from sklearn.neighbors import KDTree
#from ArchaeoPY.Positional.invdisttree import cartesian

# import the MainWindow widget from the converted .ui files
from ArchaeoPY.GUI_Templates.mpl import Ui_MainWindow

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
        
        def Open_File(self):
            self.fname = QtGui.QFileDialog.getOpenFileName()
            #Opes File
            with open(self.fname, 'r') as f:
                num_cols = len(f.readline().split('	'))-1
                f.seek(0)
                self.data = np.genfromtxt(f, names=True, delimiter='	',dtype=None,filling_values = np.nan, usecols=(range(0,num_cols)))

            #Defines x and y values
            self.x = self.data.dtype.names
            self.y = self.data.dtype.names
            self.z = self.data.dtype.names
            #Populates combo boxes with header names
            self.xcombo.clear()
            self.xcombo.addItems(self.x)
            self.ycombo.clear()
            self.ycombo.addItems(self.y)
            self.zcombo.clear()
            self.zcombo.addItems(self.z)            
            
            #Clears Legend
            #self.legend_definitions()
            
        '''
        def Save_Stats(self):
            self.f = open(self.fname, 'rb')
            data = np.genfromtxt(self.f, skip_header=1)
            fname = QtGui.QFileDialog.getSaveFileName(self, 'Save File', 
               '*.csv')            
            output_text = np.column_stack((self.x,self.y))
            np.savetxt(str(fname),output_text,fmt ='%1.2f',delimiter=',', header = self.header)                        
'''
        def grid_data(self):
            self.mpl.canvas.ax.clear()
            #Takes x and y values to plot from combo box selection
            self.xval = self.data[self.data.dtype.names[self.xcombo.currentIndex()]]
            self.yval = self.data[self.data.dtype.names[self.ycombo.currentIndex()]]
            self.zval = self.data[self.data.dtype.names[self.zcombo.currentIndex()]]
            self.x_int = float(self.xint_box.text())
            self.y_int = float(self.yint_box.text())
            
            

            #xi = np.arange(np.min(self.xval), np.max(self.xval), self.x_int)
            #yi = np.arange(np.min(self.yval), np.max(self.yval), self.y_int)
            #zi = griddata(self.xval, self.yval, self.zval, xi, yi, interp='nn')
            #print np.shape(zi)

            #self.mpl.canvas.ax.axis('auto')
            
            #Creates scatter plot
            self.mpl.canvas.ax.imshow(zi)
            self.mpl.canvas.draw()
            np.savetxt('test.txt', zi, delimiter='    ')
        
        def save_data(self):
            self.save_fname = QtGui.QFileDialog.getSaveFileName(self, 'Save Gridded Data', selectedFilter='*.txt')
        

        def stats(self): #Calculates stats info of y values and sends back to UI
            self.mean = str(np.round(np.mean(self.yval), decimals=3))
            self.mean_output.setText(self.mean)
            self.median = str(np.round(np.median(self.yval), decimals=3))
            self.median_output.setText(self.median)
            self.sd = str(np.round(np.std(self.yval), decimals=3))
            self.sd_output.setText(self.sd)
 
        def moving_average_buttons(self): #Radio Button Helper
            if self.rolling_mean_radio.isChecked():
                self.moving_mean()
            else:
                self.moving_median()
            
        def moving_mean(self):   
            self.trend_y= rolling_mean(self.yval, self.moving_avg_window.value())
            self.plot_trendline()
        
        def moving_median(self):
            self.trend_y = rolling_median(self.yval, self.moving_avg_window.value())
            self.plot_trendline()
        
                              
        def button_grid(self): #Defines button and layout 
            #self.firstrun=True
            self.buttons_layout = QtGui.QGridLayout()
            self.buttons_box = QtGui.QGroupBox()
            self.buttons_box.setLayout(self.buttons_layout)
            
            self.stats_layout = QtGui.QGridLayout()
            self.stats_box = QtGui.QGroupBox()
            self.stats_box.setLayout(self.stats_layout)

            self.plot_layout = QtGui.QGridLayout()
            self.plot_box = QtGui.QGroupBox()
            self.plot_box.setLayout(self.plot_layout)
            
            #File Properties
            self.Grid_horizontal_Layout_2.addWidget(self.buttons_box, 1)
            string = '<span style=" font-size:12pt;; font-weight:600;">File Settings</span>'       
            self.buttons_layout_text = QtGui.QLabel(string, self)             
            
            self.buttons = QtGui.QButtonGroup()            
            self.open_button = QtGui.QPushButton('Open', self)
            self.buttons.addButton(self.open_button)
            self.open_button.clicked.connect(self.Open_File)
            self.grid_button = QtGui.QPushButton('Grid', self)
            self.buttons.addButton(self.grid_button)
            self.grid_button.clicked.connect(self.grid_data)
            self.clear_button = QtGui.QPushButton('Clear', self)
            self.buttons.addButton(self.clear_button)
            self.clear_button.clicked.connect(self.ClearPlot)
            self.chart_title = QtGui.QLineEdit(self)
            self.chart_title.setText("Enter Chart Title")
            self.xy_units = QtGui.QLineEdit(self)
            self.xy_units.setText("X/Y Units")
            self.z_units = QtGui.QLineEdit(self)
            self.z_units.setText("Z Units")
            
            self.xcombo = QtGui.QComboBox()
            self.xcombo.addItems('X')
            self.x_lbl = QtGui.QLabel('X Values --')          
            
            self.ycombo = QtGui.QComboBox()
            self.ycombo.addItems('Y')
            self.y_lbl = QtGui.QLabel('Y values --')
            
            self.zcombo = QtGui.QComboBox()
            self.zcombo.addItems('Z')
            self.z_lbl = QtGui.QLabel('Z values --')
            
            self.xint_lbl = QtGui.QLabel('X Interval')            
            self.xint_box = QtGui.QLineEdit()
            self.yint_lbl = QtGui.QLabel('Y Interval')
            self.yint_box = QtGui.QLineEdit() 
            
            

            self.buttons_layout.addWidget(self.buttons_layout_text, 0,0,1,4)                      
            self.buttons_layout.addWidget(self.open_button, 1,0)
            self.buttons_layout.addWidget(self.grid_button, 2,0)
            self.buttons_layout.addWidget(self.clear_button, 3,0)
            self.buttons_layout.addWidget(self.chart_title, 4,0)
            self.buttons_layout.addWidget(self.xy_units, 5,0)
            self.buttons_layout.addWidget(self.z_units, 6,0)
            self.buttons_layout.addWidget(self.x_lbl, 1,1)
            self.buttons_layout.addWidget(self.xcombo, 2,1)
            self.buttons_layout.addWidget(self.y_lbl, 3,1)
            self.buttons_layout.addWidget(self.ycombo, 4,1)
            self.buttons_layout.addWidget(self.z_lbl, 5,1)
            self.buttons_layout.addWidget(self.zcombo, 6,1)
            self.buttons_layout.addWidget(self.xint_lbl, 1,2)
            self.buttons_layout.addWidget(self.xint_box, 2,2)
            self.buttons_layout.addWidget(self.yint_lbl, 3,2)
            self.buttons_layout.addWidget(self.yint_box, 4,2)
            


            
                    
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

            
            #self.xlabel = QtGui.QInputDialog.getText(self, 'X-axis Label')
            
            #Button_layout is a QT desginer Grid Layout.
            self.toolbar_grid.addWidget(self.navi_toolbar)
            self.button_grid()
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