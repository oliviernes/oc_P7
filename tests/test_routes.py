import pytest
from flaskapp import app
from flaskapp.backend.api import Google, WikiMedia
from flaskapp.backend.messages import Message


@pytest.fixture
def client():
    client = app.test_client()
    return client


def test_ajax_no_response_from_Google_api(client, mocker):

    mocker.patch(
                "flaskapp.backend.api.Google.geoloc",
                return_value={"status": False}
                )

    mocker.patch(
        "flaskapp.backend.messages.rand",
        return_value="Je ne comprend pas ta question. "
        "Parle moi mieux que ça!",
    )

    response = client.post(
        "/ajax/", data={"Question": "azertgdsds"}
    )

    """
    get_json() is a Flask method here. Not to be confused with get_json()
    of the GetJson class.
    """
    data = response.get_json()

    assert response.status_code == 200
    assert data == {
        "messages": ["Je ne comprend pas ta question. "
                     "Parle moi mieux que ça!"],
    }


def test_ajax_no_question(client, mocker):

    mocker.patch(
        "flaskapp.backend.messages.rand",
        return_value="Je ne comprend pas ta question. "
        "Parle moi mieux que ça!",
    )

    response = client.post("/ajax/", data={"Question": ""})

    data = response.get_json()

    assert response.status_code == 200
    assert data == {
        "messages": ["Mais pose donc une question!!"],
    }


def test_ajax_response_from_Google_api_but_not_Wikipedia(client, mocker):

    mocker.patch(
        "flaskapp.backend.api.Google.geoloc",
        return_value={
            "locate": {"lat": 48.8975156, "lng": 2.3833993},
            "district": "Quai de la Charente",
            "address": "10 Quai de la Charente, 75019 Paris, France",
            "status": True,
        },
    )

    mocker.patch(
        "flaskapp.backend.api.WikiMedia.get_infos",
        return_value={"summary": "", "url": "", "status": False},
    )

    mocker.patch(
        "flaskapp.backend.messages.Message.positive_address",
        return_value="Bien sûr mon poussin ! La voici: ",
    )

    mocker.patch(
        "flaskapp.backend.messages.Message.negative_wiki",
        return_value="Ça ne me dit rien du tout!!",
    )

    response = client.post(
        "/ajax/", data={"Question": "openclassrooms"}
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data == {
        "locate": {"lat": 48.8975156, "lng": 2.3833993},
        "address": "10 Quai de la Charente, 75019 Paris, France",
        "messages": [
            "Bien sûr mon poussin ! La voici: ",
            "Ça ne me dit rien du tout!!",
        ],
    }


def test_ajax_response_from_Google_api_and_Wikipedia(client, mocker):

    mocker.patch(
        "flaskapp.backend.api.Google.geoloc",
        return_value={
            "locate": {"lat": 48.8975156, "lng": 2.3833993},
            "district": "Quai de la Charente",
            "address": "10 Quai de la Charente, 75019 Paris, France",
            "status": True,
        },
    )

    mocker.patch(
        "flaskapp.backend.api.WikiMedia.get_infos",
        return_value={
            "summary": "Un résumé de wikipedia",
            "url": "https://fr.wikipedia.org/wiki/OpenClassrooms",
            "status": True,
        },
    )

    mocker.patch(
        "flaskapp.backend.messages.Message.positive_address",
        return_value="Bien sûr mon poussin ! La voici: ",
    )

    mocker.patch(
        "flaskapp.backend.messages.Message.positive_wiki",
        return_value="J'y suis allé quand j'étais jeune, il y a 60 ans!:",
    )

    response = client.post(
        "/ajax/", data={"Question": "openclassrooms"}
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data == {
        "locate": {"lat": 48.8975156, "lng": 2.3833993},
        "address": "10 Quai de la Charente, 75019 Paris, France",
        "messages": [
            "Bien sûr mon poussin ! La voici: ",
            "J'y suis allé quand j'étais jeune, il y a 60 ans!:",
        ],
        "summary": "Un résumé de wikipedia",
        "url": "https://fr.wikipedia.org/wiki/OpenClassrooms",
    }
