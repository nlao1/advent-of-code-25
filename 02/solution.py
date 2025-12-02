from typing import *
import math

example = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224, 1698522-1698528,446443-446449,38593856-38593862,565653-565659, 824824821-824824827,2121212118-2121212124"


def parse(s: str) -> list[tuple[int, int]]:
    ranges = []
    for range in s.strip().split(","):
        beginning, end = range.split("-")
        ranges.append((int(beginning), int(end)))
    return ranges


def part1(ranges: list[tuple[int, int]]):
    # invalid if same number repeated twice = divisible by 100...01
    def id_is_invalid(id):
        num_digits = len(str(id))
        if num_digits % 2 == 0:
            divisor = 10 ** (num_digits // 2) + 1
            return id % divisor == 0

    def invalid_ids_in_range_brute_force(start, end):
        return sum(id if id_is_invalid(id) else 0 for id in range(start, end + 1))

    return sum(invalid_ids_in_range_brute_force(*range) for range in ranges)


def factors(num):
    up_to_sqrt = set(i for i in range(1, int(math.sqrt(num) + 1)) if num % i == 0)
    return (up_to_sqrt | set(num // i for i in up_to_sqrt)) - set([num])


def part2(ranges: list[tuple[int, int]]):
    def divisors(id):
        num_digits = len(str(id))
        result = []
        for length_of_repeated_string in factors(num_digits):
            # e.g. 828282 is divisible by 10 ** 4 + 10 ** 2 + 10 ** 0
            result.append(
                sum(
                    10**i
                    for i in range(
                        0,
                        num_digits,
                        length_of_repeated_string,
                    )
                )
            )
        return result

    # an id is invalid if there is a repeated N length string, where N is a
    # factor of the id.
    def id_is_invalid(id):
        return any(id % divisor == 0 for divisor in divisors(id))

    def invalid_ids_in_range_brute_force(start, end):
        return sum(id if id_is_invalid(id) else 0 for id in range(start, end + 1))

    return sum(invalid_ids_in_range_brute_force(*range) for range in ranges)


if __name__ == "__main__":
    example = parse(example)
    print(part1(example))
    input = parse(open("input.txt").readline())
    print(part1(input))
    print(part2(example))
    print(part2(input))
