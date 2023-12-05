import string
from collections import deque
from pathlib import Path

from rich import print


def get_start_i(nums_i: list[tuple[int, str]]) -> int:
    start_i = 0
    for num_i in nums_i:
        start_i = num_i[0]+len(num_i[1])

    return start_i


def process_line(q: deque[str]) -> tuple[int, list[tuple[int, str]]]:
    prev_line, curr_line, next_line = q
    prev_line = convert_symbols(prev_line)
    curr_line = convert_symbols(curr_line)
    next_line = convert_symbols(next_line)

    nums = extract_numbers(curr_line)
    nums_i: list[tuple[int, str]] = []

    for num in nums:
        start_i = get_start_i(nums_i)
        rem_line = curr_line[start_i:]

        i = rem_line.find(num)
        if i > -1:
            nums_i.append((i + start_i, num))

    parts_list: list[tuple[int, str]] = []
    line_sum = 0
    for i, num_i in enumerate(nums_i):
        is_part = False
        min_i = max(num_i[0] - 1, 0)
        max_i = min(num_i[0] + len(num_i[1]), len(curr_line) - 1)

        # prev line first
        if prev_line[min_i : max_i + 1].find("s") > -1:
            is_part = True

        # curr line
        if curr_line[min_i] == "s" or curr_line[max_i] == "s":
            is_part = True

        # next line first
        if next_line[min_i : max_i + 1].find("s") > -1:
            is_part = True

        # if part, add to sum
        if is_part:
            line_sum += int(num_i[1])
            parts_list.append(num_i)

    return line_sum, parts_list


def extract_numbers(line: str):
    clean_line = line.replace("s", ".")
    clean_line = clean_line.replace("\n", ".")
    s = clean_line.split(".")
    nums = [c for c in s if c != "" and c]
    return nums


def convert_symbols(line: str, char_set: str = string.punctuation.replace(".", ""), to: str = "s") -> str:
    def convert_symbol(c: str):
        if c in char_set:
            return "s"
        else:
            return c

    ret_line = "".join([convert_symbol(c) for c in line])

    return ret_line


def print_parts(line: str, parts_list: list[tuple[int, str]], line_sum: int, all_sum: int, line_num: int):
    open_tags = [part[0] for part in parts_list]
    close_tags = [part[0]+len(part[1]) for part in parts_list]
    print_str = f"[bold green]{line_num:3d} [/bold green]"
    for i, c in enumerate(line):
        if i in open_tags:
            print_str += "[magenta]"
        elif i in close_tags:
            print_str += "[/magenta]"

        if c == ".":
            print_str += "."
        elif c in string.punctuation:
            print_str += f"[yellow]{c}[/yellow]"
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
            line_sum, parts_list = process_line(q)
            parts_sum += line_sum
            print_parts(q[1], parts_list, line_sum, parts_sum, line_num)
            line_num += 1

        q.append(zero_padding)
        line_sum, parts_list = process_line(q)
        parts_sum += line_sum
        print_parts(q[1], parts_list, line_sum, parts_sum, line_num)

    return parts_sum


if __name__ == "__main__":
    base_path = Path(__file__).parents[1]
    calc_file(base_path / "example.txt")
    print()
    calc_file(base_path / "input.txt")
