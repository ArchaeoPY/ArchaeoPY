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

class TraverseMainWindow(QtGui.QMainWindow, Ui_MainWindow):

        def ClearPlot(self):
            self.mpl.canvas.ax.clear()
            self.mpl.canvas.draw()
            
        def copy_to_clipboard(self):
            pixmap = QtGui.QPixmap.grabWidget(self.mpl.canvas)
            QtGui.QApplication.clipboard().setPixmap(pixmap)        
                    
        def press_open(self):
            self.fname = QtGui.QFileDialog.getExistingDirectory(self, "Select Project")
            open_project(self.fname, self)
            self.statusbar.showMessage("press_open returned")
            self.repaint()

        def Open_File(self):
            self.fname = QtGui.QFileDialog.getOpenFileName()
            #self.f = open(self.fname, 'rb')
            with open(self.fname, 'r') as f:
                num_cols = len(f.readline().split('	'))-1
                f.seek(0)
                data = np.genfromtxt(f, names=True, delimiter='	',dtype=None,filling_values = np.nan, usecols=(range(0,num_cols)))
                return data
            #print data
            #print "beak"
            #return data
            #print data
            #print "break"
            
        def top_data(self):
            #print "beak"            
            self.top_data = self.Open_File()
            print self.top_data.dtype.names
            #print data
            self.top_x = self.top_data.dtype.names
            #print self.data[self.data.dtype.names[1]]
            #print self.data[self.data.dtype.names[2]]
            #return self.top_x
            self.top_y = self.top_data.dtype.names
            #return self.top_y
            self.top_xcombo.clear()
            self.top_xcombo.addItems(self.top_x)
            self.top_ycombo.clear()
            self.top_ycombo.addItems(self.top_y)
            
            
            #Clears Legend
            #self.legend_definitions()

        def legend_definitions(self):
            self.handles = []
            self.labels = []
            
            self.colors = itertools.cycle(["b", "g", "r","c","m","y","b"])
            self.markers = itertools.cycle([".","D","p","*","+"])
            
            self.legend = self.mpl.canvas.fig.legend(self.handles,self.labels,'upper right')

        def openInputDialog(self):
                    x_axis, result = QtGui.QInputDialog.getText(self, "X axis", "Specify units")
                    if result:
                        self.x_axis = x_axis
                    y_axis, result = QtGui.QInputDialog.getText(self, "Y axis", "Specify units")
                    if result:
                        self.y_axis = y_axis
        
        def button_grid(self):
            #An Expanding Spacer Item to be used anywhere..
            spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            self.toolbar_grid.addItem(spacerItem, 0, 0, 1, 1)
            self.toolbar_grid.addItem(spacerItem, 0, 4, 1, 1)

            #self.Grid_horizontal_Layout_2.addItem(spacerItem, 0)
            #self.Grid_horizontal_Layout_2.addItem(spacerItem, 4)

            #Layout for processing toolbbox
            self.top_plot_layout = QtGui.QGridLayout()
            self.top_plot_box = QtGui.QGroupBox()
            self.top_plot_box.setLayout(self.top_plot_layout)
            
            self.middle_plot_layout = QtGui.QGridLayout()
            self.middle_plot_box = QtGui.QGroupBox()
            self.middle_plot_box.setLayout(self.middle_plot_layout)
            
            self.bottom_plot_layout = QtGui.QGridLayout()
            self.bottom_plot_box = QtGui.QGroupBox()
            self.bottom_plot_box.setLayout(self.bottom_plot_layout)
            
            #Traverse selector grid box
            self.Grid_horizontal_Layout_2.addWidget(self.top_plot_box, 0)
            #self.toolbar_grid.addLayout(self.top_plot_layout, 0, 1, 1, 1)
            
            string = '<span style=" font-size:14pt;; font-weight:600;">Top Plot</span>'       
            self.top_plot_layout_text = QtGui.QLabel(string, self)
            
            #Defines push buttons for top plot 
            self.top_plot_buttons = QtGui.QButtonGroup()
            self.top_open_button = QtGui.QPushButton('Open', self)
            self.top_fname = self.top_open_button.clicked.connect(self.top_data)
            self.top_plot_buttons.addButton(self.top_open_button)
            self.top_plot_button = QtGui.QPushButton('Plot', self)
            #self.top_fname = self.top_open_button.clicked.connect(self.Open_File)
            self.top_plot_buttons.addButton(self.top_plot_button)
            self.top_clear_button = QtGui.QPushButton('Clear', self)
            #self.top_fname = self.top_open_button.clicked.connect(self.Open_File)
            self.top_plot_buttons.addButton(self.top_clear_button)
            self.top_plot_input = QtGui.QButtonGroup()
            self.top_units = QtGui.QPushButton('Input Units', self)
            self.top_units.clicked.connect(self.openInputDialog)

            #Defines combo boxes for top plot
            self.top_plot_combo = QtGui.QButtonGroup()
            self.top_xcombo = QtGui.QComboBox()
            self.top_xcombo.addItems('X')
            self.top_xcombo_lbl = QtGui.QLabel('X Values', self)
            self.top_ycombo = QtGui.QComboBox()
            self.top_ycombo.addItems('Y')
            self.top_ycombo_lbl = QtGui.QLabel('Y Values', self)
            

            self.top_plot_layout.addWidget(self.top_plot_layout_text, 0,0,1,4)            
            self.top_plot_layout.addWidget(self.top_open_button, 1,0)
            self.top_plot_layout.addWidget(self.top_plot_button, 2,0)
            self.top_plot_layout.addWidget(self.top_clear_button, 3,0)
            self.top_plot_layout.addWidget(self.top_units, 4,0)
            
            self.top_plot_layout.addWidget(self.top_xcombo_lbl, 1,1)            
            self.top_plot_layout.addWidget(self.top_xcombo, 2,1)
            self.top_plot_layout.addWidget(self.top_ycombo_lbl, 3,1)            
            self.top_plot_layout.addWidget(self.top_ycombo, 4,1)
                      
            self.top_plot_layout.addItem(spacerItem, 0, 0, 1, 1)
            self.top_plot_layout.addItem(spacerItem, 3, 0, 1, 1)
            
            #1st Pass Selector Box
            self.Grid_horizontal_Layout_2.addWidget(self.middle_plot_box, 1)
            #self.toolbar_grid.addLayout(self.middle_plot_layout, 0, 2, 1, 1)
            
            #Title of Box. HTML required to change colour & weight
            string = '<span style=" font-size:14pt;; font-weight:600;">Middle Plot</span>'       
            self.middle_plot_layout_text = QtGui.QLabel(string, self)
            
            self.middle_plot_buttons = QtGui.QButtonGroup()
            self.middle_open_button = QtGui.QPushButton('Open', self)
            self.middle_fname = self.middle_open_button.clicked.connect(self.top_data)
            self.middle_plot_buttons.addButton(self.middle_open_button)
            self.middle_plot_button = QtGui.QPushButton('Plot', self)
            #self.middle_fname = self.middle_open_button.clicked.connect(self.Open_File)
            self.middle_plot_buttons.addButton(self.middle_plot_button)
            self.middle_clear_button = QtGui.QPushButton('Clear', self)
            #self.middle_fname = self.middle_open_button.clicked.connect(self.Open_File)
            self.middle_plot_buttons.addButton(self.middle_clear_button)
            self.middle_plot_input = QtGui.QButtonGroup()
            self.middle_units = QtGui.QPushButton('Input Units', self)
            self.middle_units.clicked.connect(self.openInputDialog)

            #Defines combo boxes for middle plot
            self.middle_plot_combo = QtGui.QButtonGroup()
            self.middle_xcombo = QtGui.QComboBox()
            self.middle_xcombo.addItems('X')
            self.middle_xcombo_lbl = QtGui.QLabel('X Values', self)
            self.middle_ycombo = QtGui.QComboBox()
            self.middle_ycombo.addItems('Y')
            self.middle_ycombo_lbl = QtGui.QLabel('Y Values', self)
            

            self.middle_plot_layout.addWidget(self.middle_plot_layout_text, 0,0,1,4)            
            self.middle_plot_layout.addWidget(self.middle_open_button, 1,0)
            self.middle_plot_layout.addWidget(self.middle_plot_button, 2,0)
            self.middle_plot_layout.addWidget(self.middle_clear_button, 3,0)
            self.middle_plot_layout.addWidget(self.middle_units, 4,0)
            
            self.middle_plot_layout.addWidget(self.middle_xcombo_lbl, 1,1)            
            self.middle_plot_layout.addWidget(self.middle_xcombo, 2,1)
            self.middle_plot_layout.addWidget(self.middle_ycombo_lbl, 3,1)            
            self.middle_plot_layout.addWidget(self.middle_ycombo, 4,1)
 

           
            #Bottom Plot Selector Box
            self.Grid_horizontal_Layout_2.addWidget(self.bottom_plot_box, 2)
            #self.toolbar_grid.addLayout(self.bottom_plot_layout, 0, 3, 1, 1)
            #Title of Box. HTML required to change colour & weight
            string = '<span style=" font-size:14pt;; font-weight:600;">Bottom Plot</span>'       
            self.bottom_plot_layout_text = QtGui.QLabel(string, self)
            
            self.bottom_plot_buttons = QtGui.QButtonGroup()
            self.bottom_open_button = QtGui.QPushButton('Open', self)
            self.bottom_fname = self.bottom_open_button.clicked.connect(self.Open_File)
            self.bottom_plot_buttons.addButton(self.bottom_open_button)
            self.bottom_plot_button = QtGui.QPushButton('Plot', self)
            #self.bottom_fname = self.bottom_open_button.clicked.connect(self.Open_File)
            self.bottom_plot_buttons.addButton(self.bottom_plot_button)
            self.bottom_clear_button = QtGui.QPushButton('Clear', self)
            #self.bottom_fname = self.bottom_open_button.clicked.connect(self.Open_File)
            self.bottom_plot_buttons.addButton(self.bottom_clear_button)
            self.bottom_plot_input = QtGui.QButtonGroup()
            self.bottom_units = QtGui.QPushButton('Input Units', self)
            self.bottom_units.clicked.connect(self.openInputDialog)

            #Defines combo boxes for bottom plot
            self.bottom_plot_combo = QtGui.QButtonGroup()
            self.bottom_xcombo = QtGui.QComboBox()
            self.bottom_xcombo.addItems('X')
            self.bottom_xcombo_lbl = QtGui.QLabel('X Values', self)
            self.bottom_ycombo = QtGui.QComboBox()
            self.bottom_ycombo.addItems('Y')
            self.bottom_ycombo_lbl = QtGui.QLabel('Y Values', self)
            

            self.bottom_plot_layout.addWidget(self.bottom_plot_layout_text, 0,0,1,4)            
            self.bottom_plot_layout.addWidget(self.bottom_open_button, 1,0)
            self.bottom_plot_layout.addWidget(self.bottom_plot_button, 2,0)
            self.bottom_plot_layout.addWidget(self.bottom_clear_button, 3,0)
            self.bottom_plot_layout.addWidget(self.bottom_units, 4,0)
            
            self.bottom_plot_layout.addWidget(self.bottom_xcombo_lbl, 1,1)            
            self.bottom_plot_layout.addWidget(self.bottom_xcombo, 2,1)
            self.bottom_plot_layout.addWidget(self.bottom_ycombo_lbl, 3,1)            
            self.bottom_plot_layout.addWidget(self.bottom_ycombo, 4,1)
            
                        
                        
        def Plot_Function(self):
            
            '''
            Clears Matplotlib Widget Canvas
            
            Adds 3 subplots
            
            plots Difference Data
            
            sharex - shares x axis between subplots
            '''
            #self.legend.remove()            
            
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
            
            self.toolbar_grid.addWidget(self.navi_toolbar)
            
            #self.top_xval = self.top_data[self.top_data.dtype.names[self.top_xcombo.currentIndex()]]
            #self.top_yval = self.top_data[self.top_data.dtype.names[self.top_ycombo.currentIndex()]]
            #self.yval = self.yval - np.median(self.yval)            
            
            x1 = np.linspace(0.0, 5.0)
            y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
            y2 = np.cos(3 * np.pi * x1) * np.exp(-x1)
            y3 = np.cos(4 * np.pi * x1) * np.exp(-x1)
            self.mpl.canvas.fig.clear()
            
            self.plot1 = self.mpl.canvas.fig.add_subplot(3,1,1)
            #self.plot1.plot(self.top_xval,self.top_yval)
            
            self.plot2 = self.mpl.canvas.fig.add_subplot(3,1,2, sharex=self.plot1)
            self.plot2.plot(x1,y2)
            
            self.plot3 = self.mpl.canvas.fig.add_subplot(3,1,3, sharex=self.plot1)
            self.plot3.plot(x1,y3)
            
        def keyboard_Definitions(self):
           
            QtGui.QShortcut(QtGui.QKeySequence("Ctrl+P"),self, self.Plot_Function)

            QtGui.QShortcut(QtGui.QKeySequence("Ctrl+C"),self, self.copy_to_clipboard)
   
        def menubar_definitions(self):
             self.fname = self.Open_button.clicked.connect(self.Open_File)
            
            
        def __init__(self, parent = None):
            # initialization of the superclass
            super(TraverseMainWindow, self).__init__(parent)
            # setup the GUI --> function generated by pyuic4
            self.setupUi(self)
        
            #Button_layout is a QT desginer Grid Layout.
            
            self.keyboard_Definitions()
            self.Plot_Function()
            self.button_grid()
            
            self.statusbar.setEnabled(True)
            self.statusbar.showMessage("Ready")
            
if __name__=='__main__':
    #Creates Main UI window
    app = QtGui.QApplication(sys.argv)
    
    app.processEvents()
    
    #Creates Window Form     
    form = TraverseMainWindow()
    
    #display form and focus
    form.show()
    #if sys.platform == "darwin":
    form.raise_()
    
    app.exec_()