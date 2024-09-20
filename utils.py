import math

from interfaces import PositionObject
from enums import Direction


def calculate_distance_between_two_points(point1: PositionObject, point2: PositionObject) -> float:
    c1 = point2.x - point1.x
    c2 = point2.y - point1.y

    return math.sqrt(c1**2 + c2**2)


def check_if_point_is_neighbour(center_point: PositionObject, point_to_check: PositionObject) -> bool:
    if center_point.x == point_to_check.x and abs(center_point.y - point_to_check.y) == 1:
        return True

    if center_point.y == point_to_check.y and abs(center_point.x - point_to_check.x) == 1:
        return True

    return False



def get_point_direction_relative(center_point: PositionObject, point_to_check: PositionObject) -> Direction:
    if center_point.x == point_to_check.x:
        if center_point.y < point_to_check.y:
            return Direction.UP.value
        else:
            return Direction.DOWN.value

    if center_point.y == point_to_check.y:
        if center_point.x < point_to_check.x:
            return Direction.RIGHT.value
        else:
            return Direction.LEFT.value

    raise Exception("Points are at a diagonal")