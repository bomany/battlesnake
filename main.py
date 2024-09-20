# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing

from interfaces import MoveRequestObject, SnakeObject
from enums import Direction
from utils import check_if_point_is_neighbour, get_point_direction_relative, calculate_distance_between_two_points


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: MoveRequestObject) -> typing.Dict:

    board = game_state.board
    my_snake: SnakeObject = game_state.you
    is_move_safe = {Direction.UP.value: True, Direction.DOWN.value: True, Direction.LEFT.value: True, Direction.RIGHT.value: True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = my_snake.body[0]  # Coordinates of your head
    my_neck = my_snake.body[1]  # Coordinates of your "neck"

    if my_neck.x < my_head.x:  # Neck is left of head, don't move left
        is_move_safe[Direction.LEFT.value] = False

    elif my_neck.x > my_head.x:  # Neck is right of head, don't move right
        is_move_safe[Direction.RIGHT.value] = False

    elif my_neck.y < my_head.y:  # Neck is below head, don't move down
        is_move_safe[Direction.DOWN.value] = False

    elif my_neck.y > my_head.y:  # Neck is above head, don't move up
        is_move_safe[Direction.UP.value] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = board.width
    board_height = board.height

    if my_head.x == 0:
        is_move_safe[Direction.LEFT.value] = False
    elif my_head.x == board_width - 1:
        is_move_safe[Direction.RIGHT.value] = False

    if my_head.y == 0:
        is_move_safe[Direction.DOWN.value] = False
    elif my_head.y == board_height - 1:
        is_move_safe[Direction.UP.value] = False


    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = my_snake.body
    for block in my_body:
        if check_if_point_is_neighbour(my_head, block):
            direction = get_point_direction_relative(my_head, block)
            is_move_safe[direction] = False


    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = board.snakes
    for opponent in opponents:
        opponent_body = opponent.body
        for block in opponent_body:
            if check_if_point_is_neighbour(my_head, block):
                direction = get_point_direction_relative(my_head, block)
                is_move_safe[direction] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state.turn}: No safe moves detected! Moving down")
        return {"move": Direction.DOWN.value}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = board.food
    if len(food) > 0:
        closest_food_distance = None
        food_position = None

        for f in food:
            f_distance = calculate_distance_between_two_points(my_head, f)
            if closest_food_distance is None or f_distance < closest_food_distance:
                closest_food_distance = f_distance
                food_position = f

        if food_position is not None:
            if food_position.x < my_head.x and is_move_safe[Direction.LEFT.value]:
                next_move = Direction.LEFT.value
            elif food_position.x > my_head.x and is_move_safe[Direction.RIGHT.value]:
                next_move = Direction.RIGHT.value
            elif food_position.y < my_head.y and is_move_safe[Direction.DOWN.value]:
                next_move = Direction.DOWN.value
            elif food_position.y > my_head.y and is_move_safe[Direction.UP.value]:
                next_move = Direction.UP.value

    print(f"MOVE {game_state.turn}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
