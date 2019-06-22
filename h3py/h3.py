class h3:
    """
    Uber developed H3, their grid system for efficiently optimizing ride pricing and dispatch, for visualizing and
    exploring spatial data. H3 enables analyst to analyze geographic information to set dynamic prices and make other
    decisions on a city-wide level. They use H3 as the grid system for analysis and optimization throughout the
    marketplaces. H3 was designed for this purpose, and led us to make some choices such as using hexagonal,
    hierarchical indexes.
    """

    def __init__(self, latitude: float, longitude: float, radius: int):
        """
            Initialize the class by passing lat/lon and raidus. This will be used to generate a geo to h3 hash.

            :param latitude: float
            :param longitude: float
            :param raidus: int

            :example
                h3.h3(37.3615593, -122.0553238, 5) # lat, lng, hex resolution
            :return
               85283473fffffff
        """

        self.__latitude = latitude
        self.__longitude = longitude
        self.__radius = radius
        self.__h3_address = None

    @property
    def geo_to_h3(self):
        """
            Index a geo-coordinate at a resolution into an h3 address

            :exmaple
                h3_address = h3.h3(7.3615593, -122.0553238, 5)
            :return
                856e71abfffffff
        """
        import subprocess
        import os
        # build args for subprocess
        # this will have to be fixed
        exe_geo_to_h3 = r"C:\Users\Owner\Desktop\h3-master\build\bin\Debug\geoToH3.exe"
        args = f'{exe_geo_to_h3} --lat {self.__latitude} --lon {self.__longitude} -r {self.__radius}'

        # create outfile to store results and to retrieve
        current_dir = os.path.dirname(os.path.abspath(__file__))
        outfile = os.path.join(current_dir, r'Output/geo2h3.txt')

        FNULL = open(outfile, 'w')
        subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)

        FNULL.close()

        with open(outfile, 'r') as readFile:
            readFile = readFile.read().rstrip('\n')
            self.__h3_address = readFile
        # delete the txt file
        if os.path.exists(outfile):
            os.remove(outfile)

        return self.__h3_address


    def h3_to_geo(self, h3_address):
        """
            Reverse lookup an h3 address into a geo-coordinate

            :return:
        """
        import subprocess, os
        # exe for h3 to geo; this will have to be fixed
        exe_h3_to_geo = r"C:\Users\Owner\Desktop\h3-master\build\bin\Debug\h3ToGeo.exe"


        # build args for subprocess
        args = f'{exe_h3_to_geo} -i {h3_address}'

        # create outfile to store results and to retrieve
        current_dir = os.path.dirname(os.path.abspath(__file__))
        outfile = os.path.join(current_dir, r'Output/h32geo.txt')

        FNULL = open(outfile, 'w')
        subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)

        FNULL.close()

        with open(outfile, 'r') as readFile:
            h32geo = readFile.read().rstrip('\n')
        # delete the txt file
        if os.path.exists(outfile):
            os.remove(outfile)
        return (float(h32geo.split()[1]), float(h32geo.split()[0]))

    def h3_to_geoboundary(self, h3_address):
        """
            Compose an array of geo-coordinates that outlines a hexagonal cell
        """

        import subprocess, os
        # exe for h3 to geo; this will have to be fixed
        exe_h3_to_geobound = r"C:\Users\Owner\Desktop\h3-master\build\bin\Debug\h3ToGeoBoundary.exe"

        # build args for subprocess
        args = f'{exe_h3_to_geobound} -i {h3_address}'

        # create outfile to store results and to retrieve
        current_dir = os.path.dirname(os.path.abspath(__file__))
        outfile = os.path.join(current_dir, r'Output/h32geobound.txt')

        FNULL = open(outfile, 'w')
        subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)

        FNULL.close()

        with open(outfile, 'r') as readFile:
            h32geo = readFile.read().rstrip('\n')
            h32geo = h32geo.replace(h3_address,'').lstrip()

        h32geo = h32geo.split('\n')

        h32geobnd = {(float(h.split()[1]), float(h.split()[0])) for h in h32geo if h != '{' and h != '}'}
        # delete the txt file
        if os.path.exists(outfile):
            os.remove(outfile)

        return h32geobnd
