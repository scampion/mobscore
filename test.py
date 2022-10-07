from pyproj import Transformer

transformer = Transformer.from_crs(crs_from=31370, crs_to=4326)
transformer.transform(146287.71013987, 177004.375537637)

from pyrosm import get_data

fp = get_data("belgium-latest", directory="data")

import pyrosm

bounding_box = [50.9029796618,4.305436024,50.9072718267,4.316397483,]
osm =  pyrosm.OSM('data/belgium-latest.osm.pbf', bounding_box=bounding_box)


import spatialite

db = spatialite.connect('belgium.sqlite')

pt = "POLYGON((50.9029796618 4.305436024, 50.9072718267 4.305436024, 50.9072718267,4.316397483, 50.9029796618 316397483))"

pt = "POLYGON((4.3077921 50.9050125, 4.3180060 50.9046336, 4.3077063 50.9016836, 4.3078350 50.904931))"
pt = "POLYGON((50.9050125 4.3077921, 50.9046336 4.3180060, 50.9016836 4.3077063,50.904931 4.3078350))"

SELECT node_id FROM osm_nodes WHERE Contains(Buffer(GeomFromText('POINT(4.3077921 50.9050125', 1 ), 0.1), osm_nodes.Geometry)
SELECT node_id FROM osm_nodes WHERE Contains(Buffer(GeomFromText('POINT(4.3077921 50.9050125)'), 0.0000000000001), osm_nodes.Geometry)

#pt = "POLYGON((4.3077921 50.9050125, 4.3180060 50.9046336, 4.3077063 50.9016836, 4.3078350 50.904931))"
#db.execute(f"SELECT node_id FROM osm_nodes WHERE within(GeomFromText('{ft}'), osm_nodes.Geometry)""").fetchone()
#r = db.execute(f"SELECT node_id FROM osm_nodes WHERE ST_Within(osm_nodes.Geometry, PolygonFromText('{ft}'))""").fetchall()


pt = "POLYGON((4.3077921 50.9050125, 4.3180060 50.9046336, 4.3077063 50.9016836, 4.3078350 50.904931))"
sql = """SELECT node_id FROM osm_nodes WHERE Contains(Buffer(GeomFromText('POINT(4.3077921 50.9050125)'), 0.01), osm_nodes.Geometry)"""
r = db.execute(sql).fetchall()
for row in r:
    for n in db.execute(f"SELECT * FROM osm_node_tags WHERE node_id = {row[0]}").fetchall():
        if n:
            print(n)

