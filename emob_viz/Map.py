import os

import folium


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

    def save(self):
        target_file_path = os.path.join(self.target, self.file_name)
        if not os.path.exists(self.target):
            os.mkdir(self.target, False)
        self.map.save(target_file_path)
