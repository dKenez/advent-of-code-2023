from pathlib import Path


def dist_done(wait_t: int, race_t: int) -> int:
    return wait_t * (race_t - wait_t)


def map2ints(in_list: list[str]) -> list[int]:
    return [int(x) for x in in_list]


def calc_file(file_path: Path) -> int:
    with open(file_path, "r") as f:
        first_line = f.readline()
        second_line = f.readline()

    race_times = map2ints(first_line.split()[1:])
    record_dists = map2ints(second_line.split()[1:])

    combos = 1
    for race_time, record_dist in zip(race_times, record_dists):
        opts = len([x for x in range(race_time + 1) if dist_done(x, race_time) > record_dist])
        combos *= opts

    return combos


if __name__ == "__main__":
    base_path = Path(__file__).parents[1]
    print(calc_file(base_path / "example.txt"))
    print(calc_file(base_path / "input.txt"))
