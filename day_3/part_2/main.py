import string
from collections import deque
from functools import reduce
from pathlib import Path

from rich import print


def get_start_i(nums_i: list[tuple[int, str]]) -> int:
    start_i = 0
    for num_i in nums_i:
        start_i = num_i[0] + len(num_i[1])

    return start_i


def locate_numbers(nums: list[str], nums_i: list[tuple[int, str]], line: str):
    for num in nums:
        start_i = get_start_i(nums_i)
        rem_line = line[start_i:]

        i = rem_line.find(num)
        if i > -1:
            nums_i.append((i + start_i, num))


def process_line(q: deque[str]) -> tuple[int, list[int]]:
    prev_line, curr_line, next_line = q

    nums_i_prev: list[tuple[int, str]] = []
    nums_i_curr: list[tuple[int, str]] = []
    nums_i_next: list[tuple[int, str]] = []

    # numbers in previous line
    nums = extract_numbers(prev_line)
    locate_numbers(nums, nums_i_prev, prev_line)

    # numbers in current line
    nums = extract_numbers(curr_line)
    locate_numbers(nums, nums_i_curr, curr_line)

    # numbers in next line
    nums = extract_numbers(next_line)
    locate_numbers(nums, nums_i_next, next_line)

    asts = extract_asterisks(curr_line)

    gears_list: list[int] = []
    line_sum = 0
    for ast_i in asts:
        # prev line first
        count_prev = [int(num[1]) for num in nums_i_prev if num[0] - 1 <= ast_i <= num[0] + len(num[1])]

        # curr line
        count_curr = [int(num[1]) for num in nums_i_curr if num[0] - 1 <= ast_i <= num[0] + len(num[1])]

        # next line
        count_next = [int(num[1]) for num in nums_i_next if num[0] - 1 <= ast_i <= num[0] + len(num[1])]

        mega_count = count_prev + count_curr + count_next
        # if gear, add to sum
        if len(count_prev + count_curr + count_next) == 2:
            line_sum += reduce(lambda x, r: r * x, mega_count, 1)
            gears_list.append(ast_i)

    return line_sum, gears_list


def extract_asterisks(line: str) -> list[int]:
    asts_i: list[int] = []
    for i, c in enumerate(line):
        if c == "*":
            asts_i.append(i)

    return asts_i


def extract_numbers(line: str):
    clean_line = convert_symbols(line, char_set=string.punctuation, to=".")
    clean_line = clean_line.replace("\n", ".")
    s = clean_line.split(".")
    nums = [c for c in s if c != "" and c]
    return nums


def convert_symbols(line: str, char_set: str = string.punctuation.replace(".", ""), to: str = "s") -> str:
    def convert_symbol(c: str):
        if c in char_set:
            return to
        else:
            return c

    ret_line = "".join([convert_symbol(c) for c in line])

    return ret_line


def print_parts(line: str, gear_list: list[int], line_sum: int, all_sum: int, line_num: int):
    print_str = f"[bold green]{line_num:3d} [/bold green]"
    for i, c in enumerate(line):
        if c == "*":
            if i in gear_list:
                print_str += f"[red]{c}[/red]"
            else:
                print_str += f"[blue]{c}[/blue]"
        elif c in string.punctuation:
            print_str += c
        elif c in string.digits:
            print_str += c
        else:
            pass

    print_str += f"\t[blue]{line_sum}[/blue]"
    print_str += f"\t[yellow]{all_sum}[/yellow]"

    print(f"[white]{print_str}[/white]", end="\n")


def calc_file(file_path: Path) -> int:
    parts_sum = 0

    with open(file_path, "r") as f:
        first_line = f.readline()
        zero_padding = "." * len(first_line[:-1]) + "\n"

        q = deque[str](maxlen=3)
        q.append(zero_padding)
        q.append(first_line)

        line_num = 0
        for line in f:
            q.append(line)
            line_sum, gear_list = process_line(q)
            parts_sum += line_sum
            print_parts(q[1], gear_list, line_sum, parts_sum, line_num)
            line_num += 1

        q.append(zero_padding)
        line_sum, gear_list = process_line(q)
        parts_sum += line_sum
        print_parts(q[1], gear_list, line_sum, parts_sum, line_num)

    return parts_sum


if __name__ == "__main__":
    base_path = Path(__file__).parents[1]
    calc_file(base_path / "example.txt")
    print()
    calc_file(base_path / "input.txt")
