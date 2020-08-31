"""Module getting informations from APIs"""

import re
import logging
from pprint import pformat as pf
import requests
from mediawiki import MediaWiki
import mediawiki
import simplejson
from flaskapp.backend.parser import Parser
from config import GEOCODE_URL, GOOGLE_API


logger = logging.getLogger()


class GetJson:
    """Class allowing to send request to the API."""

    def __init__(self, url, params):
        self.url = url
        self.params = params

    def get_json(self):
        """Method to request the API."""
        try:
            req = requests.get(self.url, self.params, timeout=20)
            """returns an HTTPError object if an error has occurred
             during the process."""
            req.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print("An HTTP error occurred.")
            print(str(error))
            logging.exception("Exception occurred")
        except requests.exceptions.ConnectionError as error:
            print(
                "OOPS!! Connection Error. Make sure you are connected"
                " to Internet. Technical Details given below.\n"
            )
            print(str(error))
            logging.exception("Exception occurred")
        except requests.exceptions.Timeout as error:
            print("OOPS!! Timeout Error")
            print(str(error))
            logging.exception("Exception occurred")
        except requests.exceptions.RequestException as error:
            print("OOPS!! General Error")
            print(str(error))
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
    """Google Maps Geocode API class."""

    def __init__(self):
        self.key = GOOGLE_API
        self.geocode_url = GEOCODE_URL
        self.loc_data = {"status": True}

    def geoloc(self, question):
        """Give coordinates and informations of the user's query."""

        parsing = Parser()
        question_parsed = parsing.parse(question)

        payload = {
            "key": self.key,
            "address": question_parsed,
        }

        response = GetJson(self.geocode_url, payload).get_json()

        try:
            locate = response["results"][0]["geometry"]["location"]
            address = response["results"][0]["formatted_address"]
            address_components = response["results"][0]["address_components"]
            district = "llkdsoisqz54"

            for add in address_components:
                if add["types"][0] == "route":
                    district = add["long_name"]
                    break
                elif add["types"][0] == "locality":
                    district = add["long_name"]

        except IndexError as error:
            self.loc_data = {
                "status": False,
                "error": {"IndexError": str(error), "response": response, },
            }
            logging.exception(f"loc_data=\n{pf(self.loc_data)}")

        except KeyError as error:
            self.loc_data = {
                "status": False,
                "error": {"KeyError": str(error), "response": response, },
            }
            logging.exception(f"loc_data=\n{pf(self.loc_data)}")

        except TypeError as error:
            self.loc_data = {
                "status": False,
                "error": {"TypeError": str(error), "response": response, },
            }
            logging.exception(f"loc_data=\n{pf(self.loc_data)}")

        else:
            if response["status"] == "OK":
                return {
                    "locate": locate,
                    "district": district,
                    "address": address
                }
            self.loc_data = {
                "status": False,
            }


class WikiMedia:
    """Wikipedia class."""

    def __init__(self):
        self.wikipedia = MediaWiki()
        self.wikipedia.language = "fr"
        self.wiki_data = {"status": True}

    def get_infos(self, query):
        """Method allowing to retrieve informations from wikipedia.fr."""
        try:
            titles = self.wikipedia.search(query)
            if len(titles) > 0:
                infos = self.wikipedia.page(titles[0])
                summary = self.wikipedia.summary(titles[0], sentences=3)

                # Add regex  to remove == string == in summary:
                summary = re.sub(r"={2}\s.+={2}", r"", summary)

                url = infos.url

            else:
                summary = ""
                url = ""
                self.wiki_data = {"status": False}

        # Use one except block in case of disambiguations errors. Allow to search for the next
        # title if the first one lead to a disambiguation error.

        except mediawiki.exceptions.DisambiguationError:
            if len(titles) > 1:
                try:
                    infos = self.wikipedia.page(titles[1])
                    summary = self.wikipedia.summary(titles[1], sentences=3)
                    summary = re.sub(r"={2}\s.+={2}", r"", summary)
                    url = infos.url

                except mediawiki.exceptions.DisambiguationError:
                    summary = ""
                    url = ""
                    self.wiki_data = {"status": False}
                    logging.exception("Exception occurred")
            else:
                summary = ""
                url = ""
                self.wiki_data = {"status": False}
                logging.exception("Exception occurred")

        return {"summary": summary, "url": url}
