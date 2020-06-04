import pygeoj
from auspixdggs.auspixengine.dggs import RHEALPixDGGS
from auspixdggs.callablemodules.util import transform_coordinates

rdggs = RHEALPixDGGS() # make an instance

'''
developed at Geoscience Australia by Joseph Bell June 2020
'''

def latlong_to_DGGS(coords, resolution, from_epsg=None):
    '''
    This function takes coords (array of x and y) and returns the dggs cell ID at an input resolution.
    If from_epsg is set, then the coordinates are transformed to epsg:4326 or WGS84 (CRS that the DGGS engine expects)
    using pyproj with the always_xy parameter set to True. Otherwise, it assumes coords are in WGS84.
    '''
    coords_to_use = coords
    if from_epsg is not None:
        coords_to_use = transform_coordinates(coords[0], coords[1], from_epsg, 4326) #convert to epsg:4326 or WGS84
    # calculate the dggs cell from long and lat
    thisCell = rdggs.cell_from_point(resolution, coords_to_use, plane=False)  # false = on the elipsoidal curve
    # now have a dggs cell for that point
    return thisCell

def dggs_cells_for_points(geojson, resolution):
    # make an output file of DGGS centroid points with the at atttibute properties
    newfile = pygeoj.new()  # default projection is WGS84
    resArea = (rdggs.cell_area(resolution, plane=False))

    #work through the features (polygons) one by one and ask for DGGS cells
    for feature in testfile:
        print('feature attributes ', feature.properties)  # the feature attributes - want to keep for output

        coords = feature.geometry.coordinates  # xy
        print('geom', coords)
        
        #this_dggs_cell = rdggs.cell_from_point(resolution, coords, plane=False)  # false = on the elipsoidal curve
        this_dggs_cell = latlong_to_DGGS(coords, resolution)

        print('found cell = ', this_dggs_cell)

        my_prop = feature.properties
        my_Cell = {"AusPIX_DGGS": str(this_dggs_cell), "LongiWGS84": coords[0], "LatiWGS84": coords[1], "CellArea_M2": resArea}

        #include the AusPIX cell information in attributes
        these_attributes = dict(list(my_Cell.items()) + list(my_prop.items()))
        #print('these attributes = ', these_attributes)

        newfile.add_feature(properties=these_attributes, geometry={"type": "Point", "coordinates": coords})

    #save the ouput geojson file
    newfile.save("test_points.geojson")  # saves into the folder where you have the script - edit to change

if __name__ == '__main__':
    testfile = pygeoj.load(filepath=r'test_data/EIT_geojson_example.geojson')
    resolution = 10

    print('len', len(testfile)) # the number of features
    print('bbox of entire file', testfile.bbox) # the bounding box region of the entire file
    dggs_cells_for_points(testfile, resolution)
