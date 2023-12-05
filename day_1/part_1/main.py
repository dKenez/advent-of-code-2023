import unicodedata
from pathlib import Path


def get_calibration_of_line(line: str) -> int:
    numeric_chars = [c for c in line if unicodedata.category(c)[0] == "N"]
    return int(numeric_chars[0] + numeric_chars[-1])


def get_calibration_of_file(file_path: Path):
    calibration_sum = 0

    with open(file_path, "r") as f:
        for line in f:
            calibration_sum += get_calibration_of_line(line)

    return calibration_sum


if __name__ == "__main__":
    base_path = Path(__file__).parent
    print(get_calibration_of_file(base_path / "example.txt"))
    print(get_calibration_of_file(base_path.parent / "input.txt"))
