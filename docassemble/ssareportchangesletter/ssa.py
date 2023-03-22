from docassemble.base.util import validation_error, Address, DAObject, DAList, Person, title_case, log
import re
import requests

def is_valid_ssn(x):
    """Validates that the field is 3 digits, a hyphen, 2 digits, a hyphen, and 4 final digits only."""
    #return True # speed up testing
    valid_ssn=re.compile(r'^\d{3}-\d{2}-\d{4}$')
    if not bool(re.match(valid_ssn,x)):
        validation_error("Write the Social Security Number like this: XXX-XX-XXXX")
    return True

class FieldOffice(Person):
    def init(self, *pargs, **kwargs):
        super(FieldOffice, self).init(*pargs, **kwargs)

class FieldOfficeList(DAList):
    def init(self, *pargs, **kwargs):
        super(FieldOfficeList, self).init(*pargs, **kwargs)
        self.auto_gather = False
        self.object_type = FieldOffice
        self.initializeAttribute('searcher',FieldOfficeSearcher)

        if hasattr(self, 'address'):
            self.load_offices(self.address, 3)
            self.gathered = True

    def load_offices(self, address, number=3):
        """ Find at least number offices closest to the given address"""

        distance = 5 # start out searching for offices within 5 miles

        results = self.searcher.nearest_offices(address, distance=distance)
        
        if not can_geolocate(address):
          self.gathered=True
          return None

        loop = 1
        max_loop = 9        

        try:
            # Keep expanding the search radius if we didn't get enough matches in the default distance
            while loop < max_loop and len(results['features']) < number:
                distance *= 2
                results = self.searcher.nearest_offices(address, distance=distance)
                loop += 1
        except:
            self.gathered = True
            return None

        for item in results.get('features',{}):
            fo = self.appendObject()
            props = item.get('properties',{})
            fo.name.text = title_case(props.get('AddressLine1','')) 
            fo.title = title_case(props.get('OfficeName',''))
            fo.address.address = title_case(props.get('AddressLine3',''))
            if props.get('AddressLine2'):
                fo.address.unit = title_case(props.get('AddressLine2',''))
            fo.address.city = title_case(props.get('City',''))
            fo.address.state = props.get('State')
            fo.address.zip = props.get('ZIP5')
            fo.office_code = props.get('OfficeCode')
            fo.phone_number = props.get('BusinessPhone')

        self.gathered = True


class FieldOfficeSearcher(DAObject):
    def init(self, *pargs, **kwargs):
        super(FieldOfficeSearcher, self).init(*pargs, **kwargs)

    #@staticmethod
    def nearest_offices_by_lat_lng(self, latitude, longitude, distance=5):
        """Search for nearby SSA offices, and return raw GeoJSON results"""
        url =   "https://services6.arcgis.com/zFiipv75rloRP5N4/ArcGIS/rest/services/Office_Points/FeatureServer/1/query"
        
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
        try:
          r = requests.get(url, params=params)
          self.url = r.url
          jdata = r.json()
          return jdata
        except:
          return {}

    def nearest_offices(self, address, distance=5):
        if hasattr(address.location,'longitude') and hasattr(address.location, 'latitude'):
            return self.nearest_offices_by_lat_lng(address.location.latitude,address.location.longitude, distance=distance)
        else:
            if can_geolocate(address):
              return self.nearest_offices_by_lat_lng(address.location.latitude,address.location.longitude, distance=distance)
            else:
              return None

def can_geolocate(address:Address)->bool:
  if hasattr(address,'geolocate_success'):
    return address.geolocate_success
  else:
    address.geolocate()
    return address.geolocate_success              
              
if __name__ == '__main__':
    # import pprint
    # res = FieldOfficeSearcher.nearest_office_by_lat_lng(42.3641657, -71.0626028,17)
    pass