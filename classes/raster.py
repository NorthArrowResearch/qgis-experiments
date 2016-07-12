import gdal

import numpy as np
from os import path
# this allows GDAL to throw Python Exceptions
gdal.UseExceptions()

class Raster:
    def __init__(self, filepath):
        gdal.UseExceptions()
        self.errs = ""
        self.filename = path.basename(filepath)

        try:
            src_ds = gdal.Open( filepath )
            print "got it"
            # Read Raster Properties
            self.srcband = src_ds.GetRasterBand(1)
            self.bands = src_ds.RasterCount
            self.driver = src_ds.GetDriver().LongName
            self.gt = src_ds.GetGeoTransform()

            """ Turn a Raster with a single band into a 2D [x,y] = v array """
            self.array = self.srcband.ReadAsArray()
            self.dataType = self.srcband.DataType
            self.band_array = self.srcband.ReadAsArray()
            self.nodata = self.srcband.GetNoDataValue()
            self.min = self.srcband.GetMinimum()
            self.max = self.srcband.GetMaximum()
            self.proj = src_ds.GetProjection()
            self.left = self.gt[0]
            self.cellWidth = self.gt[1]
            self.top = self.gt[3]
            self.cellHeight = self.gt[5]
            self.cols = src_ds.RasterXSize
            self.rows = src_ds.RasterYSize

        except RuntimeError as e:
            print('Could not retrieve meta Data for %s' % filepath)
