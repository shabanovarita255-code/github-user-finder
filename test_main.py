import json
import os
import pytest
from unittest.mock import patch, MagicMock

import main


# =========================
# TEST: load_favorites empty file
# =========================
def test_load_favorites_empty():
    main.FAVORITES_FILE = "test_fav.json"

    if os.path.exists("test_fav.json"):
        os.remove("test_fav.json")

    assert main.load_favorites() == []


# =========================
# TEST: save + load
# =========================
def test_save_and_load():
    main.FAVORITES_FILE = "test_fav.json"

    data = ["user1", "user2"]
    main.save_favorites(data)

    loaded = main.load_favorites()

    assert loaded == data


# =========================
# TEST: fetch_user success (mock API)
# =========================
@patch("main.requests.get")
def test_fetch_user_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "login": "octocat",
        "html_url": "https://github.com/octocat"
    }

    mock_get.return_value = mock_response

    response = main.fetch_user("octocat")

    assert response.status_code == 200
    assert response.json()["login"] == "octocat"


# =========================
# TEST: fetch_user failure
# =========================
@patch("main.requests.get")
def test_fetch_user_fail(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404

    mock_get.return_value = mock_response

    response = main.fetch_user("unknown_user")

    assert response.status_code == 404


# =========================
# TEST: add duplicate favorite
# =========================
def test_add_duplicate_favorite():
    main.FAVORITES_FILE = "test_fav.json"

    main.save_favorites(["user1"])

    favorites = main.load_favorites()

    item = "user1"

    if item not in favorites:
        favorites.append(item)

    # не должно добавиться второй раз
    assert favorites.count("user1") == 1


# =========================
# TEST: clear favorites
# =========================
def test_clear_favorites():
    main.FAVORITES_FILE = "test_fav.json"

    main.save_favorites(["a", "b"])

    main.save_favorites([])

    assert main.load_favorites() == []