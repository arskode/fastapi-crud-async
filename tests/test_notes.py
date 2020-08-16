import json

import pytest

from src.api.v1.tables import notes
from src.extensions import engine

users_fixture = [
    {"id": 1, "title": "something", "description": "something",},
    {"id": 2, "title": "something else", "description": "something else",},
]


def add_notes(limit: int):
    for item in users_fixture[:limit]:
        query = notes.insert().values(
            title=item["title"], description=item["description"]
        )
        engine.execute(query)


def test_create_note(client):
    request_payload = {
        "title": "something",
        "description": "something else",
    }
    response_payload = {
        "id": 1,
        "title": "something",
        "description": "something else",
    }
    response = client.post("/v1/notes", data=json.dumps(request_payload))

    assert response.status_code == 201
    assert response.json() == response_payload


def test_create_note_invalid_json(client):
    response = client.post(
        "/v1/notes", data=json.dumps({"title": "something"})
    )
    assert response.status_code == 422

    response = client.post(
        "/v1/notes", data=json.dumps({"title": "1", "description": "2"})
    )
    assert response.status_code == 422


def test_read_note(client):
    add_notes(limit=1)

    response = client.get("/v1/notes/1")
    assert response.status_code == 200
    assert response.json() == users_fixture[0]


def test_read_note_incorrect_id(client):
    response = client.get("/v1/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = client.get("/v1/notes/0")
    assert response.status_code == 422


def test_read_all_notes(client):
    add_notes(limit=2)

    response = client.get("/v1/notes")
    assert response.status_code == 200
    assert response.json() == users_fixture


def test_update_note(client):
    add_notes(limit=1)

    request_payload_put = {
        "title": "someone",
        "description": "else",
        "id": 1,
    }
    response = client.put("/v1/notes/1", data=json.dumps(request_payload_put))
    assert response.status_code == 200
    assert response.json() == request_payload_put


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"description": "bar"}, 422],
        [999, {"title": "foo", "description": "bar"}, 404],
        [1, {"title": "1", "description": "bar"}, 422],
        [1, {"title": "foo", "description": "1"}, 422],
        [0, {"title": "foo", "description": "bar"}, 422],
    ],
)
def test_update_note_invalid(client, monkeypatch, id, payload, status_code):
    add_notes(limit=1)

    response = client.put(f"/v1/notes/{id}", data=json.dumps(payload))
    assert response.status_code == status_code


def test_remove_note(client):
    add_notes(limit=1)

    response = client.delete("/v1/notes/1")
    assert response.status_code == 204


def test_remove_note_incorrect_id(client):
    response = client.delete("/v1/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = client.delete("/v1/notes/0")
    assert response.status_code == 422
