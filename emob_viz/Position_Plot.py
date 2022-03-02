import datetime
import logging
import os.path

from emob_viz.Map import Map
from emob_viz.Source import Source
from emob_viz.model.Position import Position

import plotly.graph_objects as go


def _get_parked_evs(con: object, instant: datetime):
    """
    Query all arrivals, that happened until the questioned instant and where the departure is scheduled for a later time.
    :param con: Connection to the database
    :param instant: Start datetime for the request
    :return: the given data
    """
    logging.debug(f"Querying parked evs in {instant}.")

    query = f"""
    SELECT time, "EV_Movements".id, is_charging, lat, lon
    FROM novagent."EV_Movements"
             JOIN novagent.poi ON LOWER(destination_poi) = LOWER(poi.id)
    WHERE "EV_Movements".type = 'arrival'
      AND time <= '{instant}'
      AND scheduled_departure > '{instant}';
    """
    cursor = con.cursor()
    cursor.execute(
        query
    )
    results = cursor.fetchall()
    logging.debug(f"Received {len(results)} parked evs at {instant}.")
    return results


# Configuration
logging.getLogger().setLevel(logging.DEBUG)
source = Source.with_defaults("postgres", "postgres", "postgres1234!")
total_amount_of_evs = 10000.0

try:
    connection = source.get_connection()

    # Preparations to create a map
    output_dir = os.path.join("..", "output", "positions")
    start_datetime = datetime.datetime(2016, 1, 18, 0, 0, 0, 0)
    simulation_end = datetime.datetime(2016, 1, 19, 0, 0, 0, 0)
    dt = datetime.timedelta(0, 0, 0, 0, 15, 0, 0)

    # Collect results for later visualization
    time_steps = []
    time_coordinates_parking = []
    time_coordinates_charging = []

    while start_datetime < simulation_end:
        time_steps.append(start_datetime.strftime("%Y-%m-%d %H:%M"))
        window_end = start_datetime + dt

        data = _get_parked_evs(connection, start_datetime)

        # Convert models
        positions = [Position.from_tuple(row) for row in data]
        # All positions
        coordinates = list(map(lambda x: [x.lat, x.lon, 1.0 / total_amount_of_evs], positions))
        time_coordinates_parking.append(coordinates)
        # Position, where charging is made
        charging_positions = list(filter(lambda pos: pos.is_charging, positions))
        charging_coordinates = list(map(lambda x: [x.lat, x.lon], charging_positions))
        time_coordinates_charging.append(coordinates)

        # Go on to the next window
        start_datetime = window_end

    # Don't forget to close the connection!
    connection.close()

    # Get the maximum amount of parked evs within one instant and weigh the single instant accordingly
    min_parked_evs = float(min(map(lambda coords: len(coords), time_coordinates_parking)))
    max_parked_evs = float(max(map(lambda coords: len(coords), time_coordinates_parking)))
    logging.debug(f"At min / max, there are {min_parked_evs} / {max_parked_evs} evs parked in one instant.")

    # Create a map of all positions
    mp = Map(51.5127813, 7.4648609, 12, output_dir, f'position_map_with_time.html')
    mp.add_geojson(os.path.join("..", "input", "dortmund.geojson"))
    mp.add_positions_with_time(time_coordinates_parking, time_steps, 10.0 / 10000.0, 1500.0 / total_amount_of_evs)
    mp.save()

    # # Create a map with charging positions
    # mp = Map(51.5127813, 7.4648609, 12, output_dir, f'charging_map_with_time.html')
    # mp.add_geojson(os.path.join("..", "input", "dortmund.geojson"))
    # mp.add_positions_with_time(time_coordinates_charging, time_steps, 0.0, 300.0 / 10000.0)
    # mp.save()

    # Plot the portions of driving and parking evs
    amount_of_parking_evs = list(map(lambda x: len(x) / 10000.0 * 100.0, time_coordinates_parking))
    amount_of_driving_evs = [100.0 - x for x in amount_of_parking_evs]
    layout = go.Layout(xaxis=dict(title='Time'), yaxis=dict(title='Portion of EVs'))
    plot = go.Figure(data=[
        go.Bar(
            name='Parking EVs',
            x=time_steps,
            y=amount_of_parking_evs
        ),
        go.Bar(
            name='Driving EVs',
            x=time_steps,
            y=amount_of_driving_evs
        )
    ], layout=layout
    )
    plot.update_layout(barmode='stack')
    plot.show()
except Exception as e:
    logging.error("Unable to connect to database.", e)
