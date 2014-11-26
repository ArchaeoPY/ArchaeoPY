import numpy as np
# Not to be confused with functions to be used on the Windows OS
# These window functions are similar to those found in the Windows toolbox of MATLAB
# Note that numpy has a couple of Window functions already:
# See: hamming, bartlett, blackman, hanning, kaiser
 
def tukeywin(window_length, alpha=0.5):
    '''The Tukey window, also known as the tapered cosine window, can be regarded as a cosine lobe of width \alpha * N / 2
    that is convolved with a rectangle window of width (1 - \alpha / 2). At \alpha = 1 it becomes rectangular, and
    at \alpha = 0 it becomes a Hann window.
 
    We use the same reference as MATLAB to provide the same results in case users compare a MATLAB output to this function
    output
 
    Reference
    ---------
 
     http://www.mathworks.com/access/helpdesk/help/toolbox/signal/tukeywin.html
 
    '''
    # Special cases
    if alpha <= 0:
        return np.ones(window_length) #rectangular window
    elif alpha >= 1:
        return np.hanning(window_length)
 
    # Normal case
    x = np.linspace(0, 1, window_length)
    w = np.ones(x.shape)
 
    # first condition 0 <= x < alpha/2
    first_condition = x<alpha/2
    w[first_condition] = 0.5 * (1 + np.cos(2*np.pi/alpha * (x[first_condition] - alpha/2) ))
 
    # second condition already taken care of
 
    # third condition 1 - alpha / 2 <= x <= 1
    third_condition = x>=(1 - alpha/2)
    w[third_condition] = 0.5 * (1 + np.cos(2*np.pi/alpha * (x[third_condition] - 1 + alpha/2))) 
 
    return w
    
def reduction2pole(a,sample_interval,traverse_interval,inclination,declination):
    
    """Computes Reduction to Pole of Magnetic Dataset
        a: 2-D Numpy array of data (valid for TotalField)
        
    """
    #X & Y Positions of Data
    x = np.arange(np.shape(a[1]))
    x = np.multiply(x,sample_interval)
    
    y = np.arange(np.shape(1[0]))
    y = np.multiply(y,traverse_interval)
    
    #No of samples reguired in each direction
    #should be greater than 110% of datapoints
    samp_x = np.ceil(len(x)*1.1)
    samp_y = np.ceil(len(y)*1.1)
    
    pad_x1 = np.floor((samp_x-len(x))/2.0)
    pad_x2 = np.ceil((samp_x-len(x))/2.0)
    pay_y1 = np.floor((samp_x-len(x))/2.0)
    pad_y2 = np.ceil((samp_y-len(y))/2.0)
    
    #X Padding
    
    mid_data = np.zeros(len(y),samp_x)
    mid_data[mid_data==0] = np.nan
    
    for count in np.arange(len(y)):
        firstpoint = a[i,0]
        costap = tukeywin(pad_y1*2,alpha=1)
        
        #Add Padded part of Y before data
        new_data[0:pad_y1,i] = first_point*costap[1:pad_y1]