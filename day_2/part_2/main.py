from pathlib import Path
from typing import TypedDict


class CubeCounts(TypedDict):
    red: int
    green: int
    blue: int


def extract_rgb(draw: str) -> CubeCounts:
    drawn_colors = draw.split(",")

    drawn_cubes: CubeCounts = {"red": 0, "green": 0, "blue": 0}
    for drawn_color in drawn_colors:
        value, color = drawn_color.split()

        if color in drawn_cubes.keys():
            drawn_cubes[color] = int(value)

    return drawn_cubes


def game_cube_power(line: str) -> int:
    _, draws_str = line.split(":")

    draws = draws_str.split(";")

    min_cubes: CubeCounts = {"red": 0, "green": 0, "blue": 0}

    for draw in draws:
        drawn_cubes = extract_rgb(draw)
        for color, count in drawn_cubes.items():
            if min_cubes[color] < count:
                min_cubes[color] = count

    return min_cubes["red"] * min_cubes["green"] * min_cubes["blue"]


def calc_file(file_path: Path) -> int:
    cubes_power_sum = 0

    with open(file_path, "r") as f:
        for line in f:
            cubes_power_sum += game_cube_power(line)

    return cubes_power_sum


if __name__ == "__main__":
    base_path = Path(__file__).parents[1]
    print(calc_file(base_path / "example.txt"))
    print(calc_file(base_path / "input.txt"))
