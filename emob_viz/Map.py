import os

import folium

from emob_viz.model.Poi import Poi


class Map:
    def __init__(self, center_lon: float, center_lat: float, zoom_start: float, target: str, file_name: str):
        """
        Create a mpa instance
        :param center_lon: Latitude of the map center
        :param center_lat: Longitude of the map center
        :param zoom_start: Zoom stage at the beginning
        :param target: Target directory path to write to
        :param file_name: File name to use
        """
        self.map = folium.Map(location=[center_lon, center_lat],
                              zoom_start=zoom_start)
        self.target = target
        self.file_name = file_name

    def add_pois(self, pois: list[Poi], color: str):
        for poi in pois:
            self.__add_poi(poi, color)

    def __add_poi(self, poi: Poi, color: str):
        self.__add_dot(poi.lon, poi.lat, poi.type, 20, color)

    def __add_dot(self, lon: float, lat: float, tooltip: str = None, radius: float = 20, color: str = "lightblue"):
        """
        Add a dot marker at the given location
        :param lon: Longitude
        :param lat: Latitude
        :param tooltip: Tool tip to be shown
        :param radius: Radius of the marker
        :param color: The color of the marker
        :return: nothing
        """
        folium.Circle((lat, lon), radius=radius, tooltip=tooltip, color = color).add_to(self.map)

    def save(self):
        target_file_path = os.path.join(self.target, self.file_name)
        if not os.path.exists(self.target):
            os.mkdir(self.target, False)
        self.map.save(target_file_path)
