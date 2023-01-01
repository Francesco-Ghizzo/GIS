 # Imports

from osgeo import ogr

 # Driver

driverName = "ESRI Shapefile"

driver = ogr.GetDriverByName(driverName)

 # Input Layer

inputShapefileName = "Cobertura_uso_terra_Brasil-dissolve.shp"

inputShapefileFolder = "Cobertura_uso_terra_Brasil"

inputShapefile = inputShapefileFolder + '/' + inputShapefileName

inputDataSource = driver.Open(inputShapefile, 0)

inputLayer = inputDataSource.GetLayer()


 # Overlay Layer

overlayShapefileName = "BR_Municipios_2021.shp"

overlayShapefileFolder = "BR_Municipios_2021"

overlayShapefile = overlayShapefileFolder + '/' + overlayShapefileName

overlayDataSource = driver.Open(overlayShapefile, 0)

overlayLayer = overlayDataSource.GetLayer()


 # Clipped

outputShapefileName = "Cobertura_uso_terra_Brasil-clip.shp"

outputShapefileFolder = "Cobertura_uso_terra_Brasil"

outputShapefile = outputShapefileFolder + '/' + outputShapefileName

outputDataSource = driver.CreateDataSource(outputShapefile)

outputLayer = outputDataSource.CreateLayer('Cobertura_uso_terra_Brasil-clip', geom_type=ogr.wkbMultiPolygon)

ogr.Layer.Clip(inputLayer, overlayLayer, outputLayer)
