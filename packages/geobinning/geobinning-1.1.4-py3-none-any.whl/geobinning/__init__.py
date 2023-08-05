# __init__.py

# Version of the realpython-reader package
def geobin(geojson,points):
    import matplotlib.path as mpltPath
    import numpy as np
    import pandas as pd

    id = [];bins = []
    for i,feature in enumerate(geojson['features']):
        coords = feature['geometry']['coordinates'][0]
        if (len(coords)>2):
            path = mpltPath.Path(coords)
            inside = path.contains_points(points)
            cnt = np.count_nonzero(inside)
            id.append(feature['id'])
            bins.append(cnt)
    return pd.DataFrame(list(zip(id, bins)),columns=['id','bins'])
