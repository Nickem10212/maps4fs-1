"""This module contains the base class for all map generation components."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from typing import TYPE_CHECKING, Any

import osmnx as ox  # type: ignore
from pyproj import Transformer
from shapely.geometry import Polygon, box  # type: ignore

from maps4fs.generator.qgis import save_scripts

if TYPE_CHECKING:
    from maps4fs.generator.game import Game


# pylint: disable=R0801, R0903, R0902, R0904
class Component:
    """Base class for all map generation components.

    Arguments:
        game (Game): The game instance for which the map is generated.
        coordinates (tuple[float, float]): The latitude and longitude of the center of the map.
        map_height (int): The height of the map in pixels.
        map_width (int): The width of the map in pixels.
        map_directory (str): The directory where the map files are stored.
        logger (Any, optional): The logger to use. Must have at least three basic methods: debug,
            info, warning. If not provided, default logging will be used.
    """

    def __init__(
        self,
        game: Game,
        coordinates: tuple[float, float],
        map_height: int,
        map_width: int,
        map_directory: str,
        logger: Any = None,
        **kwargs,  # pylint: disable=W0613, R0913, R0917
    ):
        self.game = game
        self.coordinates = coordinates
        self.map_height = map_height
        self.map_width = map_width
        self.map_directory = map_directory
        self.logger = logger
        self.kwargs = kwargs

        os.makedirs(self.previews_directory, exist_ok=True)
        os.makedirs(self.scripts_directory, exist_ok=True)
        os.makedirs(self.info_layers_directory, exist_ok=True)

        self.save_bbox()
        self.preprocess()

    def preprocess(self) -> None:
        """Prepares the component for processing. Must be implemented in the child class.

        Raises:
            NotImplementedError: If the method is not implemented in the child class.
        """
        raise NotImplementedError

    def process(self) -> None:
        """Launches the component processing. Must be implemented in the child class.

        Raises:
            NotImplementedError: If the method is not implemented in the child class.
        """
        raise NotImplementedError

    def previews(self) -> list[str]:
        """Returns a list of paths to the preview images. Must be implemented in the child class.

        Raises:
            NotImplementedError: If the method is not implemented in the child class.
        """
        raise NotImplementedError

    @property
    def previews_directory(self) -> str:
        """The directory where the preview images are stored.

        Returns:
            str: The directory where the preview images are stored.
        """
        return os.path.join(self.map_directory, "previews")

    @property
    def info_layers_directory(self) -> str:
        """The directory where the info layers are stored.

        Returns:
            str: The directory where the info layers are stored.
        """
        return os.path.join(self.map_directory, "info_layers")

    @property
    def scripts_directory(self) -> str:
        """The directory where the scripts are stored.

        Returns:
            str: The directory where the scripts are stored.
        """
        return os.path.join(self.map_directory, "scripts")

    @property
    def generation_info_path(self) -> str:
        """The path to the generation info JSON file.

        Returns:
            str: The path to the generation info JSON file.
        """
        return os.path.join(self.map_directory, "generation_info.json")

    def info_sequence(self) -> dict[Any, Any]:
        """Returns the information sequence for the component. Must be implemented in the child
        class. If the component does not have an information sequence, an empty dictionary must be
        returned.

        Returns:
            dict[Any, Any]: The information sequence for the component.
        """
        return {}

    def commit_generation_info(self) -> None:
        """Commits the generation info to the generation info JSON file."""
        self.update_generation_info(self.info_sequence())

    def update_generation_info(self, data: dict[Any, Any]) -> None:
        """Updates the generation info with the provided data.
        If the generation info file does not exist, it will be created.

        Arguments:
            data (dict[Any, Any]): The data to update the generation info with.
        """
        if os.path.isfile(self.generation_info_path):
            with open(self.generation_info_path, "r", encoding="utf-8") as file:
                generation_info = json.load(file)
                self.logger.debug("Loaded generation info from %s", self.generation_info_path)
        else:
            self.logger.debug(
                "Generation info file does not exist, creating a new one in %s",
                self.generation_info_path,
            )
            generation_info = {}

        updated_generation_info = deepcopy(generation_info)
        updated_generation_info[self.__class__.__name__] = data

        self.logger.debug("Updated generation info, now contains %s fields", len(data))

        with open(self.generation_info_path, "w", encoding="utf-8") as file:
            json.dump(updated_generation_info, file, indent=4)

        self.logger.debug("Saved updated generation info to %s", self.generation_info_path)

    def get_bbox(
        self,
        coordinates: tuple[float, float] | None = None,
        height_distance: int | None = None,
        width_distance: int | None = None,
        project_utm: bool = False,
    ) -> tuple[int, int, int, int]:
        """Calculates the bounding box of the map from the coordinates and the height and
        width of the map.
        If coordinates and distance are not provided, the instance variables are used.

        Arguments:
            coordinates (tuple[float, float], optional): The latitude and longitude of the center of
                the map. Defaults to None.
            height_distance (int, optional): The distance from the center of the map to the edge of
                the map in the north-south direction. Defaults to None.
            width_distance (int, optional): The distance from the center of the map to the edge of
                the map in the east-west direction. Defaults to None.
            project_utm (bool, optional): Whether to project the bounding box to UTM.

        Returns:
            tuple[int, int, int, int]: The bounding box of the map.
        """
        coordinates = coordinates or self.coordinates
        height_distance = height_distance or int(self.map_height / 2)
        width_distance = width_distance or int(self.map_width / 2)

        west, south, _, _ = ox.utils_geo.bbox_from_point(  # type: ignore
            coordinates, dist=height_distance, project_utm=project_utm
        )
        _, _, east, north = ox.utils_geo.bbox_from_point(  # type: ignore
            coordinates, dist=width_distance, project_utm=project_utm
        )
        bbox = north, south, east, west
        self.logger.debug(
            "Calculated bounding box for component: %s: %s, project_utm: %s, "
            "height_distance: %s, width_distance: %s",
            self.__class__.__name__,
            bbox,
            project_utm,
            height_distance,
            width_distance,
        )
        return bbox

    def save_bbox(self) -> None:
        """Saves the bounding box of the map to the component instance from the coordinates and the
        height and width of the map.
        """
        self.bbox = self.get_bbox(project_utm=False)
        self.logger.debug("Saved bounding box: %s", self.bbox)

    @property
    def new_bbox(self) -> tuple[float, float, float, float]:
        """This property is used for a new version of osmnx library, where the order of coordinates
        has been changed to (left, bottom, right, top).

        Returns:
            tuple[float, float, float, float]: The bounding box of the map in the new order:
                (left, bottom, right, top).
        """
        # FutureWarning: The expected order of coordinates in `bbox`
        # will change in the v2.0.0 release to `(left, bottom, right, top)`.
        north, south, east, west = self.bbox
        return west, south, east, north

    def get_espg3857_bbox(
        self, bbox: tuple[float, float, float, float] | None = None, add_margin: bool = False
    ) -> tuple[float, float, float, float]:
        """Converts the bounding box to EPSG:3857.
        If the bounding box is not provided, the instance variable is used.

        Arguments:
            bbox (tuple[float, float, float, float], optional): The bounding box to convert.
            add_margin (bool, optional): Whether to add a margin to the bounding box.

        Returns:
            tuple[float, float, float, float]: The bounding box in EPSG:3857.
        """
        bbox = bbox or self.bbox
        north, south, east, west = bbox
        transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
        epsg3857_north, epsg3857_west = transformer.transform(north, west)
        epsg3857_south, epsg3857_east = transformer.transform(south, east)

        if add_margin:
            MARGIN = 500  # pylint: disable=C0103
            epsg3857_north = int(epsg3857_north - MARGIN)
            epsg3857_south = int(epsg3857_south + MARGIN)
            epsg3857_east = int(epsg3857_east - MARGIN)
            epsg3857_west = int(epsg3857_west + MARGIN)

        return epsg3857_north, epsg3857_south, epsg3857_east, epsg3857_west

    def get_epsg3857_string(
        self, bbox: tuple[float, float, float, float] | None = None, add_margin: bool = False
    ) -> str:
        """Converts the bounding box to EPSG:3857 string.
        If the bounding box is not provided, the instance variable is used.

        Arguments:
            bbox (tuple[float, float, float, float], optional): The bounding box to convert.
            add_margin (bool, optional): Whether to add a margin to the bounding box.

        Returns:
            str: The bounding box in EPSG:3857 string.
        """
        north, south, east, west = self.get_espg3857_bbox(bbox, add_margin=add_margin)
        return f"{north},{south},{east},{west} [EPSG:3857]"

    def create_qgis_scripts(
        self, qgis_layers: list[tuple[str, float, float, float, float]]
    ) -> None:
        """Creates QGIS scripts from the given layers.
        Each layer is a tuple where the first element is a name of the layer and the rest are the
        bounding box coordinates in EPSG:3857.
        For filenames, the class name is used as a prefix.

        Arguments:
            qgis_layers (list[tuple[str, float, float, float, float]]): The list of layers to
                create scripts for.
        """
        class_name = self.__class__.__name__.lower()
        save_scripts(qgis_layers, class_name, self.scripts_directory)

    def get_polygon_center(self, polygon_points: list[tuple[int, int]]) -> tuple[int, int]:
        """Calculates the center of a polygon defined by a list of points.

        Arguments:
            polygon_points (list[tuple[int, int]]): The points of the polygon.

        Returns:
            tuple[int, int]: The center of the polygon.
        """
        polygon = Polygon(polygon_points)
        center = polygon.centroid
        return int(center.x), int(center.y)

    def absolute_to_relative(
        self, point: tuple[int, int], center: tuple[int, int]
    ) -> tuple[int, int]:
        """Converts a pair of absolute coordinates to relative coordinates.

        Arguments:
            point (tuple[int, int]): The absolute coordinates.
            center (tuple[int, int]): The center coordinates.

        Returns:
            tuple[int, int]: The relative coordinates.
        """
        cx, cy = center
        x, y = point
        return x - cx, y - cy

    def top_left_coordinates_to_center(self, top_left: tuple[int, int]) -> tuple[int, int]:
        """Converts a pair of coordinates from the top-left system to the center system.
        In top-left system, the origin (0, 0) is in the top-left corner of the map, while in the
        center system, the origin is in the center of the map.

        Arguments:
            top_left (tuple[int, int]): The coordinates in the top-left system.

        Returns:
            tuple[int, int]: The coordinates in the center system.
        """
        x, y = top_left
        cs_x = x - self.map_width // 2
        cs_y = y - self.map_height // 2

        return cs_x, cs_y

    def fit_polygon_into_bounds(
        self, polygon_points: list[tuple[int, int]], margin: int = 0
    ) -> list[tuple[int, int]]:
        """Fits a polygon into the bounds of the map.

        Arguments:
            polygon_points (list[tuple[int, int]]): The points of the polygon.
            margin (int, optional): The margin to add to the polygon. Defaults to 0.

        Returns:
            list[tuple[int, int]]: The points of the polygon fitted into the map bounds.
        """
        min_x = min_y = 0
        max_x, max_y = self.map_width, self.map_height

        # Create a polygon from the given points
        polygon = Polygon(polygon_points)

        if margin:
            polygon = polygon.buffer(margin, join_style="mitre")

        # Create a bounding box for the map bounds
        bounds = box(min_x, min_y, max_x, max_y)

        # Intersect the polygon with the bounds to fit it within the map
        fitted_polygon = polygon.intersection(bounds)

        if not isinstance(fitted_polygon, Polygon):
            raise ValueError("The fitted polygon is not a valid polygon.")

        # Return the fitted polygon points
        return list(fitted_polygon.exterior.coords)

    def get_infolayer_path(self, layer_name: str) -> str | None:
        """Returns the path to the info layer file.

        Arguments:
            layer_name (str): The name of the layer.

        Returns:
            str | None: The path to the info layer file or None if the layer does not exist.
        """
        info_layer_path = os.path.join(self.info_layers_directory, f"{layer_name}.json")
        if not os.path.isfile(info_layer_path):
            self.logger.warning("Info layer %s does not exist", info_layer_path)
            return None
        return info_layer_path
