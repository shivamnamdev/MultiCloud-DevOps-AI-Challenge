from app import app

def test_rooms_returns_list():
    r = app.test_client().get("/rooms")
    assert r.status_code == 200
    assert len(r.get_json()) >= 1

def test_health():
    assert app.test_client().get("/health").status_code == 200
