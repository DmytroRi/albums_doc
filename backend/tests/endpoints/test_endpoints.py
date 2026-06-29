from fastapi.testclient import TestClient


def test_health_endpoint_from_production_app():
    from app.main import app

    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_album_crud_happy_path_and_search(client: TestClient):
    create_response = client.post(
        "/albums",
        json={"title": "Blue", "release_date": "1971-06-22", "grade": 5},
    )
    assert create_response.status_code == 201
    album = create_response.json()
    assert album == {
        "id": album["id"],
        "title": "Blue",
        "release_date": "1971-06-22",
        "grade": 5.0,
    }

    album_id = album["id"]
    assert client.get(f"/albums/{album_id}").json()["title"] == "Blue"
    assert client.get("/albums/search", params={"q": "blu"}).json()[0]["id"] == album_id

    patch_response = client.patch(f"/albums/{album_id}", json={"grade": 4.5})
    assert patch_response.status_code == 200
    assert patch_response.json()["grade"] == 4.5

    delete_response = client.delete(f"/albums/{album_id}")
    assert delete_response.status_code == 204
    assert client.get(f"/albums/{album_id}").status_code == 404


def test_album_endpoint_payload_validation(client: TestClient):
    missing_title_response = client.post("/albums", json={"grade": 4})
    assert missing_title_response.status_code == 422

    invalid_grade_response = client.post("/albums", json={"title": "Bad", "grade": 7})
    assert invalid_grade_response.status_code == 422

    invalid_query_response = client.get("/albums/search", params={"q": ""})
    assert invalid_query_response.status_code == 422

    invalid_limit_response = client.get("/albums", params={"limit": 501})
    assert invalid_limit_response.status_code == 422


def test_named_resource_crud_endpoints(client: TestClient):
    resources = [
        ("artists", "Nina Simone"),
        ("genres", "Soul"),
        ("vibes", "Reflective"),
    ]

    for endpoint, name in resources:
        created = client.post(f"/{endpoint}", json={"name": name})
        assert created.status_code == 201
        record_id = created.json()["id"]

        assert client.get(f"/{endpoint}").status_code == 200
        assert client.get(f"/{endpoint}/{record_id}").json()["name"] == name

        updated = client.patch(f"/{endpoint}/{record_id}", json={"name": f"{name} Updated"})
        assert updated.status_code == 200
        assert updated.json()["name"] == f"{name} Updated"

        assert client.post(f"/{endpoint}", json={}).status_code == 422
        assert client.get(f"/{endpoint}/999999").status_code == 404
        assert client.delete(f"/{endpoint}/{record_id}").status_code == 204
        assert client.delete(f"/{endpoint}/{record_id}").status_code == 404


def test_track_crud_and_foreign_key_payload_validation(client: TestClient):
    album_id = client.post("/albums", json={"title": "Kind of Blue"}).json()["id"]

    created = client.post(
        "/tracks",
        json={
            "title": "So What",
            "track_order": 1,
            "length_seconds": 545,
            "album_id": album_id,
        },
    )
    assert created.status_code == 201
    track_id = created.json()["id"]
    assert created.json()["album_id"] == album_id

    assert client.get(f"/tracks/{track_id}").json()["title"] == "So What"
    assert client.patch(f"/tracks/{track_id}", json={"track_order": 2}).json()["track_order"] == 2
    assert client.post("/tracks", json={"title": "Incomplete"}).status_code == 422
    assert client.get("/tracks/999999").status_code == 404
    assert client.delete(f"/tracks/{track_id}").status_code == 204


def test_link_resource_crud_endpoints(client: TestClient):
    album_id = client.post("/albums", json={"title": "Vespertine"}).json()["id"]
    artist_id = client.post("/artists", json={"name": "Björk"}).json()["id"]
    genre_id = client.post("/genres", json={"name": "Electronic"}).json()["id"]
    vibe_id = client.post("/vibes", json={"name": "Glacial"}).json()["id"]
    track_id = client.post(
        "/tracks",
        json={"title": "Hidden Place", "track_order": 1, "album_id": album_id},
    ).json()["id"]

    cases = [
        ("album_artist_links", {"album_id": album_id, "artist_id": artist_id}, f"{album_id}/{artist_id}"),
        ("album_genre_links", {"album_id": album_id, "genre_id": genre_id}, f"{album_id}/{genre_id}"),
        ("album_vibe_links", {"album_id": album_id, "vibe_id": vibe_id}, f"{album_id}/{vibe_id}"),
        ("track_genre_links", {"track_id": track_id, "genre_id": genre_id}, f"{track_id}/{genre_id}"),
        ("track_vibe_links", {"track_id": track_id, "vibe_id": vibe_id}, f"{track_id}/{vibe_id}"),
    ]

    for endpoint, payload, path in cases:
        created = client.post(f"/{endpoint}", json=payload)
        assert created.status_code == 201
        assert created.json() == payload
        assert client.get(f"/{endpoint}/{path}").json() == payload
        assert client.get(f"/{endpoint}").status_code == 200
        assert client.post(f"/{endpoint}", json={}).status_code == 422
        assert client.get(f"/{endpoint}/999999/999999").status_code == 404
        assert client.delete(f"/{endpoint}/{path}").status_code == 204
        assert client.delete(f"/{endpoint}/{path}").status_code == 404
