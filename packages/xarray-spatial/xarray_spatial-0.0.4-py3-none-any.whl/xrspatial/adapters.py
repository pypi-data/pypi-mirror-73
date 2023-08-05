import xarray as xr

def arcpy_raster_to_xarray():
    try:
        import arcpy
    except:
        print('arcpy is required to use this adapter')
        return

 
    '''
    Something like:

    import arcpy
    import numpy
    
    # Get input Raster properties
    inRas = arcpy.Raster('C:/data/inRaster')
    arr = arcpy.RasterToNumPyArray(inRas,nodata_to_value=0)

    lowerLeft = arcpy.Point(inRas.extent.XMin, inRas.extent.YMin)
    cellSize = ras.meanCellWidth
    
    # Convert Raster to numpy array
    
    # Calculate percentage of the row for each cell value
    arrSum = arr.sum(1)
    arrSum.shape = (arr.shape[0],1)
    arrPerc = (arr)/arrSum
    
    #Convert Array to raster (keep the origin and cellsize the same as the input)
    newRaster = arcpy.NumPyArrayToRaster(arrPerc,lowerLeft,cellSize,
                                         value_to_nodata=0)
    newRaster.save("C:/output/fgdb.gdb/PercentRaster")
    '''

