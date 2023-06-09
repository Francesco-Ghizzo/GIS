''' Polygon '''

import fiona
import geopandas
import shapely.speedups
from shapely import geometry
from shapely.geometry import shape, mapping

input_filename = "osm_polygon_buffers.gpkg"

output_filename = "osm_polygon_buffers_difference.gpkg"

with fiona.open(input_filename, mode='r') as input_geopackage:
    input_layers = fiona.listlayers(input_filename)

input_layers

input_layer1 = input_layers[2]

input_layer2 = input_layers[4]

with fiona.open(input_filename, mode='r', layer=input_layer1) as layer1:
	layer1_polygons = [shape(element['geometry']) for element in list(layer1)]	# Collection (fiona.collection.Collection) to list of polygons
	layer1_geoseries = geopandas.GeoSeries(layer1_polygons)		# list of polygons to GeoSeries

with fiona.open(input_filename, mode='r', layer=input_layer2) as layer2:
	layer2_polygons = [shape(element['geometry']) for element in list(layer2)]	# Collection (fiona.collection.Collection) to list of polygons
	layer2_geoseries = geopandas.GeoSeries(layer2_polygons)		# list of polygons to GeoSeries

layer1_geoseries.sindex		# create spatial index

layer2_geoseries.sindex		# create spatial index

layer1_geodataframe = geopandas.GeoDataFrame(geometry=layer1_geoseries)

layer2_geodataframe = geopandas.GeoDataFrame(geometry=layer2_geoseries)

layer1_geoseries.index = geopandas.sjoin(layer1_geodataframe, layer2_geodataframe, how='left', predicate='within').index_right

# layer2_geoseries.index = geopandas.sjoin(layer2_geodataframe, layer0_geodataframe, how='left', predicate='Contains').index_right

difference_polygons = [polygon2.difference(layer1_geoseries[i]) for i, polygon2 in enumerate(layer2_polygons)]

# Cast to MultiPolygon

from shapely.geometry.multipolygon import MultiPolygon

def cast_to_multipolygon(geom):
	if type(geom) == geometry.polygon.Polygon:
		return geometry.multipolygon.MultiPolygon([geom])

difference_multipolygons = list(map(cast_to_multipolygon, difference_polygons))

output_layer = input_layer2

schema = {
	"geometry": "MultiPolygon", "properties": {"id": "int"}
}

with fiona.open(output_filename, mode='w', driver='GPKG', schema=schema, crs='ESRI:102032', layer=output_layer) as output_geopackage:
	for id, geoms in enumerate(difference_multipolygons):
		output_geopackage.write({"geometry": mapping(geoms), "properties": {"id": id}})




''' MultiPolygon '''

import fiona
import shapely.speedups
from shapely import geometry
from shapely.geometry import shape, mapping

input_filename = "osm_polygon_buffers_union.gpkg"

output_filename = "osm_polygon_buffers_difference.gpkg"

with fiona.open(input_filename, mode='r') as input_geopackage:
    input_layers = fiona.listlayers(input_filename)

input_layers

input_layer1 = input_layers[3]

input_layer2 = input_layers[5]

with fiona.open(input_filename, mode='r', layer=input_layer1) as layer1:
	layer1_as_list = list(layer1)		# Collection (fiona.collection.Collection) to list of dictionaries
	layer1_as_dict = layer1_as_list[0]
	layer1_multipolygon = shape(layer1_as_dict['geometry'])		# list of dictionaries to multipolygon

with fiona.open(input_filename, mode='r', layer=input_layer2) as layer2:
	layer2_as_list = list(layer2)		# Collection (fiona.collection.Collection) to list of dictionaries
	layer2_as_dict = layer2_as_list[0]
	layer2_multipolygon = shape(layer2_as_dict['geometry'])		# list of dictionaries to multipolygon

difference_multipolygon = layer2_multipolygon.difference(layer1_multipolygon)

difference_polygons = list(difference_multipolygon.geoms)

output_layer = input_layer2

schema = {
	"geometry": "Polygon", "properties": {"id": "int"}
}

with fiona.open(output_filename, mode='w', driver='GPKG', schema=schema, crs='ESRI:102032', layer=output_layer) as output_geopackage:
	for id, geom in enumerate(difference_polygons):
		output_geopackage.write({"geometry": mapping(geom), "properties": {"id": id}})