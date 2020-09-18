import pytest
from flaskapp.backend.messages import Message

class TestMessages:
    """Test Grandypy messages answer"""

    def test_positive_adresse(self, mocker):

        message = Message()

        mocker.patch(
            "flaskapp.backend.messages.rand",
            return_value="Mais t'ai-je déjà raconté"
            " l'histoire de ce quartier qui m'a vu en "
            "culottes courtes ?",
        )

        assert (
            message.positive_address() == "Mais t'ai-je déjà raconté "
            "l'histoire de ce quartier qui m'a vu en culottes courtes ?"
        )

    def test_negative_adresse(self, mocker):

        message = Message()

        mocker.patch(
            "flaskapp.backend.messages.rand",
            return_value="Je ne comprend pas ta question. "
            "Parle moi mieux que ça!",
        )

        assert (
            message.negative_address() == "Je ne comprend pas ta "
            "question. Parle moi mieux que ça!"
        )
