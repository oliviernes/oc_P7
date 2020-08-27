from random import choice as rand


class Message:
    """Set Grandpy messages according to API response """

    def __init__(self):
        self.phrase = {
            "positive_address": [
                "Bien sûr mon poussin ! La voici: ",
                "Mais oui, je connais très bien, c'est l'adresse:",
                "Ma mémoire ne me faillit jamais! Voici l'adresse:",
            ],
            "positive_wiki": [
                "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ?",
                "Je connais très bien, on y est allé plein de fois avec ta Mamy. Je t'en dis plus:",
                "J'y suis allé quand j'étais jeune, il y a 60 ans!:",
            ],
            "negative_addresse": [
                "Je ne comprend pas ta question. Parle moi mieux que ça!",
                "Ça ne me dit rien du tout!!",
                "Ta question n'est pas claire. Reformule moi ça!",
            ],
            "negative_wiki": [
                "Je ne connais que l'adresse...",
                "Pas d'histoire à te raconter... Je connais pas tout non plus!",
            ],
        }

    def positive_address(self):
        return rand(self.phrase["positive_address"])

    def positive_wiki(self):
        return rand(self.phrase["positive_wiki"])

    def negative_addresse(self):
        return rand(self.phrase["negative_addresse"])

    def negative_wiki(self):
        return rand(self.phrase["negative_wiki"])
