import sqlite3
conn = sqlite3.connect("belgium.sqlite")
conn.enable_load_extension(True)
conn.load_extension("/opt/homebrew/lib/mod_spatialite.dylib")
conn.execute("select InitSpatialMetadata(1)")

# conn.execute(
#     "SELECT AddGeometryColumn('museums', 'point_geom', 4326, 'POINT', 2);"
# )
# # Now update that geometry column with the lat/lon points
# conn.execute(
#     """
#     UPDATE museums SET
#     point_geom = GeomFromText('POINT('||"longitude"||' '||"latitude"||')',4326);
# """
# )
# # Now add a spatial index to that column

conn.execute(
    "SELECT CreateSpatialIndex('osm_nodes', 'Geometry');"
)
conn.commit()
conn.close()




