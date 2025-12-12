from collections import defaultdict
from itertools import combinations, pairwise
from typing import *
import sys
from PIL import ImageDraw, Image, ImageColor

D = sys.stdin.readlines()
points = [line.strip().split(",") for line in D]
points = [(int(x), int(y)) for x, y in points]


def max_area(points, *, filter):
    max_area = -1
    for p1, p2 in combinations(points, 2):
        x1, y1 = p1
        x2, y2 = p2
        if not filter(p1, p2):
            continue
        area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        max_area = max(area, max_area)
    return max_area


consecutive_points = pairwise(points)

print(max_area(points, filter=lambda _p1, _p2: True))

points_scaled_down = [(x / 10, y / 10) for x, y in points]
image = Image.new("RGB", (10000, 10000), color=ImageColor.getcolor("white", mode="RGB"))
image_draw = ImageDraw.Draw(image)
image_draw.polygon(points_scaled_down, fill=(0, 255, 0), outline=(255, 0, 0), width=1)
image.save(open("image.png", "wb"))
