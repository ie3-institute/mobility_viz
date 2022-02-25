import logging
import os

import folium as folium

from emob_viz.Map import Map
from emob_viz.Source import Source
from emob_viz.model.Poi import Poi

source = Source.with_defaults("postgres", "postgres", "postgres1234!")
try:
    connection = source.get_connection()

    # Query poi from database
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM novagent.poi LIMIT 5;")
    data = cursor.fetchall()

    # Don't forget to close the connection!
    connection.close()

    # Convert models
    poi = [Poi.from_tuple(row) for row in data]
    print(poi)

    # Create a map
    mp = Map(51.5127813, 7.4648609, 12, 'output', 'poi_map.html')
    mp.save()
except Exception as e:
    logging.error("Unable to connect to database.", e)
