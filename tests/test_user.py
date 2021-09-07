from starlette.testclient import TestClient


class TestUser:
    _ENDPOINT = "/v1/users/"

    def test_user_creation_with_success(self, client: TestClient):
        response = client.post(
            self._ENDPOINT,
            json={
                "email": "testuser@example.com",
                "password": "Test123#",
            },
        )

        assert response.status_code == 201

    def test_user_creation_with_conflicting_email(self, client: TestClient):
        response = client.post(
            self._ENDPOINT,
            json={
                "email": "testuser@example.com",
                "password": "Test123#",
            },
        )

        assert response.status_code == 409

    def test_users_list_with_single_user(
        self, client: TestClient, existing_user_id: int
    ):
        response = client.get(self._ENDPOINT)

        assert response.status_code == 200

    def test_existing_user_retrieval(self, client: TestClient, existing_user_id: int):
        response = client.get(f"{self._ENDPOINT}{existing_user_id}/")

        assert response.status_code == 200
