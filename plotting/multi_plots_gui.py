import numpy as np
import sys
#from PyQt4 import QtCore
from PyQt4 import QtGui
#import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab
#import matplotlib.cm as cm
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
import itertools
from pandas import *

# import the MainWindow widget from the converted .ui files
from ArchaeoPY.GUI_Templates.plotter import Ui_MainWindow

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

            self.open_handler()


        def open_handler(self):
            if self.plot1_selector.isChecked():
                #Defines x and y values
                self.x1 = self.data.dtype.names
                self.y1 = self.data.dtype.names
                #Populates combo boxes with header names
                self.x1combo.clear()
                self.x1combo.addItems(self.x1)
                self.y1combo.clear()
                self.y1combo.addItems(self.y1)

            if self.plot2_selector.isChecked():
                #Defines x and y values
                self.x2 = self.data.dtype.names
                self.y2 = self.data.dtype.names
                #Populates combo boxes with header names
                self.x2combo.clear()
                self.x2combo.addItems(self.x2)
                self.y2combo.clear()
                self.y2combo.addItems(self.y2)

            if self.plot3_selector.isChecked():
                #Defines x and y values
                self.x3 = self.data.dtype.names
                self.y3 = self.data.dtype.names
                #Populates combo boxes with header names
                self.x3combo.clear()
                self.x3combo.addItems(self.x3)
                self.y3combo.clear()
                self.y3combo.addItems(self.y3)                        

            
        def Plot_Function(self):
            #self.mpl.canvas.fig.clear()
            #self.legend.remove()
            #Takes x and y values to plot from combo box selection
            self.x1val = self.data[self.data.dtype.names[self.x1combo.currentIndex()]]
            self.y1val = self.data[self.data.dtype.names[self.y1combo.currentIndex()]]
            self.x2val = self.data[self.data.dtype.names[self.x2combo.currentIndex()]]
            self.y2val = self.data[self.data.dtype.names[self.y2combo.currentIndex()]]
            self.x3val = self.data[self.data.dtype.names[self.x3combo.currentIndex()]]
            self.y3val = self.data[self.data.dtype.names[self.y3combo.currentIndex()]]            
            #self.yval = self.yval - np.median(self.yval)
            
            self.axes = self.canvas.fig.add_subplot

            self.plot1 = self.mpl.canvas.fig.add_subplot(3,1,1)
            self.plot2 = self.mpl.canvas.fig.add_subplot(3,1,2)
            self.plot3 = self.mpl.canvas.fig.add_subplot(3,1,3)            
            
            
            #Calculates stats info of y values
            #self.stats() 
         
            #self.plot1 = self.mpl.canvas.fig.add_subplot(3,1,1)
            #self.plot1.set_xlabel(self.x_units.text())
            #self.plot1.set_ylabel(self.y1_units.text(), size=15)
            self.plot1.axes.set_autoscale_on(True)
            self.plot1.axes.autoscale_view(True,True,True)
            self.plot1.plot(self.x1val,self.y1val)
            
            #self.plot2 = self.mpl.canvas.fig.add_subplot(3,1,2, sharex=self.plot1)
            #self.plot2.set_xlabel(self.x_units.text())
            #self.plot2.set_ylabel(self.y2_units.text(), size=15)
            self.plot2.plot(self.x2val,self.y2val)
            
            #self.plot3 = self.mpl.canvas.fig.add_subplot(3,1,3, sharex=self.plot1)
            #self.plot3.set_xlabel(self.x_units.text())
            #self.plot3.set_ylabel(self.y3_units.text(),size=15)
            self.plot3.plot(self.x3val, self.y3val)
            

            #temp_scatter = self.mpl.canvas.ax.scatter(self.xval,self.yval, color=self.marker_colour.currentText(),marker=self.marker_style.currentText())
            #self.handles.append(temp_scatter)
            #self.labels.append(self.data.dtype.names[self.ycombo.currentIndex()])
            #self.legend = self.mpl.canvas.fig.legend(self.handles,self.labels,'upper right')
            
            #self.mpl.canvas.ax.set_ylim(ymin=np.min(self.yval), ymax=(np.max(self.yval)))
            #self.mpl.canvas.ax.set_xlim(xmin=np.min(self.xval), xmax=np.max(self.xval))            
            #self.mpl.canvas.ax.set_autoscale_on(True)
            #self.mpl.canvas.ax.autoscale_view(True,True,True)
            #self.mpl.canvas.ax.set_xlabel(self.x_units.text(), size = 15)
            #self.mpl.canvas.ax.set_ylabel(self.y_units.text(), size=15)
            #self.mpl.canvas.ax.set_title(self.chart_title.text(), size=20)
            #self.mpl.canvas.ax.axis('auto')
            
            #Creates scatter plot

            #self.mpl.canvas.draw()
            
        
        def legend_definitions(self): #Handles legend
            self.handles = []
            self.labels = []
            
            #self.colors = itertools.cycle(["b","g","r","c","m","y","b"])
            #self.markers = itertools.cycle([".","D","p","*","+"])
            
            self.legend = self.mpl.canvas.fig.legend(self.handles,self.labels,'upper right')

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

                            
        def polyfit(self): #Calculates Polynomial Fit with Error Estimation
            #Calculate Poly Fit            
            self.order = self.poly_order.value()            
            self.p = np.polyfit(self.xval, self.yval, self.order)  #coefficients
            print self.order
            self.trend_y = np.polyval(self.p, self.xval) #fit values
            self.plot_trendline()
            
            #Calculate coeffecient of determination            
            self.residuals = np.subtract(self.yval, self.trend_y) #residuals
            self.RSS = np.sum(np.square(self.residuals)) #residual sum of squares
            self.TSS = np.sum(np.square(np.subtract(self.yval, np.mean(self.yval))))

            #Sends R-Squared value back to UI
            self.r_squared = str(np.round(np.subtract(1, np.divide(self.RSS, self.TSS)), decimals=3)) #send back to GUI
            self.r_squared_output.setText(self.r_squared) 

            #Sends trendline equation back to UI
            coeff1 = np.round(self.p[0], decimals=10)
            coeff1 = str(coeff1)
            coeff2 = np.round(self.p[1], decimals=8)
            coeff2 = str(coeff2)
            if self.order == 1:
                self.fit_equation = coeff1+'x + '+coeff2
                self.trendline_equation.setText(self.fit_equation) 
            if self.order == 2:
                coeff3 = np.round(self.p[2],decimals=3)
                coeff3 = str(coeff3)
                self.fit_equation = coeff1+'x^2 + '+coeff2+'x + '+coeff3
                self.trendline_equation.setText(self.fit_equation)
            if self.order == 3:
                coeff3 = np.round(self.p[2],decimals=5)
                coeff3 = str(coeff3)
                coeff4 = np.round(self.p[3],decimals=3)
                coeff4 = str(coeff4)
                self.fit_equation = coeff1+'x^3 + '+coeff2+'x^2 + '+coeff3+'x + '+coeff4
                self.trendline_equation.setText(self.fit_equation)    
            
                
        def plot_trendline(self): #Plots poly-line as solid line
            self.mpl.canvas.ax.plot(self.xval, self.trend_y, color=self.line_colour.currentText(), linestyle=self.line_style.currentText(), linewidth=self.line_width.value())            
            self.mpl.canvas.ax.set_ylim(ymin=np.min(self.yval), ymax=(np.max(self.yval)))
            self.mpl.canvas.ax.set_autoscale_on(True)
            self.mpl.canvas.ax.autoscale_view(True,True,True)
            self.mpl.canvas.ax.set_xlabel(self.x_units.text(), size = 15)
            self.mpl.canvas.ax.set_ylabel(self.y_units.text(), size=15)
            self.mpl.canvas.ax.set_title(self.chart_title.text(), size=20)
            #self.mpl.canvas.ax.set_ylabel(self.ytitle, size = 15)
            #self.mpl.canvas.ax.set_title(self.title, size = 15)
            #self.handles.append(trendline)
            #self.handles.append(poly_line)
            #self.poly_order_title = self.poly_order.text()
            #self.labels.append(self.poly_order_title + ' Order Polynomial')
            #self.legend = self.mpl.canvas.fig.legend(self.handles,self.labels,'upper right')
            self.mpl.canvas.draw()
        
                              
        def button_grid(self): #Defines button and layout 
            #self.firstrun=True
            self.plot_layout = QtGui.QGridLayout()
            self.plot_box = QtGui.QGroupBox()
            self.plot_box.setLayout(self.plot_layout)

            #self.plot2_layout = QtGui.QGridLayout()
            #self.plot2_box = QtGui.QGroupBox()
            #self.plot2_box.setLayout(self.plot2_layout)

            #self.plot3_layout = QtGui.QGridLayout()
            #self.plot3_box = QtGui.QGroupBox()
            #self.plot3_box.setLayout(self.plot3_layout)
            
            #self.stats_layout = QtGui.QGridLayout()
            #self.stats_box = QtGui.QGroupBox()
            #self.stats_box.setLayout(self.stats_layout)

            #self.plot_layout = QtGui.QGridLayout()
            #self.plot_box = QtGui.QGroupBox()
            #self.plot_box.setLayout(self.plot_layout)
            
            #File-Plot Options
            self.Grid_horizontal_Layout_2.addWidget(self.plot_box, 1)
            string = '<span style=" font-size:12pt;; font-weight:600;">File Options</span>'       
            self.plot_layout_text = QtGui.QLabel(string, self)             
            
            self.plot_buttons = QtGui.QButtonGroup()            
            self.open_button = QtGui.QPushButton('Open', self)
            self.plot_buttons.addButton(self.open_button)
            self.open_button.clicked.connect(self.Open_File)
            self.plot_button = QtGui.QPushButton('Plot', self)
            self.plot_buttons.addButton(self.plot_button)
            self.plot_button.clicked.connect(self.Plot_Function)
            self.clear_button = QtGui.QPushButton('Clear', self)
            self.plot_buttons.addButton(self.clear_button)
            self.clear_button.clicked.connect(self.ClearPlot)
            self.chart_title = QtGui.QLineEdit(self)
            self.chart_title.setText("Enter Chart Title")
            
            self.plot1_selector = QtGui.QRadioButton('Plot 1', self)
            self.plot2_selector = QtGui.QRadioButton('Plot 2', self)
            self.plot3_selector = QtGui.QRadioButton('Plot 3', self)
            
            
            self.x1combo = QtGui.QComboBox()
            self.x1combo.addItems('X')
            self.x1_lbl = QtGui.QLabel('Plot 1: X Values --')          
            
            self.y1combo = QtGui.QComboBox()
            self.y1combo.addItems('Y')
            self.y1_lbl = QtGui.QLabel('Plot 1: Y values --')

            self.x1_units = QtGui.QLineEdit(self)
            self.x1_units_lbl = QtGui.QLabel("X Units:", self)
            #self.connect(self.inputDlgBtn, QtCore.SIGNAL("clicked()"), self.openInputDialog)
            self.y1_units = QtGui.QLineEdit(self)
            self.y1_units_lbl = QtGui.QLabel("Y Units:", self)
            
            self.x2combo = QtGui.QComboBox()
            self.x2combo.addItems('X')
            self.x2_lbl = QtGui.QLabel('Plot 2 X Values --')          
            
            self.y2combo = QtGui.QComboBox()
            self.y2combo.addItems('Y')
            self.y2_lbl = QtGui.QLabel('Plot 2 Y values --')

            self.x2_units = QtGui.QLineEdit(self)
            self.x2_units_lbl = QtGui.QLabel("X Units:", self)
            #self.connect(self.inputDlgBtn, QtCore.SIGNAL("clicked()"), self.openInputDialog)
            self.y2_units = QtGui.QLineEdit(self)
            self.y2_units_lbl = QtGui.QLabel("Y Units:", self)
            
            self.x3combo = QtGui.QComboBox()
            self.x3combo.addItems('X')
            self.x3_lbl = QtGui.QLabel('Plot 3 X Values --')          
            
            self.y3combo = QtGui.QComboBox()
            self.y3combo.addItems('Y')
            self.y3_lbl = QtGui.QLabel('Plot 3 Y values --')

            self.x3_units = QtGui.QLineEdit(self)
            self.x3_units_lbl = QtGui.QLabel("X Units:", self)
            #self.connect(self.inputDlgBtn, QtCore.SIGNAL("clicked()"), self.openInputDialog)
            self.y3_units = QtGui.QLineEdit(self)
            self.y3_units_lbl = QtGui.QLabel("Y Units:", self)

            self.plot_layout.addWidget(self.plot_layout_text, 0,0,1,4)                      
            self.plot_layout.addWidget(self.plot1_selector, 1,0)
            self.plot_layout.addWidget(self.plot2_selector, 2,0)
            self.plot_layout.addWidget(self.plot3_selector, 3,0)            
            self.plot_layout.addWidget(self.open_button, 1,1)
            self.plot_layout.addWidget(self.plot_button, 2,1)
            self.plot_layout.addWidget(self.clear_button, 3,1)
            self.plot_layout.addWidget(self.chart_title, 4,1)
            self.plot_layout.addWidget(self.x1_lbl, 1,2)
            self.plot_layout.addWidget(self.x1combo, 2,2)
            self.plot_layout.addWidget(self.y1_lbl, 3,2)
            self.plot_layout.addWidget(self.y1combo, 4,2)
            self.plot_layout.addWidget(self.x1_units_lbl, 1,3)
            self.plot_layout.addWidget(self.x1_units, 2,3)            
            self.plot_layout.addWidget(self.y1_units_lbl, 3,3)            
            self.plot_layout.addWidget(self.y1_units, 4,3)
            self.plot_layout.addWidget(self.x2_lbl, 1,4)
            self.plot_layout.addWidget(self.x2combo, 2,4)
            self.plot_layout.addWidget(self.y2_lbl, 3,4)
            self.plot_layout.addWidget(self.y2combo, 4,4)
            self.plot_layout.addWidget(self.x2_units_lbl, 1,5)
            self.plot_layout.addWidget(self.x2_units, 2,5)            
            self.plot_layout.addWidget(self.y2_units_lbl, 3,5)            
            self.plot_layout.addWidget(self.y2_units, 4,5)
            self.plot_layout.addWidget(self.x3_lbl, 1,6)
            self.plot_layout.addWidget(self.x3combo, 2,6)
            self.plot_layout.addWidget(self.y3_lbl, 3,6)
            self.plot_layout.addWidget(self.y3combo, 4,6)
            self.plot_layout.addWidget(self.x3_units_lbl, 1,7)
            self.plot_layout.addWidget(self.x3_units, 2,7)            
            self.plot_layout.addWidget(self.y3_units_lbl, 3,7)            
            self.plot_layout.addWidget(self.y3_units, 4,7)

            #Plotting Properties
            '''self.Grid_horizontal_Layout_2.addWidget(self.plot_box, 1)
            string = '<span style=" font-size:12pt;; font-weight:600;">Plot Settings</span>'       
            self.plot_layout_text = QtGui.QLabel(string, self)
            self.plot_buttons = QtGui.QButtonGroup()
                        
            self.marker_style = QtGui.QComboBox()
            self.marker_style.addItems(('.', 'o', 'v', '^', '*', 'D', 'd'))
            self.marker_style_lbl = QtGui.QLabel('Marker Style', self)
            self.marker_colour = QtGui.QComboBox()
            self.marker_colour.addItems(('0.25', '0.5', '0.75', 'k', 'b', 'g', 'r', 'c', 'y', 'm'))
            self.marker_colour_lbl = QtGui.QLabel('Marker Colour', self)
             
            self.line_style = QtGui.QComboBox()
            self.line_style.addItems(('-', '--', ':','_'))
            self.line_style_lbl = QtGui.QLabel('Line Style', self)
            self.line_width = QtGui.QSpinBox()
            self.line_width.setRange(1,10)
            self.line_width_lbl = QtGui.QLabel('Line Width', self)
            self.line_colour = QtGui.QComboBox()
            self.line_colour.addItems(('r','b','g','c','y','m','0.25','0.5','0.75','k'))
            self.line_colour_lbl = QtGui.QLabel('Line Colour', self)
        
            self.plot_layout.addWidget(self.plot_layout_text, 0,0,1,4)
            self.plot_layout.addWidget(self.line_style_lbl, 1,0)
            self.plot_layout.addWidget(self.line_style, 1,1)
            self.plot_layout.addWidget(self.line_width_lbl, 2,0)
            self.plot_layout.addWidget(self.line_width, 2,1)
            self.plot_layout.addWidget(self.line_colour_lbl, 3,0)
            self.plot_layout.addWidget(self.line_colour,3,1)              
            self.plot_layout.addWidget(self.marker_style_lbl, 1,2)
            self.plot_layout.addWidget(self.marker_style, 1,3)
            self.plot_layout.addWidget(self.marker_colour_lbl, 2,2)
            self.plot_layout.addWidget(self.marker_colour, 2,3)
            

            #Stats Properties
            self.Grid_horizontal_Layout_2.addWidget(self.stats_box, 1)
            string = '<span style=" font-size:12pt;; font-weight:600;">Stats Settings</span>'       
            self.stats_layout_text = QtGui.QLabel(string, self)
            
            self.mean_output_lbl = QtGui.QLabel("Data Mean")            
            self.mean_output = QtGui.QLineEdit(self)
            
            self.median_output_lbl = QtGui.QLabel("Data Median")
            self.median_output = QtGui.QLineEdit(self)
            
            self.sd_lbl = QtGui.QLabel("Std Deviation")
            self.sd_output = QtGui.QLineEdit(self)
           
            self.stats_buttons = QtGui.QButtonGroup()            
            self.poly_label = QtGui.QLabel('Poly Fit')            
            #self.poly_fit = QtGui.QRadioButton('Poly Fit', self)            
            self.poly_order_text = QtGui.QLabel('Order', self)
            self.poly_order = QtGui.QSpinBox(self)
            self.poly_order.setRange(1, 10)  
            self.poly_plot_button = QtGui.QPushButton('Plot', self)
            self.stats_buttons.addButton(self.poly_plot_button)
            self.poly_plot_button.clicked.connect(self.polyfit)
            
            self.rolling_mean_radio = QtGui.QRadioButton('Rolling Mean', self)
            self.rolling_median_radio = QtGui.QRadioButton('Rolling Median', self) 
            self.moving_avg_window_text = QtGui.QLabel('Window')
            self.moving_avg_window = QtGui.QSpinBox(self)
            self.moving_avg_window.setRange(1,1000)
            self.moving_avg_plot = QtGui.QPushButton('Plot', self)
            self.moving_avg_plot.clicked.connect(self.moving_average_buttons)

            self.trendline_lbl = QtGui.QLabel("Trendline Equation")
            self.trendline_equation = QtGui.QLineEdit(self)
            self.r_squared_lbl = QtGui.QLabel("R Squared")            
            self.r_squared_output = QtGui.QLineEdit(self)
            
            self.stats_layout.addWidget(self.stats_layout_text, 0,0,1,4)
            self.stats_layout.addWidget(self.mean_output_lbl, 1,0)
            self.stats_layout.addWidget(self.mean_output, 1,1)
            self.stats_layout.addWidget(self.median_output_lbl, 1,2)
            self.stats_layout.addWidget(self.median_output, 1,3)
            self.stats_layout.addWidget(self.sd_lbl, 1,4)
            self.stats_layout.addWidget(self.sd_output, 1,5)            
            self.stats_layout.addWidget(self.poly_label, 2,0)
            self.stats_layout.addWidget(self.poly_order_text, 2,1)
            self.stats_layout.addWidget(self.poly_order, 2,2)
            self.stats_layout.addWidget(self.poly_plot_button,2,3)
            self.stats_layout.addWidget(self.rolling_mean_radio, 3,0)
            self.stats_layout.addWidget(self.rolling_median_radio, 3,1)
            self.stats_layout.addWidget(self.moving_avg_window_text,3,2)
            self.stats_layout.addWidget(self.moving_avg_window, 3,3)
            self.stats_layout.addWidget(self.moving_avg_plot, 3,4)
            self.stats_layout.addWidget(self.trendline_lbl, 5,0)
            self.stats_layout.addWidget(self.trendline_equation, 5,1)
            self.stats_layout.addWidget(self.r_squared_lbl, 5,2)
            self.stats_layout.addWidget(self.r_squared_output, 5,3)'''

            
                    
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
            #self.draw_plots()
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