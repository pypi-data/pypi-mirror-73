import requests
import ast
import json

base_url = "https://developers.zomato.com/api/v2.1/"


class Zomato:
    """
    Wrapper class to the zomato web api.
    original source: https://github.com/sharadbhat/Zomatopy
    """

    def __init__(self, key):
        self.user_key = key

    def get_categories(self):
        """
        @params: None.
        @return: Returns a dictionary of IDs and their respective category names.
        """

        headers = {'Accept': 'application/json', 'user-key': self.user_key}
        r = requests.get(base_url + "categories", headers=headers).content.decode("utf-8")
        a = ast.literal_eval(r)

        self.is_key_invalid(a)
        self.is_rate_exceeded(a)

        categories = {}
        for category in a['categories']:
            categories.update({category['categories']['id']: category['categories']['name']})

        return categories

    def get_city_id(self, city_name=None, state_name=None):
        """
        @params: string, city_name.
        @return:
        Returns the ID for the city given as input.
        If no parameters are passed, returns city id based on current location
        """

        if city_name is None or state_name is None:
            lat, lon = self.get_geo_coords()
            headers = {'Accept': 'application/json', 'user-key': self.user_key}
            r = requests.get(base_url + "cities?lat=" + str(lat) + "&lon=" + str(lon), headers=headers).\
                content.decode("utf-8")
            a = json.loads(r)
            if len(a['location_suggestions']) == 0:
                raise Exception("current city's ID cannot be found!")
            else:
                return a['location_suggestions'][0]['id']

        if not city_name.isalpha():
            raise ValueError('InvalidCityName')

        headers = {'Accept': 'application/json', 'user-key': self.user_key}
        r = requests.get(base_url + "cities?q=" + city_name, headers=headers).content.decode("utf-8")
        a = json.loads(r)

        self.is_key_invalid(a)
        self.is_rate_exceeded(a)

        if len(a['location_suggestions']) == 0:
            raise Exception('invalid_city_name')
        elif 'name' in a['location_suggestions'][0]:
            city_state = a['location_suggestions'][0]['name'].lower()
            city, state = str(city_state.split(',')[0]), str(city_state.split(',')[1])
            if city == str(city_name).lower() and state == str(state_name):
                return a['location_suggestions'][0]['id']
            else:
                raise ValueError('InvalidCityId')

    def get_city_name(self, city_id):
        """
        @params: City ID int or str.
        @return: the name of the city ID.
        """

        self.is_valid_city_id(city_id)

        headers = {'Accept': 'application/json', 'user-key': self.user_key}
        r = requests.get(base_url + "cities?city_ids=" + str(city_id), headers=headers).content.decode("utf-8")
        a = json.loads(r)

        self.is_key_invalid(a)
        self.is_rate_exceeded(a)

        if a['location_suggestions'][0]['country_name'] == "":
            raise ValueError('InvalidCityId')
        else:
            temp_city_id = a['location_suggestions'][0]['id']
            if temp_city_id == str(city_id):
                return a['location_suggestions'][0]['name']

    def get_collections(self, city_id, limit=None):
        """
        @param
        city_id: int/str City ID as input.
        limit: optional parameter. displays limit number of result.
        @return
        python dictionary of Zomato restaurant collections in a city and their respective URLs.
        """

        self.is_valid_city_id(city_id)

        headers = {'Accept': 'application/json', 'user-key': self.user_key}
        if limit is None:
            r = requests.get(base_url + "collections?city_id=" + str(city_id), headers=headers).content.decode(
                "utf-8")
        else:
            if str(limit).isalpha():
                raise ValueError('LimitNotInteger')
            else:
                r = (requests.get(base_url + "collections?city_id=" + str(city_id) + "&count=" + str(limit),
                                  headers=headers).content).decode("utf-8")
        a = json.loads(r)

        self.is_key_invalid(a)
        self.is_rate_exceeded(a)

        collections = {}
        for collection in a['collections']:
            collections.update({collection['collection']['title']: collection['collection']['url']})

        return collections

    def get_cuisines(self, city_id):
        """
        @params: City ID int/str
        @return:
        a sorted dictionary by ID of all cuisine IDs and their respective cuisine names.
        key: cuisine name
        value: dictionary
        """

        self.is_valid_city_id(city_id)

        headers = {'Accept': 'application/json', 'user-key': self.user_key}
        r = requests.get(base_url + "cuisines?city_id=" + str(city_id), headers=headers).content.decode("utf-8")
        a = ast.literal_eval(r)

        self.is_key_invalid(a)
        self.is_rate_exceeded(a)

        if len(a['cuisines']) == 0:
            raise ValueError('InvalidCityId')
        temp_cuisines = {}
        cuisines = {}
        for cuisine in a['cuisines']:
            # temp_cuisines.update({cuisine['cuisine']['cuisine_id']: cuisine['cuisine']['cuisine_name']})
            temp_cuisines.update({cuisine['cuisine']['cuisine_name']: cuisine['cuisine']['cuisine_id']})

        for cuisine in sorted(temp_cuisines):
            cuisines.update({cuisine: temp_cuisines[cuisine]})

        return cuisines

    def get_establishment_types(self, city_id):
        """
        @params: City ID (int/str).
        @return: sorted dictionary of all establishment type IDs and their respective establishment type names.
        """

        self.is_valid_city_id(city_id)

        headers = {'Accept': 'application/json', 'user-key': self.user_key}
        r = requests.get(base_url + "establishments?city_id=" + str(city_id), headers=headers).content.decode("utf-8")
        a = ast.literal_eval(r)

        self.is_key_invalid(a)
        self.is_rate_exceeded(a)

        temp_establishment_types = {}
        establishment_types = {}
        if 'establishments' in a:
            for establishment_type in a['establishments']:
                temp_establishment_types.update(
                    {establishment_type['establishment']['id']: establishment_type['establishment']['name']})

            for establishment_type in sorted(temp_establishment_types):
                establishment_types.update({establishment_type: temp_establishment_types[establishment_type]})

            return establishment_types
        else:
            raise ValueError('InvalidCityId')

    def get_nearby_restaurants(self, latitude="", longitude=""):
        """
        @params: latitude and longitude of current or interested location.
        @return: a dictionary of Restaurant IDs and their corresponding Zomato URLs.
        """

        """obtains the current location's latitude and longitude if none is provided"""
        if latitude == "" or longitude == "":
            latitude, longitude = self.get_geo_coords()

        try:
            float(latitude)
            float(longitude)
        except ValueError:
            raise ValueError('InvalidLatitudeOrLongitude')

        headers = {'Accept': 'application/json', 'user-key': self.user_key}
        r = (requests.get(base_url + "geocode?lat=" + str(latitude) + "&lon=" + str(longitude),
                          headers=headers).content).decode("utf-8")
        a = json.loads(r)

        nearby_restaurants = {}
        for nearby_restaurant in a['nearby_restaurants']:
            nearby_restaurants.update({nearby_restaurant['restaurant']['id']: nearby_restaurant['restaurant']['url']})

        return nearby_restaurants

    def get_restaurant(self, restaurant_id):
        """
        @params: Restaurant ID (int/str) as input.
        @return: a dictionary of restaurant details.
        """

        self.is_valid_restaurant_id(restaurant_id)

        headers = {'Accept': 'application/json', 'user-key': self.user_key}
        r = requests.get(base_url + "restaurant?res_id=" + str(restaurant_id), headers=headers).content.decode(
            "utf-8")
        a = json.loads(r)

        if 'code' in a:
            if a['code'] == 404:
                raise ('InvalidRestaurantId')

        restaurant_details = {}
        restaurant_details.update({"name": a['name']})
        restaurant_details.update({"url": a['url']})
        restaurant_details.update({"location": a['location']['address']})
        restaurant_details.update({"city": a['location']['city']})
        restaurant_details.update({"city_ID": a['location']['city_id']})
        restaurant_details.update({"user_rating": a['user_rating']['aggregate_rating']})

        restaurant_details = DotDict(restaurant_details)
        return restaurant_details

    def restaurant_search(self, query="", latitude="", longitude="", radius="", cuisines="", limit=5):
        """
        @params
        query: string keyword to query.
        latitude: latitude of interested place.
        longitude: longitude of interested place.
        radius: search restaurants within a radius in meters
        cuisines: multiple cuisines as input in string format.
        @return: a list of Restaurants.
        """

        cuisines = "%2C".join(cuisines.split(","))

        """obtains the current location's latitude and longitude if none is provided"""
        if latitude == "" or longitude == "":
            latitude, longitude = self.get_geo_coords()

        if str(limit).isalpha():
            raise ValueError('LimitNotInteger')
        headers = {'Accept': 'application/json', 'user-key': self.user_key}
        r = (requests.get(
            base_url + "search?q=" + str(query) + "&count=" + str(limit) + "&lat=" + str(latitude) + "&lon=" + str(
                longitude) + "&radius=" + str(radius) + "&cuisines=" + str(cuisines), headers=headers).content).decode("utf-8")
        a = json.loads(r)

        if a['results_found'] == 0:
            return []
        else:
            return a  # dictionary of all restaurants

    def is_valid_restaurant_id(self, restaurant_ID):
        """
        Checks if the Restaurant ID is valid or invalid.
        If invalid, throws a InvalidRestaurantId Exception.
        @param: id of a restaurant
        @return:
        None

        """
        restaurant_ID = str(restaurant_ID)
        if not restaurant_ID.isnumeric():
            raise ValueError('InvalidRestaurantId')

    def is_valid_city_id(self, city_ID):
        """
        Checks if the City ID is valid or invalid.
        If invalid, throws a InvalidCityId Exception.
        @param: id of a city
        @return: None
        """
        city_ID = str(city_ID)
        if not city_ID.isnumeric():
            raise ValueError('InvalidCityId')

    def is_key_invalid(self, a):
        """
        Checks if the API key provided is valid or invalid.
        If invalid, throws a InvalidKey Exception.
        @params: return of the web request in 'json'
        @return: None
        """
        if 'code' in a:
            if a['code'] == 403:
                raise ValueError('InvalidKey')

    def is_rate_exceeded(self, a):
        """
        Checks if the request limit for the API key is exceeded or not.
        If exceeded, throws a ApiLimitExceeded Exception.
        @params: return of the web request in 'json'
        @return: None
        """
        if 'code' in a:
            if a['code'] == 440:
                raise Exception('ApiLimitExceeded')

    def get_geo_coords(self):
        """
        captures latitude and longitude based on current location
        @params: None
        @return: latitude, longitude
        """

        ip_request = requests.get('https://get.geojs.io/v1/ip.json')
        my_ip = ip_request.json()['ip']
        geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
        geo_request = requests.get(geo_request_url)
        geo_data = geo_request.json()
        return geo_data['latitude'], geo_data['longitude']  # latitude, longitude


class DotDict(dict):
    """
    Dot notation access to dictionary attributes
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
