import itertools
import logging

from emob_viz.Map import Map
from emob_viz.Source import Source
from emob_viz.model.Poi import Poi

source = Source.with_defaults("postgres", "postgres", "postgres1234!")
try:
    connection = source.get_connection()

    # Query poi from database
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM novagent.poi LIMIT 5;")
    # cursor.execute("SELECT * FROM novagent.poi;")
    data = cursor.fetchall()

    # Don't forget to close the connection!
    connection.close()

    # Convert models
    pois = [Poi.from_tuple(row) for row in data]
    pois_by_type = itertools.groupby(pois, lambda poi: poi.type)

    color_map = {
        "home": 'blue',
        "work": 'cadetblue',
        "bbpg": 'darkblue',
        "othershop": 'darkgreen',
        "religious": 'darkpurple',
        "sports": 'darkred',
        "medicinal": 'gray',
        "supermarket": 'green',
        "restaurant": 'lightblue',
        "services": 'lightgreen',
        "culture": 'orange'
    }

    # Create a map
    mp = Map(51.5127813, 7.4648609, 12, 'output', 'poi_map.html')
    for poi_type, type_pois in pois_by_type:
        type_pois = list(type_pois)
        color = color_map[poi_type]
        mp.add_pois(type_pois, color)
    mp.save()
except Exception as e:
    logging.error("Unable to connect to database.", e)
