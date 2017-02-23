import fiona
import geopandas as gpd
from sqlalchemy import create_engine

from web.app.config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)

data_path = './shapefiles/gadm28_levels.gdb'

for layer_index, layer_name in enumerate(fiona.listlayers(data_path)):

    print "Currently working on layer {0}, called {1}".format(layer_index, layer_name)
    with gpd.read_file(data_path, layer=layer_index) as collection:
        try:
            print "About to write {0} to SQL".format(layer_name)
            collection.to_sql(name=table_name, con=engine, index=False)
        except Exception as ex:
            print "there was a problem: {0}".format(ex)