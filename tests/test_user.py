from httpx import AsyncClient


async def test_get_users(ac: AsyncClient):
    response = await ac.get("/users")
    assert response.status_code == 200
    assert response.json().get("result").get("users") == []


async def test_bad_create_user_not_password(ac: AsyncClient):
    payload = {
      "user_password": "",
      "user_password_repeat": "",
      "user_email": "test@test.test",
      "user_name": "test"
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 422


async def test_bad_create_user_low_password(ac: AsyncClient):
    payload = {
      "user_password": "tet",
      "user_password_repeat": "tet",
      "user_email": "test@test.test",
      "user_name": "test"
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 422


async def test_bad_create_user_dont_match(ac: AsyncClient):
    payload = {
      "user_password": "test",
      "user_password_repeat": "tess",
      "user_email": "test@test.test",
      "user_name": "test"
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 422


async def test_bad_create_user_no_valid_email(ac: AsyncClient):
    payload = {
      "user_password": "test",
      "user_password_repeat": "tess",
      "user_email": "test",
      "user_name": "test"
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 422


async def test_create_user_one(ac: AsyncClient):
    payload = {
      "user_password": "testt",
      "user_password_repeat": "testt",
      "user_email": "test1@test.com",
      "user_name": "test1",
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 1


async def test_create_user_error(ac: AsyncClient):
    payload = {
      "user_password": "testt",
      "user_password_repeat": "testt",
      "user_email": "test1@test.com",
      "user_name": "test2",
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 400


async def test_create_user_two(ac: AsyncClient):
    payload = {
      "user_password": "testt",
      "user_password_repeat": "testt",
      "user_email": "test2@test.com",
      "user_name": "test2",
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 2


async def test_create_user_three(ac: AsyncClient):
    payload = {
      "user_password": "testt",
      "user_password_repeat": "testt",
      "user_email": "test3@test.com",
      "user_name": "test3",
    }
    response = await ac.post("/user", json=payload)
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 3


async def test_get_users_list(ac: AsyncClient):
    response = await ac.get("/users")
    assert response.status_code == 200
    assert len(response.json().get("result").get("users")) == 3


async def test_get_user_by_id(ac: AsyncClient):
    response = await ac.get("/user?user_id=1")
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 1
    assert response.json().get("result").get("user_email") == 'test1@test.com'
    assert response.json().get("result").get("user_name") == 'test1'


async def test_bad_get_user_by_id(ac: AsyncClient):
    response = await ac.get("/user?user_id=4")
    assert response.status_code == 404


async def test_update_user_one(ac: AsyncClient):
    payload = {
      "user_name": "test1NEW",
    }
    response = await ac.put("/user?user_id=1", json=payload)
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 1


async def test_get_user_by_id_updates(ac: AsyncClient):
    response = await ac.get("/user?user_id=1")
    assert response.status_code == 200
    assert response.json().get("result").get("user_id") == 1
    assert response.json().get("result").get("user_email") == 'test1@test.com'
    assert response.json().get("result").get("user_name") == 'test1NEW'


async def test_update_user_not_exist(ac: AsyncClient):
    payload = {
      "user_name": "test1NEW",
    }
    response = await ac.put("/user?user_id=4", json=payload)
    assert response.status_code == 404


async def test_delete_user_one(ac: AsyncClient):
    response = await ac.delete("/user?user_id=1")
    assert response.status_code == 200


async def test_get_users_list_after_delete(ac: AsyncClient):
    response = await ac.get("/users")
    assert response.status_code == 200
    assert len(response.json().get("result").get("users")) == 2


async def test_bad_login_try(ac: AsyncClient):
    payload = {
        "user_email": "test2@test.com",
        "user_password": "tess",
    }
    response = await ac.post("/auth/login", json=payload)
    assert response.status_code == 401
    assert response.json().get('detail') == 'Incorrect username or password'


async def test_login_try(ac: AsyncClient, login_user):
    response = await login_user("test2@test.com", "testt")
    assert response.status_code == 200
    assert response.json().get('result').get('token_type') == 'Bearer'


async def test_auth_me(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}"
    }
    response = await ac.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json().get('result').get('user_name') == "test2"
    assert response.json().get('result').get('user_email') == "test2@test.com"
    assert response.json().get('result').get('user_id') == 2


async def test_bad_auth_me(ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer sdffaf.afdsg.rtrwtrete",
    }
    response = await ac.get("/auth/me", headers=headers)
    assert response.status_code == 401
