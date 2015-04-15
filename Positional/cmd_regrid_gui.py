import numpy as np
import sys
#from PyQt4 import QtCore
from PyQt4 import QtGui
#import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab
#import matplotlib.cm as cm
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar


# import the MainWindow widget from the converted .ui files
from ArchaeoPY.GUI_Templates.plotter import Ui_MainWindow
from ArchaeoPY.Positional.regrid_cmd import regrid_cmd

#import ArchaeoPY modules
#import stats
class ArchaeoPYMainWindow(QtGui.QMainWindow, Ui_MainWindow):

        
        """Customization for Qt Designer created window"""
    
        def ClearPlot(self):
            self.mpl.canvas.ax.clear()
            self.mpl.canvas.draw()
            #Clears Legend
                       
        def copy_to_clipboard(self):
            pixmap = QtGui.QPixmap.grabWidget(self.mpl.canvas)
            QtGui.QApplication.clipboard().setPixmap(pixmap)
        
        def Open_File(self):
            self.fname = QtGui.QFileDialog.getOpenFileName()
            #Opes File
            with open(self.fname, 'r') as f:
                self.num_cols = len(f.readline().split(','))
                f.seek(0)
                self.array = np.genfromtxt(f, dtype=float, delimiter=',', skiprows=1, filling_values=np.nan)

            self.chart_title.clear() #Display file path in GUI
            self.chart_title.setText(self.fname)
            #print self.array


        def regrid(self): #Regrid CMD data
            array = self.array #set data
            num_cols = self.num_cols #set number of columns
            fname = self.fname #set filename
            if self.hcp_config.isChecked: #set Coil orientation
                config = 'HCP'
            else:
                config = 'VCP'
            grid = self.grid.text() #set grid(s) to be regridded
            samples_int = float(self.samples_int.text()) #Sampling Interval
            samples_start = float(self.samples_start.text()) #Sample starting position
            samples_stop = float(self.samples_stop.text()) #Sample ending position
            no_samples = (samples_stop - samples_start + samples_int) / samples_int #number of amples down the line     
            traverses_start = float(self.trav_start.text()) #Starting traverse number
            traverses_stop = float(self.trav_stop.text()) #Ending traverse number
            no_traverses = (traverses_stop - traverses_start + float(self.trav_int.text())) / float(self.trav_int.text()) #Number of traverses
            
            #Regrid data
            regrid_cmd(fname, config, grid, array, num_cols, samples_start, samples_stop, no_samples, traverses_start, traverses_stop, no_traverses)
            
                              
        def button_grid(self): #Defines button and layout 
            #self.firstrun=True
            self.buttons_layout = QtGui.QGridLayout()
            self.buttons_box = QtGui.QGroupBox()
            self.buttons_box.setLayout(self.buttons_layout)

            self.survey_layout = QtGui.QGridLayout()
            self.survey_box = QtGui.QGroupBox()
            self.survey_box.setLayout(self.survey_layout)
        
            #File Properties
            self.Grid_horizontal_Layout_2.addWidget(self.buttons_box, 1)
            string = '<span style=" font-size:10pt;; font-weight:600;">File Settings</span>'       
            self.buttons_layout_text = QtGui.QLabel(string, self)             
            
            self.buttons = QtGui.QButtonGroup()            
            self.open_button = QtGui.QPushButton('Open', self)
            self.buttons.addButton(self.open_button)
            self.open_button.clicked.connect(self.Open_File)
            self.regrid_button = QtGui.QPushButton('Regrid', self)
            self.buttons.addButton(self.regrid_button)
            self.regrid_button.clicked.connect(self.regrid)
            self.clear_button = QtGui.QPushButton('Clear', self)
            self.buttons.addButton(self.clear_button)
            self.clear_button.clicked.connect(self.ClearPlot)
            self.chart_title = QtGui.QLineEdit(self)
            self.config_lbl = QtGui.QLabel('Orientation', self)
            self.hcp_config = QtGui.QRadioButton('HCP', self)
            self.vcp_config = QtGui.QRadioButton('VCP', self)
            self.grid = QtGui.QLineEdit(self)
            self.grid.setText('Enter Grid Number')
            

            self.buttons_layout.addWidget(self.buttons_layout_text, 0,0,1,4)                      
            self.buttons_layout.addWidget(self.open_button, 1,0)
            self.buttons_layout.addWidget(self.regrid_button, 2,0)
            self.buttons_layout.addWidget(self.clear_button, 3,0)
            self.buttons_layout.addWidget(self.chart_title, 4,0)
            self.buttons_layout.addWidget(self.config_lbl, 1,1)
            self.buttons_layout.addWidget(self.hcp_config, 2,1)
            self.buttons_layout.addWidget(self.vcp_config, 3,1)
            self.buttons_layout.addWidget(self.grid, 4,1)
            

            #survey parameters
            self.Grid_horizontal_Layout_2.addWidget(self.survey_box, 1)
            string = '<span style=" font-size:10pt;; font-weight:600;">Survey Parameters</span>'       
            self.survey_layout_text = QtGui.QLabel(string, self)
            self.survey_buttons = QtGui.QButtonGroup()
                               
            self.samples_start_lbl = QtGui.QLabel('Samples Start Position')
            self.samples_start = QtGui.QLineEdit(self)
        
            self.samples_stop_lbl = QtGui.QLabel('Samples End Position')
            self.samples_stop = QtGui.QLineEdit(self)

            self.samples_int_lbl = QtGui.QLabel('Sampling Interval')
            self.samples_int = QtGui.QLineEdit(self)

            self.trav_start_lbl = QtGui.QLabel('Traverses Start Position')
            self.trav_start = QtGui.QLineEdit(self)

            self.trav_stop_lbl = QtGui.QLabel('Traverses End Position')
            self.trav_stop = QtGui.QLineEdit(self)

            self.trav_int_lbl = QtGui.QLabel('Traverse Interval')
            self.trav_int = QtGui.QLineEdit(self)
                        
            self.survey_layout.addWidget(self.survey_layout_text, 0,0,1,2)
            self.survey_layout.addWidget(self.samples_start_lbl, 1,0)
            self.survey_layout.addWidget(self.samples_start, 1,1)
            self.survey_layout.addWidget(self.samples_stop_lbl, 2,0)
            self.survey_layout.addWidget(self.samples_stop, 2,1)
            self.survey_layout.addWidget(self.samples_int_lbl, 3,0)
            self.survey_layout.addWidget(self.samples_int,3,1)              
            self.survey_layout.addWidget(self.trav_start_lbl, 4,0)
            self.survey_layout.addWidget(self.trav_start, 4,1)
            self.survey_layout.addWidget(self.trav_stop_lbl, 5,0)
            self.survey_layout.addWidget(self.trav_stop, 5,1)
            self.survey_layout.addWidget(self.trav_int_lbl, 6,0)
            self.survey_layout.addWidget(self.trav_int, 6,1)

                  
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