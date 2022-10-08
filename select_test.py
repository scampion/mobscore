import sqlite3
conn = sqlite3.connect("belgium.sqlite")
conn.enable_load_extension(True)
conn.load_extension("/opt/homebrew/lib/mod_spatialite.dylib")
conn.execute("select InitSpatialMetadata(1)")


sql = f"""
SELECT * FROM osm_node_tags WHERE osm_node_tags.node_id in (
    SELECT pkid FROM idx_osm_nodes_Geometry
    WHERE xmin > 4.3027568
    AND xmax < 4.3187213
    AND ymin >  50.8997986
    AND ymax < 50.9047514
);
"""

cur = conn.execute(sql)
for r in cur.fetchall():
    print(r)

conn.commit()
conn.close()


