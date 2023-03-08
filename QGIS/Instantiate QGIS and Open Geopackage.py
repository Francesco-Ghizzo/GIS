# Imports

from osgeo import ogr

import qgis

from qgis.core import (QgsMapClippingRegion,
   QgsMapClippingUtils,
   QgsMapSettings,
   QgsRenderContext,
   QgsGeometry,
   QgsVectorLayer,
   QgsCoordinateTransform,
   QgsCoordinateReferenceSystem,
   QgsProject,
   QgsMapToPixel,
   QgsMapLayerType
)

from qgis.testing import start_app

start_app()

''' Output sample:

Application state:
QGIS_PREFIX_PATH env var:		
Prefix:		/Applications/QGIS-LTR.app/Contents/MacOS/bin
Plugin Path:		/Applications/QGIS-LTR.app/Contents/MacOS/bin/../PlugIns/qgis
Package Data Path:	/Applications/QGIS-LTR.app/Contents/MacOS/bin/../Resources
Active Theme Name:	
Active Theme Path:	/Applications/QGIS-LTR.app/Contents/MacOS/bin/../Resources/resources/themes//icons/
Default Theme Path:	:/images/themes/default/
SVG Search Paths:	/Applications/QGIS-LTR.app/Contents/MacOS/bin/../Resources/svg/
		/var/folders/rt/k30tjkvx04vdq1qxvtwsb47m0000gn/T/QGIS-PythonTestConfigPath-xdfmtwwh/profiles/default/svg/
User DB Path:	/Applications/QGIS-LTR.app/Contents/MacOS/bin/../Resources/resources/qgis.db
Auth DB Path:	/var/folders/rt/k30tjkvx04vdq1qxvtwsb47m0000gn/T/QGIS-PythonTestConfigPath-xdfmtwwh/profiles/default/qgis-auth.db

'''

# Input Layer

inputFileName = "Cobertura_uso_terra_Brasil.gpkg"

inputFolder = "/Users/francescoghizzo/Documents/DEEP ESG/Extração e Processamento/Cobertura_uso_terra_Brasil"

inputFile = inputFolder + '/' + inputFileName

inputDataSource = ogr.Open(inputFile, update=True)

def ListAllLayers( self ):
    for layer in range(self.GetLayerCount()):
        print('Layer [', layer, ']: ', self.GetLayerByIndex(layer).GetName())

ogr.DataSource.ListAllLayers = ListAllLayers

inputDataSource.ListAllLayers()

''' Output sample:
    
Layer [ 0 ]:  uso2020_14
Layer [ 1 ]:  uso2020_13
Layer [ 2 ]:  uso2020_12
Layer [ 3 ]:  uso2020_11
Layer [ 4 ]:  uso2020_10
Layer [ 5 ]:  uso2020_9
Layer [ 6 ]:  uso2020_6
Layer [ 7 ]:  uso2020_5
Layer [ 8 ]:  uso2020_4
Layer [ 9 ]:  uso2020_3
Layer [ 10 ]:  uso2020_2
Layer [ 11 ]:  uso2020_1

'''

Layer9 = inputDataSource.GetLayerByName('uso2020_9')
