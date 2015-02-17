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
        
        def press_open(self):
            self.fname = QtGui.QFileDialog.getExistingDirectory(self, "Select Project")
            open_project(self.fname, self)
            self.statusbar.showMessage("press_open returned")
            self.repaint()

        def button_grid(self):
            #An Expanding Spacer Item to be used anywhere..
            spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            self.toolbar_grid.addItem(spacerItem, 0, 0, 1, 1)
            self.toolbar_grid.addItem(spacerItem, 0, 4, 1, 1)

            #Layout for processing toolbbox
            self.Traverse_selector_layout = QtGui.QGridLayout()
            self.traverse_box = QtGui.QGroupBox()
            self.traverse_box.setLayout(self.Traverse_selector_layout)
            
            
            self.first_pass_layout = QtGui.QGridLayout()
            self.first_pass_box = QtGui.QGroupBox()
            self.first_pass_box.setLayout(self.first_pass_layout)
            
            self.second_pass_layout = QtGui.QGridLayout()
            self.second_pass_box = QtGui.QGroupBox()
            self.second_pass_box.setLayout(self.second_pass_layout)
            
            #Traverse selector grid box
            self.toolbar_grid.addWidget(self.traverse_box, 0, 1, 1, 1)
            #self.toolbar_grid.addLayout(self.Traverse_selector_layout, 0, 1, 1, 1)
            
            self.trav_no_text = QtGui.QLabel('Traverse Number', self)
            self.trav_no = QtGui.QSpinBox(self)
            self.trav_no.setRange(0, 9999)
            self.trav_no.setValue(1)
            
            self.cb_second_pass = QtGui.QCheckBox('Run Second Filter', self)
            self.cb_second_pass.setChecked(True)
            
            self.pb_save = QtGui.QPushButton('Save', self)
            
            
            self.Traverse_selector_layout.addWidget(self.trav_no_text, 1,0)
            self.Traverse_selector_layout.addWidget(self.trav_no,2,0)
            self.Traverse_selector_layout.addWidget(self.cb_second_pass,3,0)
            self.Traverse_selector_layout.addWidget(self.pb_save, 5,0)
            
            self.Traverse_selector_layout.addItem(spacerItem, 0, 0, 1, 1)
            self.Traverse_selector_layout.addItem(spacerItem, 3, 0, 1, 1)
            
            #1st Pass Selector Box
            self.toolbar_grid.addWidget(self.first_pass_box, 0, 2, 1, 1)
            #self.toolbar_grid.addLayout(self.first_pass_layout, 0, 2, 1, 1)
            #Title of Box. HTML required to change colour & weight
            string = '<span style=" font-size:14pt;; font-weight:600;">1st Pass</span>'       
            self.first_pass_layout_text = QtGui.QLabel(string, self)
            
            #Creates RadoButtons
            self.rb_1_radio_group = QtGui.QButtonGroup()
            self.rb_1_zero_median  = QtGui.QRadioButton('Zero Median', self)
            self.rb_1_radio_group.addButton(self.rb_1_zero_median)
            self.rb_1_linear_median  = QtGui.QRadioButton('Linear Median', self)
            self.rb_1_radio_group.addButton(self.rb_1_linear_median)
            self.rb_1_poly_median  = QtGui.QRadioButton('Poly Median', self)
            self.rb_1_radio_group.addButton(self.rb_1_poly_median)
            self.rb_1_roll_median  = QtGui.QRadioButton('Rolling Median', self)
            self.rb_1_radio_group.addButton(self.rb_1_roll_median)
            
            #Creates Spinboxes
            self.sb_1_neg_limit_text = QtGui.QLabel('Filter Lower Limit', self)
            self.sb_1_neg_limit = QtGui.QDoubleSpinBox(self)
            self.sb_1_neg_limit.setRange(-2047.5, 2047.5)
            self.sb_1_neg_limit.setValue(-15)
 
            self.sb_1_pos_limit_text = QtGui.QLabel('Filter Upper Limit', self)
            self.sb_1_pos_limit = QtGui.QDoubleSpinBox(self)
            self.sb_1_pos_limit.setRange(-2047.5, 2047.5)
            self.sb_1_pos_limit.setValue(15)
            
            #Adds radio & Spinboxes to 1st pass box
            self.first_pass_layout.addWidget(self.first_pass_layout_text, 0,0,1,4)
            self.first_pass_layout.addWidget(self.rb_1_zero_median, 1,0)
            self.first_pass_layout.addWidget(self.rb_1_linear_median, 2,0)
            self.first_pass_layout.addWidget(self.rb_1_poly_median, 3,0)
            self.first_pass_layout.addWidget(self.rb_1_roll_median, 4,0)
            
            self.first_pass_layout.addWidget(self.sb_1_neg_limit_text, 1,1)
            self.first_pass_layout.addWidget(self.sb_1_neg_limit, 2,1)
            self.first_pass_layout.addWidget(self.sb_1_pos_limit_text, 3,1)
            self.first_pass_layout.addWidget(self.sb_1_pos_limit, 4,1)
            
            
            #2nd Pass Selector Box
            self.toolbar_grid.addWidget(self.second_pass_box, 0, 3, 1, 1)
            #self.toolbar_grid.addLayout(self.second_pass_layout, 0, 3, 1, 1)
            #Title of Box. HTML required to change colour & weight
            string = '<span style=" font-size:14pt;; font-weight:600;">2nd Pass</span>'       
            self.second_pass_layout_text = QtGui.QLabel(string, self)
            
            #Creates RadoButtons
            self.rb_2_radio_group = QtGui.QButtonGroup()
            self.rb_2_zero_median  = QtGui.QRadioButton('Zero Median', self)
            self.rb_2_radio_group.addButton(self.rb_2_zero_median)
            self.rb_2_linear_median  = QtGui.QRadioButton('Linear Median', self)
            self.rb_2_radio_group.addButton(self.rb_2_linear_median)
            self.rb_2_poly_median  = QtGui.QRadioButton('Poly Median', self)
            self.rb_2_radio_group.addButton(self.rb_2_poly_median)
            self.rb_2_roll_median  = QtGui.QRadioButton('Rolling Median', self)
            self.rb_2_radio_group.addButton(self.rb_2_roll_median)
            
            #Creates Spinboxes
            self.sb_2_neg_limit_text = QtGui.QLabel('Filter Lower Limit', self)
            self.sb_2_neg_limit = QtGui.QDoubleSpinBox(self)
            self.sb_2_neg_limit.setRange(-2047.5, 2047.5)
            self.sb_2_neg_limit.setValue(-15)
 
            self.sb_2_pos_limit_text = QtGui.QLabel('Filter Upper Limit', self)
            self.sb_2_pos_limit = QtGui.QDoubleSpinBox(self)
            self.sb_2_pos_limit.setRange(-2047.5, 2047.5)
            self.sb_2_pos_limit.setValue(15)
            
            #Adds radio & Spinboxes to 1st pass box
            self.second_pass_layout.addWidget(self.second_pass_layout_text, 0,0,1,4)
            self.second_pass_layout.addWidget(self.rb_2_zero_median, 1,0)
            self.second_pass_layout.addWidget(self.rb_2_linear_median, 2,0)
            self.second_pass_layout.addWidget(self.rb_2_poly_median, 3,0)
            self.second_pass_layout.addWidget(self.rb_2_roll_median, 4,0)
            
            self.second_pass_layout.addWidget(self.sb_2_neg_limit_text, 1,1)
            self.second_pass_layout.addWidget(self.sb_2_neg_limit, 2,1)
            self.second_pass_layout.addWidget(self.sb_2_pos_limit_text, 3,1)
            self.second_pass_layout.addWidget(self.sb_2_pos_limit, 4,1)

            self.statusbar.setEnabled(True)
            self.statusbar.showMessage("Ready")
            
            
                        
        def plot_options(self):
            
            '''
            Clears Matplotlib Widget Canvas
            
            Adds 3 subplots
            
            plots Difference Data
            
            sharex - shares x axis between subplots
            '''
            x1 = np.linspace(0.0, 5.0)
            y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
            y2 = np.cos(3 * np.pi * x1) * np.exp(-x1)
            y3 = np.cos(4 * np.pi * x1) * np.exp(-x1)
            self.mpl.canvas.fig.clear()
            
            self.plot1 = self.mpl.canvas.fig.add_subplot(3,1,1)
            self.plot1.plot(x1,y1)
            
            self.plot2 = self.mpl.canvas.fig.add_subplot(3,1,2, sharex=self.plot1)
            self.plot2.plot(x1,y2)
            
            self.plot3 = self.mpl.canvas.fig.add_subplot(3,1,3, sharex=self.plot1)
            self.plot3.plot(x1,y3)
            
            self.button_grid()

            
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
            self.keyboard_Definitions()
            self.plot_options()
            
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