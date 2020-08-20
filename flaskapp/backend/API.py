import requests
from flaskapp.backend.parser import Parser
from config import GEOCODE_URL, GOOGLE_API, DETAIL_URL, SEARCH_URL
from mediawiki import MediaWiki
import mediawiki
import simplejson
from pprint import pformat as pf

import logging

logger = logging.getLogger()

import pdb

class Get_json:
    """Class allowing to send request to the API"""

    def __init__(self, url, params):
        self.url = url
        self.params = params

    def get_json(self):

        try:
            req = requests.get(self.url, self.params, timeout=20)
            req.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("An HTTP error occurred.")
            print(str(e))
            logging.exception("Exception occurred")
        except requests.exceptions.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            logging.exception("Exception occurred")
        except requests.exceptions.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
            logging.exception("Exception occurred")
        except requests.exceptions.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            logging.exception("Exception occurred")
        except KeyboardInterrupt:
            print("Someone closed the program")

        try:
            response = req.json()
        except simplejson.errors.JSONDecodeError:
            print("Not a json answer")
            logging.exception("Exception occurred")
        else:
            return response


class Google:
    """Google Maps and place APIs class"""

    def __init__(self):
        self.key = GOOGLE_API
        self.geocode_url = GEOCODE_URL
        self.loc_data = {'status' : True}

    def geoloc(self, question):
        "Give coordinates and place_id of the user's query"

        parsing = Parser()
        question_parsed = parsing.parse(question)

        payload = {
            'key': self.key,
            'address': question_parsed,
        }
        
        response = Get_json(self.geocode_url, payload).get_json()


        try:
            locate = response['results'][0]['geometry']['location']
            address = response['results'][0]['formatted_address']
            address_components = response['results'][0]['address_components']

            for address in address_components:
                if address['types'][0] == 'route':
                    district = address['long_name']

        except IndexError as error:
            self.loc_data = {
                'status': False,
                'error': {
                    'IndexError': str(error),
                    'response': response,
                }
            }
            breakpoint()
            logging.exception("loc_data=\n{}".format(pf(self.loc_data)))

        except KeyError as error:
            self.loc_data = {
                'status': False,
                'error': {
                    'KeyError': str(error),
                    'response': response,
                }
            }
            logging.exception("loc_data=\n{}".format(pf(self.loc_data)))
        
        except TypeError as error:
            self.loc_data = {
                'status': False,
                'error': {
                    'TypeError': str(error),
                    'response': response,
                }
            }
            logging.exception("loc_data=\n{}".format(pf(self.loc_data)))

        else:
            if response['status'] == "OK":
                return { 'locate': locate, 'district': district, 'address': address }


class WikiMedia:

    def __init__(self):
        self.wikipedia = MediaWiki()
        self.wikipedia.language = "fr"

    def get_infos(self, query):
        try:
            titles = self.wikipedia.search(query)
            infos = self.wikipedia.page(titles[0])
            summary = infos.summarize(chars = 500)
            url = infos.url

        except mediawiki.exceptions.DisambiguationError:
            summary = ""
            url = ""

        return { 'summary': summary, 'url': url }