def geoplot_spreadsheet(filename, array, val_dimens, xbounds, ybounds, zbounds):

    array[array==1.70141e38] = float(2047.5)
    
    gridfile = open(filename, 'w')
#    print >> gridfile, 'DSAA'
#    print >> gridfile, str(val_dimens[0]) + ' ' + str(val_dimens[1])
#    print >> gridfile, str(xbounds[0]) + ' ' + str(xbounds[1])
#    print >> gridfile, str(ybounds[0]) + ' ' + str(ybounds[1])
#    print >> gridfile, str(zbounds[0]) + ' ' + str(zbounds[1])
#    print >> gridfile
    
    for row in array:
        #temp = list(row)
        #temp = ' '.join(temp)
        temp = ''
        delimiter = '   '
        #for item in row:
        print >> gridfile, delimiter.join(["%.3f" % (v) for v in row])
        #print >> gridfile
    gridfile.close()