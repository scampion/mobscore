# mobscore

	
Extract an OSM file to Sqlite

	
	spatialite_osm_raw -o data/belgium-latest.osm.pbf  -d belgium.sqlite

https://groups.google.com/g/spatialite-users/c/eCiJ7gD2VN0

```SQL
-- starting a Transaction
BEGIN;

-- creating a Spatial Table
CREATE TABLE osm_amenities (
node_id INTEGER PRIMARY KEY,
type TEXT NOT NULL);

-- adding a Geometry Column
SELECT AddGeometryColumn('osm_amenities', 'geom', 4326, 'POINT', 'XY');

-- creating a Spatial Index
SELECT CreateSpatialIndex('osm_amenities', 'geom');

SELECT CreateSpatialIndex('osm_nodes', 'Geometry');

-- populating the table by extracting all OSM amenities
INSERT INTO osm_amenities (node_id, type, geom)
SELECT t.node_id, t.v, geometry
FROM osm_node_tags AS t
JOIN osm_nodes AS n ON (t.node_id = n.node_id)
WHERE t.k = 'amenity';

-- confirming the pending Transaction
COMMIT;
```
