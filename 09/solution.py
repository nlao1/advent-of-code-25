from collections import defaultdict
from itertools import combinations, pairwise
from typing import *
import sys
from PIL import ImageDraw, Image, ImageColor
import shapely

D = sys.stdin.readlines()
Point = tuple[int, int]
Segment = tuple[Point, Point]
points = [line.strip().split(",") for line in D]
points = [(int(x), int(y)) for x, y in points]


def max_area(points: list[Point], *, filter):
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

# points_scaled_down = [(x / 10, y / 10) for x, y in points]
# image = Image.new("RGB", (10000, 10000), color=ImageColor.getcolor("white", mode="RGB"))
# image_draw = ImageDraw.Draw(image)
# image_draw.polygon(points_scaled_down, fill=(0, 255, 0), outline=(255, 0, 0), width=1)
# image.save(open("image.png", "wb"))


# this is copied
def find_intersection(segment1, segment2):
    p1, q1 = segment1
    p2, q2 = segment2

    dx1, dy1 = q1[0] - p1[0], q1[1] - p1[1]
    dx2, dy2 = q2[0] - p2[0], q2[1] - p2[1]

    denom = dx1 * dy2 - dy1 * dx2
    if denom == 0:  # colinear or parallel
        return None

    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    t = (dx * dy2 - dy * dx2) / denom
    u = (dx * dy1 - dy * dx1) / denom

    if 0 <= t <= 1 and 0 <= u <= 1:
        ix = p1[0] + t * dx1
        iy = p1[1] + t * dy1
        return (ix, iy)

    return None


"""
idea sketch: because the polygon is simple and concave, we can do some better
guesswork. if the segments on the perimeter of the candidate rectangle
intersect the polygon, disqualify. otherwise, pass the polygon.

this
1. prevents the need to do coordinate compression
2. avoids use of any external libraries 
"""


def rectangle_intersects_polygon(
    corner1: Point, corner2: Point, segments_in_polygon: list[Segment]
):
    x1, y1 = corner1
    x2, y2 = corner2
    segments_of_rectangle = [
        (corner1, (x1, y2)),
        (corner1, (x2, y1)),
        (corner2, (x1, y2)),
        (corner2, (x2, y1)),
    ]

    for segment_of_polygon in segments_in_polygon:
        for segment_of_rectangle in segments_of_rectangle:
            intersection = find_intersection(segment_of_polygon, segment_of_rectangle)
            if intersection is not None and intersection not in [x1, y2, x2, y2]:
                print(intersection)
                return True


polygon: list[Segment] = list(pairwise(points))
last_segment: Segment = (points[-1], points[0])
polygon.append(last_segment)

# print(
#     max_area(
#         points,
#         filter=lambda p1, p2: not (rectangle_intersects_polygon(p1, p2, polygon)),
#     )
# )


# i gave up because i had the right idea but didn't feel like implementing it
# https://topaz.github.io/paste/#XQAAAQAHBgAAAAAAAAARiEJGPfQWNG6xo4rUnrU/FzgTXmJOWQF53DaV6F4jcQsRQpNT4KyGWX66ZLlpstXf+BRXuzz0b0x6nu636AVL8evH+/0PJpYybn5SL1OsKe3lC6MDHMK9T9+o7IM3EGo2yuZYJqHdZmzwv9ZC1K3fcyOYKdaNib2p2LDFk8uCxB/T1x27flvI+y2kxMffiGBAxQwGZIwrHc/SxDgpRH4L+7fafBdFgPBgC5nptQg0kOjmu1cxafQahpgPchxUrdxEdw074voR7TW/WPcKv6cLiDY6tJV2zrlmwKKA1CJp2dj3mXqPLEGKsViA1d/FSGzkyi+O2XmZwl46ezGgfXf533LoithiURZnSJTrRZbNtCbByOuN9GOE5c41OeosKmGZ6ZLAKH0Doc5GciipAXBPQTrcZF/LNfi9a7X0zXqA+IlTrhIygHvhYix+RPaHI++U55CUtAUbmZTOhjrKI6TQl0Evn865B9uFFKQIx4CW07KrVQqzVVMiKuRgNd1VIMXtuLFqbWsTrc7SfkWpmjsx+eZsvEoStAzTmf5T81cNkbdJyF4dTgXjsfsL+9iFfIHPXAAF5llFMYIymolfCvAKiV+e5RBE8OgpLo0x5eNDbxHbkxSi+/6jnZJzGUF+pB8091mgFJLeTAl0GJhMLuIXFcEcWqvRyswgm/4JYmoUiALrZwzWqwYuZNtOdVeF6MUyEbh8pExMuihcmYnYYuHPaEum4ZakWmV6u0iVq/6WasGqa6uDOF0JEG5xVz/h7EwBXvUISANEUQVF6cG8UwH3AZXHY3DRuAI7McAHGWB0rqDSERhZShgEzJmFDZ4rTSWsger7p65ZGSDAi3l3TCS2b/WPVMaAfI9WFiyDY+dVyyNyE/55MQ6Q4wD+7gDe
answer = 0
red_green = shapely.Polygon([(x, y) for (y, x) in points])

for a, b in combinations(points, 2):
    ax = a[1]
    ay = a[0]
    bx = b[1]
    by = b[0]

    left = ax if ax < bx else bx
    right = ax if ax > bx else bx
    top = ay if ay < by else by
    bottom = ay if ay > by else by

    candidate = shapely.box(left, top, right, bottom)

    if not shapely.contains(red_green, candidate):
        continue

    area = (right - left + 1) * (bottom - top + 1)
    if answer < area:
        answer = area
