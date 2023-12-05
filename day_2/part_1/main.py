from pathlib import Path
from typing import TypedDict


class CubeCounts(TypedDict):
    red: int
    green: int
    blue: int


def is_draw_possible(draw: str, cube_counts: CubeCounts) -> bool:
    drawn_colors = draw.split(",")

    for drawn_color in drawn_colors:
        value, color = drawn_color.split()

        if color in cube_counts.keys() and cube_counts[color] < int(value):
            return False

    return True


def is_game_possible(line: str, cube_counts: CubeCounts) -> tuple[bool, int]:
    game_str, draws_str = line.split(":")
    game_id = int(game_str.split()[1])

    draws = draws_str.split(";")

    game_is_possible = False

    for draw in draws:
        if not is_draw_possible(draw, cube_counts):
            break
    else:
        game_is_possible = True

    return game_is_possible, game_id


def calc_file(file_path: Path, cube_counts: CubeCounts) -> int:
    possible_games_sum = 0

    with open(file_path, "r") as f:
        for line in f:
            game_possible, game_id = is_game_possible(line, cube_counts)
            if game_possible:
                possible_games_sum += game_id

    return possible_games_sum


if __name__ == "__main__":
    cube_counts: CubeCounts = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    base_path = Path(__file__).parents[1]
    print(calc_file(base_path / "example.txt", cube_counts))
    print(calc_file(base_path / "input.txt", cube_counts))
