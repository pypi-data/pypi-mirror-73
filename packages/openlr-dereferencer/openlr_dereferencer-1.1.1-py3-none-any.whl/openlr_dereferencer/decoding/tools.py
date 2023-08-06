"Some tooling functions for path and offset handling"

from math import degrees
from typing import List
from logging import debug
from shapely.geometry import LineString, Point
from openlr import Coordinates, LocationReferencePoint
from .routes import Route, PointOnLine
from ..maps.wgs84 import project_along_path, bearing


def remove_offsets(path: Route, p_off: float, n_off: float) -> Route:
    """Remove start+end offsets, measured in meters, from a route and return the result"""
    debug(f"Will consider positive offset = {p_off} m and negative offset {n_off} m.")
    lines = path.lines
    debug(f"This routes consists of {lines} and is {path.length()} m long.")
    # Remove positive offset
    debug(f"first line's offset is {path.absolute_start_offset}")
    remaining_poff = p_off + path.absolute_start_offset
    while remaining_poff >= lines[0].length:
        debug(f"Remaining positive offset {remaining_poff} is greater than "
              f"the first line. Removing it.")
        remaining_poff -= lines.pop(0).length
        if not lines:
            raise LRDecodeError("Offset is bigger than line location path")
    # Remove negative offset
    remaining_noff = n_off + path.absolute_end_offset
    while remaining_noff >= lines[-1].length:
        debug(f"Remaining negative offset {remaining_noff} is greater than "
              f"the last line. Removing it.")
        remaining_noff -= lines.pop().length
        if not lines:
            raise LRDecodeError("Offset is bigger than line location path")
    start_line = lines.pop(0)
    if lines:
        end_line = lines.pop()
    else:
        end_line = start_line
    return Route(
        PointOnLine(start_line, remaining_poff / start_line.length),
        lines,
        PointOnLine(end_line, 1.0 - remaining_noff / end_line.length)
    )


class LRDecodeError(Exception):
    "An error that happens through decoding location references"


def coords(lrp: LocationReferencePoint) -> Coordinates:
    "Return the coordinates of an LRP"
    return Coordinates(lrp.lon, lrp.lat)


def project(line_string: LineString, coord: Coordinates) -> float:
    """Computes the nearest point to `coord` on the line
    
    Returns:
        The place on `line_string` where this nearest point resides, as
        a fractional value in [ 0.0 .. 1.0 ], where 0.0 specifies the
        starting and 1.0 the ending point."""
    return line_string.project(Point(coord.lon, coord.lat), normalized=True)


def linestring_coords(line: LineString) -> List[Coordinates]:
    "Returns the edges of the line geometry as Coordinate list"
    return [Coordinates(*point) for point in line.coords]


def compute_bearing(
        lrp: LocationReferencePoint,
        candidate: PointOnLine,
        is_last_lrp: bool,
        bear_dist: float
) -> float:
    "Returns the bearing angle of a partial line in degrees in the range 0.0 .. 360.0"
    line1, line2 = candidate.split()
    if is_last_lrp:
        if line1 is None:
            return 0.0
        coordinates = linestring_coords(line1)
        coordinates.reverse()
        relative_offset = 1.0 - candidate.relative_offset
    else:
        if line2 is None:
            return 0.0
        coordinates = linestring_coords(line2)
        relative_offset = candidate.relative_offset
    absolute_offset = candidate.line.length * relative_offset
    bearing_point = project_along_path(coordinates, absolute_offset + bear_dist)
    bear = bearing(coordinates[0], bearing_point)
    return degrees(bear) % 360
