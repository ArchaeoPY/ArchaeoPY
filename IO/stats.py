import numpy as np

def poly_fit(x_points, y_points, poly_order):
    p = np.polyfit(x_points, y_points, poly_order)
    return (x, np.polyval(p, x_points))
    