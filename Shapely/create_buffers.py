'''
Open a geopackage with a polygon layer, create a buffer and save in the same geopackage as a different layer.
Example:
$ python create_buffers.py osm_polygon_buffers.gpkg 100
'''

import sys
import fiona
import shapely
from shapely.ops import unary_union
from shapely.geometry import shape, mapping

input_filename = "osm_polygon_buffers.gpkg"     # input_filename = sys.argv[1]
distance=100        # distance = int(sys.argv[2])

with fiona.open(input_filename, mode='r') as input_vector:
    input_layer = fiona.listlayers(input_filename)[0]

with fiona.open(input_filename, mode='r', layer=input_layer) as input_vector:
    driver = input_vector.driver
    input_geometries = [shape(element['geometry']) for element in list(input_vector)]     # list of polygons

buffer_layer = shapely.buffer(geometry=input_geometries, distance=distance, cap_style='round', join_style='round')

buffer_layer_dissolved = unary_union(buffer_layer)

output_geometries = list(buffer_layer_dissolved.geoms)      # MultiPolygon to list of polygons

output_filename = input_filename

output_layer = input_layer + "_buffer" + str(distance)

schema = {
    "geometry": "Polygon", "properties": {"id": "int"}
}

crs = "ESRI:102032"

with fiona.open(output_filename, mode='w', driver=driver, schema=schema, crs=crs, layer=output_layer) as output_vector:
    for id, geom in enumerate(output_geometries):
        output_vector.write({"geometry": mapping(geom), "properties": {"id": id}})
