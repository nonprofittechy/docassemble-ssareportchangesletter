from docassemble.base.util import validation_error, Address, DAObject, text_type
import re
import requests

def is_valid_ssn(x):
    """Validates that the field is 3 digits, a hyphen, 2 digits, a hyphen, and 4 final digits only."""
    #return True # speed up testing
    valid_ssn=re.compile(r'^\d{3}-\d{2}-\d{4}$')
    if not bool(re.match(valid_ssn,x)):
        validation_error("Write the Social Security Number like this: XXX-XX-XXXX")
    return True

class FieldOffice(DAObject):
    def init(self, *pargs, **kwargs):
        super(FieldOffice, self).init(*pargs, **kwargs)

    def __unicode__(self):
        return self.title + ' (' + self.city + ')'
    
    def __str__(self):
        return str(self.__unicode__())

class FieldOfficeSearcher(DAObject):
    def init(self, *pargs, **kwargs):
        super(FieldOfficeSearcher, self).init(*pargs, **kwargs)

    #@staticmethod
    def nearest_offices_by_lat_lng(self, latitude, longitude, number=3, distance=5):
        """Recursively search for the nearest number SSA offices, expanding search area if we receive too few results"""
        url =   "http://services6.arcgis.com/zFiipv75rloRP5N4/ArcGIS/rest/services/Office_Points/FeatureServer/1/query"
        
        results = []

        params = {
            'geometry': str(longitude) + ',' + str(latitude),
            'distance': distance,
            'geometryType': 'esriGeometryPoint',
            'inSR': 4326, # See https://developers.arcgis.com/documentation/core-concepts/spatial-references/
            'outSR': 4326,
            'spatialRel': 'esriSpatialRelIntersects',
            'resultType': 'none',
            'units': 'esriSRUnit_StatuteMile',
            'returnGeodetic': 'false',
            'outFields': '*',
            'returnGeometry': 'true',
            'multipatchOption': 'xyFootprint',
            'applyVCSProjection': 'false',
            'returnIdsOnly': 'false',
            'returnUniqueIdsOnly': 'false',
            'returnExtentOnly': 'false',
            'returnDistinctValues': 'false',
            'returnZ': 'false',
            'returnM': 'false',
            'returnExceededLimitFeatures': 'true',
            'sqlFormat': 'none',
            'f': 'pgeojson',
            'quantizationParameters': '',
            'where': '',
            'objectIds': '',
            'time': '',
            'maxAllowableOffset': '',
            'geometryPrecision': '',
            'datumTransformation': '',
            'orderByFields': '',
            'groupByFieldsForStatistics': '',
            'outStatistics': '',
            'having': '',
            'resultOffset': '',
            'resultRecordCount': '',
            'token': ''
        }
        
        r = requests.get(url, params=params)

        self.url = r.url

        jdata = r.json()

        try:
            for item in jdata['features']:
                fo = FieldOffice()
                fo.title = item['properties']['AddressLine1']
                fo.address = item['properties']['AddressLine3']
                fo.suite = item['properties']['AddressLine2']
                fo.city = item['properties']['City']
                fo.state = item['properties']['State']
                results.append(fo)
        except:
            return []
        
        return results


    def nearest_offices(self, address, number=3, distance=5, results=[]):
        return self.nearest_office_by_lat_lng(address.location.longitude, address.location.latitude, number=number, distance=distance, results=results)


if __name__ == '__main__':
    # import pprint
    # res = FieldOfficeSearcher.nearest_office_by_lat_lng(42.3641657, -71.0626028,17)
    pass