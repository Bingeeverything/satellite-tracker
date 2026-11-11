import math

def point_to_line_distance(x0, y0, x1, y1, x2, y2): 

    distance = abs((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1)) / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance