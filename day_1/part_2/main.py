from enum import Enum
from math import inf
from pathlib import Path


class Numbers(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9


def get_calibration_of_line(line: str) -> int | None:
    line = line.lower()

    l_index = inf
    r_index = -inf

    first_number: str | None = None
    last_number: str | None = None

    for num in Numbers:
        ln_i = line.find(num.name.lower())
        ln_i = ln_i if ln_i != -1 else inf
        lv_i = line.find(str(num.value))
        lv_i = lv_i if lv_i != -1 else inf

        l_i = min(ln_i, lv_i)

        rn_i = line.rfind(num.name.lower())
        rv_i = line.rfind(str(num.value))
        r_i = max(rn_i, rv_i)

        if -1 < l_i < l_index:
            l_index = l_i
            first_number = str(num.value)

        if -1 < r_i > r_index:
            r_index = r_i
            last_number = str(num.value)

    if first_number is None or last_number is None:
        return None

    return int(first_number + last_number)


def get_calibration_of_file(file_path: Path):
    calibration_sum = 0

    with open(file_path, "r") as f:
        for line in f:
           cs = get_calibration_of_line(line)
           if cs is None:
               raise ValueError("Calibration numbers not found")
           calibration_sum += cs

    return calibration_sum


if __name__ == "__main__":
    base_path = Path(__file__).parent
    print(get_calibration_of_file(base_path / "example.txt"))
    print(get_calibration_of_file(base_path.parent / "input.txt"))
