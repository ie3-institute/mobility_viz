import datetime
import itertools
import logging
import os.path
import re

from emob_viz.Map import Map
from emob_viz.Source import Source
from emob_viz.conversion.Html2Png import Html2Png
from emob_viz.conversion.Png2Gif import Png2Gif
from emob_viz.model.Movement import Movement


def _get_data(con: object, start: datetime, end: datetime):
    """
    Query the information from database
    :param con: Connection to the database
    :param start: Start datetime for the request
    :param end: End datetime for the request
    :return: the given data
    """
    logging.debug(f"Querying movements between {start} and {end}.")
    cursor = con.cursor()
    dtf = "%Y-%m-%dT%H:%M:%S"
    query = f"""
    SELECT "Time", "ArrivalOrDeparture", lat, lon
    FROM novagent."EV_Movements"
             JOIN novagent.poi on LOWER("DestinationPoi") = LOWER(poi.id)
    WHERE "Time" BETWEEN '{start.strftime(dtf)}' AND '{end.strftime(dtf)}' ORDER BY "Time";
    """
    cursor.execute(
        query
    )
    results = cursor.fetchall()
    logging.debug(f"Received {len(results)} movements between {start} and {end}.")
    return results


logging.getLogger().setLevel(logging.DEBUG)
source = Source.with_defaults("postgres", "postgres", "postgres1234!")
try:
    connection = source.get_connection()

    # Preparations to create a map
    color_map = {
        "arrival": 'blue',
        "departure": 'darkred'
    }
    output_dir = os.path.join("..", "output")
    converter = Html2Png(output_dir)
    start_datetime = datetime.datetime(2016, 1, 4, 0, 0, 0, 0)
    simulation_end = datetime.datetime(2016, 1, 11, 0, 0, 0)
    dt = datetime.timedelta(0, 0, 0, 0, 15, 0, 0)
    while start_datetime < simulation_end:
        window_end = start_datetime + dt

        data = _get_data(connection, start_datetime, window_end)

        # Convert models
        movements = [Movement.from_tuple(row) for row in data]
        movement_by_type = itertools.groupby(movements, lambda mvmt: mvmt.type)

        # Create a map
        suffix = re.sub(":", "-", re.sub(" ", "_", str(start_datetime)))
        mp = Map(51.5127813, 7.4648609, 12, output_dir, f'movement_map_{suffix}.html')
        mp.add_geojson(os.path.join("..", "input", "dortmund.geojson"))
        for mvmt_type, type_mvmts in movement_by_type:
            mvmts = list(type_mvmts)
            color = color_map[mvmt_type]
            mp.add_movements(mvmts, color)
        mp.add_text(start_datetime.strftime("%A, %d.%m.%Y - %H:%M"))
        mp.save()
        converter.convert(f'movement_map_{suffix}.html', delay=1, remove=True)

        # Go on to the next window
        start_datetime = window_end

    # Convert png's to gif
    Png2Gif(output_dir, output_dir).build_gif("movements")

    # Don't forget to close the connection!
    converter.close()
    connection.close()
except Exception as e:
    logging.error("Unable to connect to database.", e)
