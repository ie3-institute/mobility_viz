import logging

from emob_viz.Source import Source
from emob_viz.model.Poi import Poi

source = Source.with_defaults("postgres", "postgres", "postgres1234!")
try:
    connection = source.get_connection()

    # Query poi from database
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM novagent.poi LIMIT 5;")
    data = cursor.fetchall()

    # Convert models
    poi = [Poi.from_tuple(row) for row in data]
    print(poi)

    # Don't forget to close the connection!
    connection.close()
except Exception as e:
    logging.error("Unable to connect to database.", e)
