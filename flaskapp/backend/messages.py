"""Module to display Grandpy's messages"""

from random import choice as rand


class Message:
    """Set Grandpy messages according to API responses """

    def __init__(self):
        self.phrase = {
            "positive_address": [
                "Bien sûr mon poussin ! La voici: ",
                "Mais oui, je connais très bien, c'est l'adresse:",
                "Ma mémoire ne me faillit jamais! Voici l'adresse:",
            ],
            "positive_wiki": [
                "Mais t'ai-je déjà raconté l'histoire de ce quartier"
                " qui m'a vu en culottes courtes ?",
                "Je connais très bien, on y est allé plein de fois avec"
                " ta Mamy. Je t'en dis plus:",
                "J'y suis allé quand j'étais jeune, il y a 60 ans!:",
            ],
            "negative_address": [
                "Je ne comprend pas ta question. Parle moi mieux que ça!",
                "Ça ne me dit rien du tout!!",
                "Ta question n'est pas claire. Reformule moi ça!",
            ],
            "negative_wiki": [
                "Je ne connais que l'adresse...",
                "Pas d'histoire à te raconter... " "Je connais pas tout non plus!",
            ],
        }

    def positive_address(self):
        """
        Method to display messages in case of an
         address return by Google's API
        """
        return rand(self.phrase["positive_address"])

    def positive_wiki(self):
        """
        Method to display messages in case of
         informations return by Wikipedia's API
        """
        return rand(self.phrase["positive_wiki"])

    def negative_address(self):
        """
        Method to display messages in case of no
         address return by Google's API
        """
        return rand(self.phrase["negative_address"])

    def negative_wiki(self):
        """
        Method to display messages in case of no
         informations return by Wikipedia's API
        """
        return rand(self.phrase["negative_wiki"])
