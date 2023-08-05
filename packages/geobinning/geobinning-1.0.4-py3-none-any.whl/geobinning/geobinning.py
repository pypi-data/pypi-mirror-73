import matplotlib.path as mpltPath

class geobinning:
    def __init__(self):
        pass;
    def geobin(geojson):
        id = [];bins = []
        for i,feature in enumerate(geojson['features']):
            coords = geojson['geometry']['coordinates'][0]
            if (len(coords)>2):
                path = mpltPath.Path(coords)
                inside = path.contains_points(points)
                cnt = np.count_nonzero(inside)
                id.append(feature['id'])
                bins.append(cnt)
        return pd.DataFrame(list(zip(id, bins)),columns=['id','bins'])
