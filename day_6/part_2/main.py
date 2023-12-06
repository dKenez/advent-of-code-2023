from pathlib import Path


def dist_done(wait_t: int, race_t: int) -> int:
    return wait_t * (race_t - wait_t)



def calc_file(file_path: Path) -> int:
    with open(file_path, "r") as f:
        first_line = f.readline()
        second_line = f.readline()

    race_time = int("".join(first_line.split()[1:]))
    record_dist = int("".join(second_line.split()[1:]))

    combos = len([x for x in range(race_time + 1) if dist_done(x, race_time) > record_dist])

    return combos


if __name__ == "__main__":
    base_path = Path(__file__).parents[1]
    print(calc_file(base_path / "example.txt"))
    print(calc_file(base_path / "input.txt"))
