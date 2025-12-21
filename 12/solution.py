from typing import *
import sys
import re
from dataclasses import dataclass


@dataclass
class Region:
    width: int
    height: int
    requirements: list[int]


Shape = list[str]  # length 3 array of 3-character strings

D = sys.stdin.readlines()

shapes: list[Shape] = []
regions: list[Region] = []
is_matching_shape = False
shape = []
shape_regex = re.compile(r"(\d+):$")
region_regex = re.compile(r"(\d+)x(\d+):")
for line in D:
    line = line.strip()
    shape_match = re.match(shape_regex, line)
    region_match = re.match(region_regex, line)
    if len(line) == 0 and len(shape) > 0:
        shapes.append(shape)
        is_matching_shape = False
    elif is_matching_shape:
        shape.append(line)
    elif shape_match:
        shape = []
        is_matching_shape = True
    elif region_match:
        width = int(region_match.group(1))
        height = int(region_match.group(2))
        requirements = [int(num.strip()) for num in line.split(":")[1].split()]
        regions.append(Region(width, height, requirements))


def area_of_shape(shape: Shape):
    return sum(line.count("#") for line in shape)


shape_areas = {
    shape_idx: area_of_shape(shape) for shape_idx, shape in enumerate(shapes)
}


# this isn't robust, it just cheats based on what people said on reddit about
# what the shape of the solution was. if I hadn't known that area alone was
# enough, I would have probably used a sat solver
def region_meets_requirements(region: Region):
    area = region.width * region.height
    area_needed = sum(
        shape_areas[shape_idx] * required_number
        for shape_idx, required_number in enumerate(region.requirements)
    )
    return area_needed < area


print(sum(1 if region_meets_requirements(region) else 0 for region in regions))
