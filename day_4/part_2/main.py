from pathlib import Path


def process_line(line: str) -> int:
    _, numbers_str = line.split(":")
    winning_nums_str, my_nums_str = numbers_str.split("|")
    winning_nums = set([int(n) for n in winning_nums_str.split()])
    my_nums = set([int(n) for n in my_nums_str.split()])

    my_winning_nums = winning_nums & my_nums

    winnings = 0
    if my_winning_nums:
        winnings = 2 ** (len(my_winning_nums) - 1)

    return winnings


def calc_file(file_path: Path) -> int:
    win_sum = 0

    with open(file_path, "r") as f:
        for line in f:
            win_sum += process_line(line)

    return win_sum


if __name__ == "__main__":
    base_path = Path(__file__).parents[1]
    print(calc_file(base_path / "example.txt"))
    print(calc_file(base_path / "input.txt"))
