# import pandas as pd
# import geopandas as gpd
# import geopy
from geopy.geocoders import Nominatim
# from geopy.extra.rate_limiter import RateLimiter
# import matplotlib.pyplot as plt
# import plotly_express as px
# import tqdm
# from tqdm._tqdm_notebook import tqdm_notebook

locator = Nominatim(user_agent="myGeocoder")
coordinates = "41.310267, 69.307709"
location = locator.reverse(coordinates)
print(location.raw['display_name'])
# print(f"{location.raw['address']['city']} shahar {location.raw['address']['locality']} {location.raw['address']['house_number']}")