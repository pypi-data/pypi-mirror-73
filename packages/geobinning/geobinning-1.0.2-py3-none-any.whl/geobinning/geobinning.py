import matplotlib.path as mpltPath


def bin(geojson):
    print('adsadasd')

    fips = []
    bins = []
    for i,county in enumerate(counties['features']):
        coords = county['geometry']['coordinates'][0]
        print(county['properties']['STATE'])
        if (len(coords)>2):
            path = mpltPath.Path(coords)
            inside = path.contains_points(points)
            cnt = np.count_nonzero(inside)

            print(i)
            print('   -> ' + str(cnt))
            fips.append(county['id'])
            bins.append(cnt)
    fp= pd.DataFrame(list(zip(fips, bins)),columns=['fips','bins'])
