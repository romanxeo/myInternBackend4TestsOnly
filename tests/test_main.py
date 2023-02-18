
def test_health_check(test_app):
    data = {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == data