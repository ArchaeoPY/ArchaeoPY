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

        def Open_File(self):
            self.fname = QtGui.QFileDialog.getOpenFileName()
            #self.f = open(self.fname, 'rb')
            with open(self.fname, 'r') as f:
                num_cols = len(f.readline().split('	'))-1
                f.seek(0)
                self.data = np.genfromtxt(f, names=True, delimiter='	',dtype=None,filling_values = np.nan, usecols=(range(0,num_cols)))

            self.x_val = self.data.dtype.names
            self.top_y = self.data.dtype.names
            self.middle_y = self.data.dtype.names
            self.bottom_y = self.data.dtype.names
            self.xcombo.clear()
            self.xcombo.addItems(self.x_val)
            self.top_ycombo.clear()
            self.top_ycombo.addItems(self.top_y)
            self.middle_ycombo.clear()
            self.middle_ycombo.addItems(self.middle_y)            
            self.bottom_ycombo.clear()
            self.bottom_ycombo.addItems(self.bottom_y)            
            
            #Clears Legend
            #self.legend_definitions()

        def legend_definitions(self):
            self.handles = []
            self.labels = []
            
            self.colors = itertools.cycle(["b", "g", "r","c","m","y","b"])
            self.markers = itertools.cycle([".","D","p","*","+"])
            
            self.legend = self.mpl.canvas.fig.legend(self.handles,self.labels,'upper right')
        
        def button_grid(self):
            #An Expanding Spacer Item to be used anywhere..
            #spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            #self.toolbar_grid.addItem(spacerItem, 0, 0, 1, 1)
            #self.toolbar_grid.addItem(spacerItem, 0, 4, 1, 1)

            #self.Grid_horizontal_Layout_2.addItem(spacerItem, 0)
            #self.Grid_horizontal_Layout_2.addItem(spacerItem, 4)

            #Layout for processing toolbbox
            self.file_properties_layout = QtGui.QGridLayout()
            self.file_properties_box = QtGui.QGroupBox()
            self.file_properties_box.setLayout(self.file_properties_layout)

            self.top_plot_layout = QtGui.QGridLayout()
            self.top_plot_box = QtGui.QGroupBox()
            self.top_plot_box.setLayout(self.top_plot_layout)
            
            self.middle_plot_layout = QtGui.QGridLayout()
            self.middle_plot_box = QtGui.QGroupBox()
            self.middle_plot_box.setLayout(self.middle_plot_layout)
            
            self.bottom_plot_layout = QtGui.QGridLayout()
            self.bottom_plot_box = QtGui.QGroupBox()
            self.bottom_plot_box.setLayout(self.bottom_plot_layout)
            
            #File Properties
            self.Grid_horizontal_Layout_2.addWidget(self.file_properties_box, 1)
            string = '<span style=" font-size:14pt;; font-weight:600;">File</span>'       
            self.file_properties_layout_text = QtGui.QLabel(string, self)            

            #Defines push buttons for file properties
            self.file_properties_buttons = QtGui.QButtonGroup()
            self.open_button = QtGui.QPushButton('Open', self)
            self.file_properties_buttons.addButton(self.open_button)
            self.open_button.clicked.connect(self.Open_File)
            
            self.plot_button = QtGui.QPushButton('Plot', self)
            self.file_properties_buttons.addButton(self.plot_button)
            #self.plot_button.clicked.connect(self.plot_button)            
            self.plot_button.clicked.connect(self.Plot_Function)
            #self.plot_button.clicked.connect(self.input_units)
            
            self.clear_button = QtGui.QPushButton('Clear', self)
            #self.top_fname = self.top_open_button.clicked.connect(self.Open_File)
            self.file_properties_buttons.addButton(self.clear_button)
            #self.file_properties_input = QtGui.QButtonGroup()
            #Defines combo boxes for File Properties
            self.file_properties_combo = QtGui.QButtonGroup()
            self.xcombo = QtGui.QComboBox()
            self.xcombo.addItems('X')
            self.xcombo_lbl = QtGui.QLabel('X Values', self)
            self.x_units = QtGui.QLineEdit(self)
            self.x_units_lbl = QtGui.QLabel("Input X Units", self)
            #self.x_units.setText("Input X Units")
                        
                   
            self.file_properties_layout.addWidget(self.file_properties_layout_text, 0,0,1,4)            
            self.file_properties_layout.addWidget(self.open_button, 1,0)
            self.file_properties_layout.addWidget(self.plot_button, 2,0)
            self.file_properties_layout.addWidget(self.clear_button, 3,0)
            
            self.file_properties_layout.addWidget(self.xcombo_lbl, 1,1)            
            self.file_properties_layout.addWidget(self.xcombo, 2,1)
            self.file_properties_layout.addWidget(self.x_units_lbl, 3,1)
            self.file_properties_layout.addWidget(self.x_units, 4,1)
            
            #Top Plot Box
            self.Grid_horizontal_Layout_2.addWidget(self.top_plot_box, 2)
            #self.toolbar_grid.addLayout(self.top_plot_layout, 0, 1, 1, 1)
            
            string = '<span style=" font-size:14pt;; font-weight:600;">Top Plot</span>'       
            self.top_plot_layout_text = QtGui.QLabel(string, self)
    
            self.top_ycombo = QtGui.QComboBox()
            self.top_ycombo.addItems('Y')
            self.top_ycombo_lbl = QtGui.QLabel('Y Values', self)
            self.y1_units = QtGui.QLineEdit(self)
            self.y1_units_lbl = QtGui.QLabel("Input Y Units", self)

            self.top_plot_layout.addWidget(self.top_plot_layout_text, 0,0,1,4)        
            self.top_plot_layout.addWidget(self.top_ycombo_lbl, 1,0)            
            self.top_plot_layout.addWidget(self.top_ycombo, 2,0)
            self.top_plot_layout.addWidget(self.y1_units_lbl, 3,0)
            self.top_plot_layout.addWidget(self.y1_units, 4,0)
                      
           #self.top_plot_layout.addItem(spacerItem, 0, 0, 1, 1)
           #self.top_plot_layout.addItem(spacerItem, 3, 0, 1, 1)
            
            
            #Middle Plot Box
            self.Grid_horizontal_Layout_2.addWidget(self.middle_plot_box, 3)
            #self.toolbar_grid.addLayout(self.middle_plot_layout, 0, 2, 1, 1)
            
            #Title of Box. HTML required to change colour & weight
            string = '<span style=" font-size:14pt;; font-weight:600;">Middle Plot</span>'       
            self.middle_plot_layout_text = QtGui.QLabel(string, self)
            
            self.middle_ycombo = QtGui.QComboBox()
            self.middle_ycombo.addItems('Y')
            self.middle_ycombo_lbl = QtGui.QLabel('Y Values', self)
            self.y2_units = QtGui.QLineEdit(self)
            self.y2_units_lbl = QtGui.QLabel("Input Y Units", self)


            self.middle_plot_layout.addWidget(self.middle_plot_layout_text, 0,0,1,4)            
            self.middle_plot_layout.addWidget(self.middle_ycombo_lbl, 1,0)            
            self.middle_plot_layout.addWidget(self.middle_ycombo, 2,0)
            self.middle_plot_layout.addWidget(self.y2_units_lbl, 3,0)
            self.middle_plot_layout.addWidget(self.y2_units, 4,0) 

           
            #Bottom Plot Selector Box
            self.Grid_horizontal_Layout_2.addWidget(self.bottom_plot_box, 4)
            #self.toolbar_grid.addLayout(self.bottom_plot_layout, 0, 3, 1, 1)
            #Title of Box. HTML required to change colour & weight
            string = '<span style=" font-size:14pt;; font-weight:600;">Bottom Plot</span>'       
            self.bottom_plot_layout_text = QtGui.QLabel(string, self)
            
            self.bottom_ycombo = QtGui.QComboBox()
            self.bottom_ycombo.addItems('Y')
            self.bottom_ycombo_lbl = QtGui.QLabel('Y Values', self)
            self.y3_units = QtGui.QLineEdit(self)
            self.y3_units_lbl = QtGui.QLabel("Input Y Units", self)


            self.bottom_plot_layout.addWidget(self.bottom_plot_layout_text, 0,0,1,4)
            self.bottom_plot_layout.addWidget(self.bottom_ycombo_lbl, 1,0)            
            self.bottom_plot_layout.addWidget(self.bottom_ycombo, 2,0)
            self.bottom_plot_layout.addWidget(self.y3_units_lbl, 3,0)
            self.bottom_plot_layout.addWidget(self.y3_units, 4,0)            
            
            
        def draw_plots(self):
            self.plot1 = self.mpl.canvas.fig.add_subplot(3,1,1)
            self.plot2 = self.mpl.canvas.fig.add_subplot(3,1,2, sharex=self.plot1)                       
            self.plot3 = self.mpl.canvas.fig.add_subplot(3,1,3, sharex=self.plot1)
                        
        def Plot_Function(self):        
            
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
            self.xval = self.data[self.data.dtype.names[self.xcombo.currentIndex()]]
            self.top_yval = self.data[self.data.dtype.names[self.top_ycombo.currentIndex()]]            
            self.middle_yval = self.data[self.data.dtype.names[self.middle_ycombo.currentIndex()]]  
            self.bottom_yval = self.data[self.data.dtype.names[self.bottom_ycombo.currentIndex()]]  
            
            self.mpl.canvas.fig.clear()
            
            
            self.plot1 = self.mpl.canvas.fig.add_subplot(3,1,1)
            #self.plot1.set_xlabel(self.x_units.text())
            self.plot1.set_ylabel(self.y1_units.text(), size=15)
            self.plot1.plot(self.xval,self.top_yval)
            
            self.plot2 = self.mpl.canvas.fig.add_subplot(3,1,2, sharex=self.plot1)
            #self.plot2.set_xlabel(self.x_units.text())
            self.plot2.set_ylabel(self.y2_units.text(), size=15)
            self.plot2.plot(self.xval,self.middle_yval)
            
            self.plot3 = self.mpl.canvas.fig.add_subplot(3,1,3, sharex=self.plot1)
            self.plot3.set_xlabel(self.x_units.text())
            self.plot3.set_ylabel(self.y3_units.text(),size=15)
            self.plot3.plot(self.xval, self.bottom_yval)
            
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
            self.draw_plots()
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