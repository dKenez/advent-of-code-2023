from pathlib import Path


class DataItem:
    def __init__(self, min: int, max: int):
        self.min = min
        self.max = max

    def __repr__(self):
        return f"DataItem({self.min}, {self.max})"


class Data(list[DataItem]):
    def __repr__(self):
        return f"Data({super().__repr__()})"


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


def extract_seeds(line: str) -> Data:
    _, nums_str = line.split(":")
    data = [int(n) for n in nums_str.split()]
    seeds = Data()
    for i in range(len(data) // 2):
        seeds.append(DataItem(min=data[2 * i], max=data[2 * i] + data[2 * i + 1] - 1))
    return seeds


def extractAlmMap(map_lines: list[str]) -> AlmMap:
    almMap = AlmMap()
    for map_line in map_lines:
        dst, src, rng = [int(m) for m in map_line.split()]
        almMap.append(AlmMapItem(dst, src, rng))
    return almMap


def MapToNext(data: Data, almMap: AlmMap) -> Data:
    def findMaps(d: DataItem, almMap: AlmMap) -> AlmMap:
        ret_am = AlmMap(
            [map for map in almMap if d.min <= map.src <= d.max or map.src <= d.min <= map.src + map.rng - 1]
        )
        ret_am.sort(key=lambda i: i.src)
        return ret_am

    def applyMaps(d: DataItem, almMap: AlmMap) -> Data:
        if len(almMap) == 0:
            return Data([d])

        ret_d = Data()
        cursor = d.min
        if d.min < almMap[0].src:
            ret_d.append(DataItem(cursor, almMap[0].src - 1))
            cursor = almMap[0].src

        almMapLen = len(almMap)
        for i, map in enumerate(almMap):
            shift = map.dst - map.src
            cursor_end = min(map.src + map.rng - 1, d.max)

            ret_d.append(DataItem(cursor + shift, cursor_end + shift))
            cursor = cursor_end + 1
            if i + 1 < almMapLen:
                next_map = almMap[i + 1]
                if map.src + map.rng < next_map.src:
                    ret_d.append(DataItem(map.src + map.rng, next_map.src - 1))
            else:
                if map.src + map.rng - 1 < d.max:
                    ret_d.append(DataItem(map.src + map.rng, d.max))
        return ret_d

    ret_data = Data()

    for d in data:
        almMaps = findMaps(d, almMap)
        new_ranges = applyMaps(d, almMaps)
        ret_data += new_ranges

    return ret_data


def calc_file(file_path: Path) -> int:
    with open(file_path, "r") as f:
        line = f.readline()
        data = extract_seeds(line)
        # print(data)
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

            # print(data)

    return min([d.min for d in data])


if __name__ == "__main__":
    base_path = Path(__file__).parents[1]
    print(calc_file(base_path / "example.txt"))
    print(calc_file(base_path / "input.txt"))
