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
from emob_viz.model.Position import Position


def _get_data(con: object, start: datetime, end: datetime, sim_start: datetime):
    """
    Query the information from database
    :param con: Connection to the database
    :param start: Start datetime for the request
    :param end: End datetime for the request
    :param sim_start: Wall clock time of the simulation start
    :return: the given data
    """
    logging.debug(f"Querying ev positions between {start} and {end}.")

    # Determine minutes since simulation start
    start_minutes = int((start - sim_start).total_seconds() // 60)
    end_minutes = int((end - sim_start).total_seconds() // 60)
    print(f"Start minutes: {start_minutes}, end minutes: {end_minutes}")

    query = f"""
    SELECT "Time", "EV_Movements"."Id", "IsCharging", lat, lon
    FROM novagent."EV_Movements"
             JOIN novagent.poi ON LOWER("DestinationPoi") = LOWER(poi.id)
    WHERE "ArrivalOrDeparture" = 'arrival'
      AND "ParkingTimeStart" >= {start_minutes}
      AND "ParkingTimeStart" < {end_minutes}
      AND "DepartureTime" < {end_minutes};
    """
    cursor = con.cursor()
    cursor.execute(
        query
    )
    results = cursor.fetchall()
    logging.debug(f"Received {len(results)} ev positions between {start} and {end}.")
    return results


logging.getLogger().setLevel(logging.DEBUG)
source = Source.with_defaults("postgres", "postgres", "postgres1234!")
try:
    connection = source.get_connection()

    # Preparations to create a map
    output_dir = os.path.join("..", "output", "positions")
    simulation_start = datetime.datetime(2016, 1, 4, 0, 0, 0, 0)
    start_datetime = simulation_start
    simulation_end = datetime.datetime(2016, 1, 5, 0, 0, 0)
    dt = datetime.timedelta(0, 0, 0, 0, 15, 0, 0)

    # Collect results for later visualization
    time_steps = []
    time_coordinates = []

    while start_datetime < simulation_end:
        time_steps.append(start_datetime.strftime("%Y-%m-%d %H:%M"))
        window_end = start_datetime + dt

        data = _get_data(connection, start_datetime, window_end, simulation_start)

        # Convert models
        positions = [Position.from_tuple(row) for row in data]
        coordinates = list(map(lambda x: [x.lat, x.lon], positions))
        time_coordinates.append(coordinates)

        # Go on to the next window
        start_datetime = window_end

    # Create a map
    suffix = re.sub(":", "-", re.sub(" ", "_", str(start_datetime)))
    mp = Map(51.5127813, 7.4648609, 12, output_dir, f'position_map_with_time.html')
    mp.add_geojson(os.path.join("..", "input", "dortmund.geojson"))
    mp.add_positions_with_time(time_coordinates, time_steps)
    mp.save()

    # Don't forget to close the connection!
    connection.close()
except Exception as e:
    logging.error("Unable to connect to database.", e)
