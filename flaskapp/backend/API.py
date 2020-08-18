import requests
from flaskapp.backend.parser import Parser
from config import GEOCODE_URL, GOOGLE_API, DETAIL_URL

import pdb

class Get_json:
    """Class allowing to send request to the API"""

    def __init__(self, url, params):
        self.url = url
        self.params = params

    def get_json(self):

        try:
            req = requests.get(self.url, self.params, timeout=20)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
        except KeyboardInterrupt:
            print("Someone closed the program")

        try:
            response = req.json()
        except simplejson.errors.JSONDecodeError:
            print("Not a json answer")
        else:
            return response


class Google:
    """Google Maps and place APIs class"""

    def __init__(self):
        self.key = GOOGLE_API
        self.geocode_url = GEOCODE_URL
        self.detail_url = DETAIL_URL

    def detail(self, place_id):
        "Give informations about the user's query"

        payload = {
            'key': self.key,
            'place_id': place_id
        }

        # req = requests.get(self.detail_url, params=payload)
        # response = req.json()

        response = Get_json(self.detail_url, payload).get_json()

        address = response['result']['formatted_address']
        rating = response['result'].get('rating', "no_rating")
        coordinates = response['result']['geometry']['location']
        breakpoint()

        return { 'address': address, 'rating': rating , 'coordinates': coordinates }


    def geoloc(self, question):
        "Give coordinates and place_id of the user's query"

        parsing = Parser()
        question_parsed = parsing.parse(question)

        payload = {
            'key': self.key,
            'address': question_parsed,
        }

        # req = requests.get(self.geocode_url, params=payload)
        # response = req.json()
        
        response = Get_json(self.geocode_url, payload).get_json()

        locate = response['results'][0]['geometry']['location']
        place_id = response['results'][0]['place_id']

        return { 'locate': locate, 'place_id': place_id }
