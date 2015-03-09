import numpy as np

def rad_invdisttree(tree, xy, z, radius):
    print radius
    groups, distances = tree.query_radius(xy, radius, return_distance=True)
    #groups2, distances2 = tree.query_radius(xy, radius*4, return_distance=True)

    interpol = np.zeros( (len(distances),) + np.shape(z[0]))
    interpol[interpol==0] = 4095

    jinterpol = 0
    i = 0
    for dist, ix in zip( distances, groups ):
        #print dist, ix
        if len(ix) == 0:
        #    if len(groups2[i]) == 0:
            wz = 4095
        #    else:
        #        w = 1 / distances2[i]**3
        #        w /= np.sum(w)
        #        wz = np.dot( w, z[groups2[i]])
        else:  # weight z s by 1/dist --
            w = 1 / dist**2
            w /= np.sum(w)
            wz = np.dot( w, z[ix])
        i +=1
        if np.isnan(wz):
            wz = 4095
        interpol[jinterpol] = wz
        jinterpol += 1
    return interpol