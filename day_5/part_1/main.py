from pathlib import Path
from typing import Optional


class AlmMapItem:
    def __init__(self, dst: int, src: int, rng: int):
        self.dst = dst
        self.src = src
        self.rng = rng

    def __repr__(self):
        return f"AlmMapItem({self.dst}, {self.src}, {self.rng})"


class AlmMap(list[AlmMapItem]):
    def __repr__(self):
        return f"AlmMap({super().__repr__()})"


def extract_seeds(line: str) -> list[int]:
    _, nums_str = line.split(":")
    seeds = [int(n) for n in nums_str.split()]
    return seeds


def extractAlmMap(map_lines: list[str]) -> AlmMap:
    almMap = AlmMap()
    for map_line in map_lines:
        dst, src, rng = [int(m) for m in map_line.split()]
        almMap.append(AlmMapItem(dst, src, rng))
    return almMap


def MapToNext(data: list[int], almMap: AlmMap) -> list[int]:
    def findMap(item: int, almMap: AlmMap) -> Optional[AlmMapItem]:
        for sub_map in almMap:
            if item in range(sub_map.src, sub_map.src + sub_map.rng):
                return sub_map
        return None

    def applyMap(item: int, almMapItem: Optional[AlmMapItem]) -> int:
        if almMapItem is None:
            return item

        shift = almMapItem.dst - almMapItem.src
        return item + shift

    ret_data = [applyMap(i, findMap(i, almMap)) for i in data]
    return ret_data


def calc_file(file_path: Path) -> int:
    with open(file_path, "r") as f:
        line = f.readline()
        data = extract_seeds(line)
        print(data)
        line = f.readline()

        while line:
            line = f.readline()
            map_lines: list[str] = []
            while line and line != "\n":
                map_lines.append(line)
                line = f.readline()

            map_lines = map_lines[1:]
            almMap: AlmMap = extractAlmMap(map_lines)
            data = MapToNext(data, almMap)

            print(data)

    return min(data)


if __name__ == "__main__":
    base_path = Path(__file__).parents[1]
    print(calc_file(base_path / "example.txt"))
    print(calc_file(base_path / "input.txt"))
