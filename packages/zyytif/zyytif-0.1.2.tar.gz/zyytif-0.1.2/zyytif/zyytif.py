#Author: Franklin
#Date: 7/10/2020
#Decription: 


import gdal
import ogr
from osgeo import gdal, gdalconst
import numpy as np
import threading


class ZYYTif:
    def __init__(self, path):
        self._path = path

        # Check the tif
        self._dataset = gdal.Open(self._path)
        if self._dataset == None:
            print('Can not open ' + self._path)
            raise Exception('Can not open ' + self._path)
        self._width = self._dataset.RasterXSize
        self._height = self._dataset.RasterYSize
        self._bandsCount = self._dataset.RasterCount
        self._geotrans = self._dataset.GetGeoTransform()
        self._proj = self._dataset.GetProjection()
        self._buffer = None
        self._jobs_process = []
        self._jobs_total = 0
        


    def _calculateRate(self, bands, startPoint, count, taskIndex):
        print(str(startPoint) + ":" + str(count))
        for yIndex in range(startPoint, startPoint + count, 1):
            for xIndex in range(self._width):
                count = 0
                for band in bands:
                    value = band.ReadAsArray(xIndex, yIndex, 1, 1)[0][0]
                    if str(value).find("e") > 0:
                        count = count + 1
                rate = count * 1.00000000 / self._bandsCount
                self._buffer[yIndex][xIndex] = rate
            self._jobs_process[taskIndex] = self._jobs_process[taskIndex] + 1
            allLoad = 0
            for item in self._jobs_process:
                allLoad = allLoad + item
            print("Threading [" + str(taskIndex) + "]: " + str(allLoad) + "/" + str(self._jobs_total) + " finished!")
        
    def checkNULL(self, output, jobs = 2):
        if jobs < 1:
            raise Exception("Illegal jobs setting!")
        bands = []
        for bandIndex in range(self._bandsCount):
            bands.append(self._dataset.GetRasterBand(bandIndex + 1))

        self._buffer = np.array([[0.0]*self._width]*self._height)

        length = int(self._height/jobs)
        lastCount = self._height - ((jobs-1)*length)

        tPool = []

        self._jobs_process = [0]*jobs
        self._jobs_total = self._height
        
        for index in range(jobs):
            t = None
            if index == (jobs - 1):
                t = threading.Thread(target=self._calculateRate, args=(bands, index*length, lastCount, index))
            else:
                t = threading.Thread(target=self._calculateRate, args=(bands, index*length, length, index))
            tPool.append(t)
            
        for t in tPool:
            t.start()

        for t in tPool:
            t.join()

        ZYYTif.WriteTiff(self._buffer, self._width, self._height, 1, self._geotrans, self._proj, output)

        self._buffer = None

    # Public method
    @staticmethod
    def WriteTiff(im_data, im_width, im_height, im_bands, im_geotrans, im_proj, path):
        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32

        if len(im_data.shape) == 3:
            im_bands, im_height, im_width = im_data.shape
        elif len(im_data.shape) == 2:
            im_data = np.array([im_data])
        else:
            im_bands, (im_height, im_width) = 1,im_data.shape
        driver = gdal.GetDriverByName("GTiff")
        dataset = driver.Create(path, im_width, im_height, im_bands, datatype)
        if(dataset!= None):
            dataset.SetGeoTransform(im_geotrans) 
            dataset.SetProjection(im_proj) 
        for i in range(im_bands):
            dataset.GetRasterBand(i+1).WriteArray(im_data[i])
        del dataset