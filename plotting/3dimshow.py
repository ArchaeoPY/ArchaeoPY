import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from scipy import interpolate
from ArchaeoPY.Interp.invdisttree import rad_invdisttree, cartesian
from sklearn.neighbors import KDTree

from PIL import Image
    
fname = "C:/Users/fpopecarter.GSBPROSPECTION/OneDrive/Documents/NSGG/Carteasyn/topo2.txt"
imname = "C:/Users/fpopecarter.GSBPROSPECTION/OneDrive/Documents/NSGG/Carteasyn/1by1.png"
array = np.genfromtxt(fname, dtype=float)

array[:,0] = array[:,0]- np.min(array[:,0])
array[:,1] = array[:,1]- np.min(array[:,1])

print np.min(array[:,0]), np.min(array[:,1])
print np.max(array[:,0]), np.max(array[:,1])


x = np.arange(np.min(array[:,0]), np.max(array[:,0]), 1)
y = np.arange(np.min(array[:,1]), np.max(array[:,1]), 1)

tree = KDTree(np.column_stack((array[:,0],array[:,1])))

xyi = cartesian(([x[None,:]],[y[:,None]]))
xyi2 = np.array_split(xyi, 10)

za = np.empty(0, dtype=np.int)

for line in xyi2:
    print 'dealing with chunk'
    za= np.concatenate((za,rad_invdisttree(tree, line, array[:,2], 3)))
    
xyzi = np.column_stack((xyi, za))
i = np.lexsort((xyzi[:,0], xyzi[:,1]))
xyzi = xyzi[i]

print np.shape(xyzi[:,1])
print (len(y), len(x)), len(y)*len(x)


Z = np.reshape(xyzi[:,2], (len(y), len(x)))
#Z[Z==4095] = np.nan
Z[np.isnan(Z)] = 4095

#Z = np.repeat(Z, 30, axis=1)
#Z = np.repeat(Z, 30, axis=0)
#newKernel = interpolate.RectBivariateSpline(x,y,Z, kx=2,ky=2)

x = np.arange(np.min(array[:,0]), np.shape(Z)[1], 1)
y = np.arange(np.min(array[:,1]), np.shape(Z)[0], 1)

X, Y = np.meshgrid(x,y)
print np.shape(Z)

#Z = newKernel(x,y)
print np.shape(Z)

np.savetxt('nans.txt',Z)

Z[Z==4095] = np.nan

fig = plt.figure()
ax = Axes3D(fig)

im = Image.open(imname)
colors = im.convert("L")
colors = np.array(colors, dtype = float)
colors = colors / 255.0
colors=np.flipud(colors)
#colors = np.random.rand(len(y), len(x))
print np.shape(colors)

colors = colors.astype(str)
print colors

ax.plot_surface(X,Y,Z, rstride=1, facecolors=colors, cstride=1, cmap='Greys')
ax.view_init(elev=60, azim=130)
ax.set_zlim(bottom =1044 , top=1062)
ax.set_title('GNSS Data Collection')
ax.set_xlabel('East (m)')
ax.set_ylabel('North (m)')
ax.set_zlabel('height (m)')

m = plt.cm.ScalarMappable(cmap=plt.cm.Greys)
z = (-1, 2)
m.set_array(z)

fig.colorbar(m, shrink=0.5, aspect=5)
            
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
plt.show(block=True)