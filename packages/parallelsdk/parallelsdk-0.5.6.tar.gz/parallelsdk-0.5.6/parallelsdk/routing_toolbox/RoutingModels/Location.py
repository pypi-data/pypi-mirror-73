import json
import urllib.request
import numpy as np


class Location:
    def __init__(self, position=[], address='', demand=0.0, location_id=-1):
        self.unique_id = id(self)
        self.location_id = location_id
        self.position = position
        self.address = address
        self.demand = demand

    def get_unique_id(self):
        return self.unique_id

    def get_id(self):
        return self.location_id

    def set_address(self, address):
        self.address = address

    def get_address_for_geocoding(self):
        address = self.address
        address = address.replace(",", "")
        address = address.replace(" ", "+")
        return address

    def get_address(self, API_key):
        if self.address:
            return self.address

        # Get actual address with reverse geocoding
        request = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + str(self.position[0]) + \
                  ',' + str(self.position[1]) + '&key=' + API_key
        with urllib.request.urlopen(request) as url:
            json_result = url.read()
            response = json.loads(json_result)
            status = response['status']
            if status != 'OK':
                raise Exception('Error while retrieving reverse geocoding coordinates for coordinates ' +
                                str(self.position[0]) + ',' + str(self.position[1]))
            self.address = response['results'][0]['formatted_address']
        return self.address

    def set_coordinates(self, position):
        self.position = position

    def get_coordinates(self, API_key):
        """Returns latitude/longitude of the location's address"""
        if self.position:
            return self.position

        address = self.get_address_for_geocoding()
        request = 'https://maps.googleapis.com/maps/api/geocode/json' + '?address=' + address + '&key=' + API_key
        with urllib.request.urlopen(request) as url:
            json_result = url.read()
            response = json.loads(json_result)
            status = response['status']
            if status != 'OK':
                raise Exception('Error while retrieving geocoding coordinates for address ' + self.address)
            lat = response['results'][0]['geometry']['location']['lat']
            lng = response['results'][0]['geometry']['location']['lng']
            self.position = np.ndarray((2,), buffer=np.array([lat, lng]), dtype=float)
            return self.position


class Depot(Location):
    def __init__(self, position=[], address=''):
        super().__init__(position=position, address=address, location_id=0)
