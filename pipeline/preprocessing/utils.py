from shapely.geometry import Point
import math

SQFT_PER_SQM = 10.7639  # conversion

def compute_buffer_and_metadata(lat, lon, radius_sqft=2400):
    """
    Creates a small buffer polygon around the lat/lon coordinate.
    Returns polygon + area_sqft.
    """

    # convert square feet to radius in meters
    radius_m = math.sqrt(radius_sqft / SQFT_PER_SQM)

    # convert meters to degrees (rough, but ok for small radius)
    deg_per_meter = 1 / 111111
    radius_deg = radius_m * deg_per_meter

    point = Point(lon, lat)
    poly = point.buffer(radius_deg)

    return poly, radius_sqft
