from pathlib import Path


def process_line(line: str) -> int:
    _, numbers_str = line.split(":")
    winning_nums_str, my_nums_str = numbers_str.split("|")
    winning_nums = set([int(n) for n in winning_nums_str.split()])
    my_nums = set([int(n) for n in my_nums_str.split()])

    my_winning_nums = winning_nums & my_nums
    num_wins = len(my_winning_nums)

    return num_wins


def calc_file(file_path: Path) -> int:
    cards_dict: dict[int, int] = {}

    with open(file_path, "r") as f:
        line_count = sum([1 for _ in f])
        f.seek(0)

        for i in range(line_count):
            cards_dict[i] = 1

        for curr_line, line in enumerate(f):
            num_wins = process_line(line)

            for i in range(curr_line + 1, curr_line + num_wins + 1):
                if i in cards_dict:
                    cards_dict[i] += cards_dict[curr_line]
                else:
                    print("Oh no!")

    sum_cards = sum(cards_dict.values())

    return sum_cards


if __name__ == "__main__":
    base_path = Path(__file__).parents[1]
    print(calc_file(base_path / "example.txt"))
    print(calc_file(base_path / "input.txt"))
