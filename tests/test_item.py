from starlette.testclient import TestClient


class TestItem:
    _ENDPOINT = "/v1/items/"

    def test_item_creation_with_success(
        self, client: TestClient, existing_user_id: int
    ):
        response = client.post(
            self._ENDPOINT,
            json={
                "title": "Test title",
                "description": "Lorem ipsum dolor sit amet ...",
                "owner_id": existing_user_id,
            },
        )

        assert response.status_code == 200

    def test_item_retrieval_with_sucess(
        self, client: TestClient, existing_item_id: int
    ):
        response = client.get(f"{self._ENDPOINT}{existing_item_id}/")

        assert response.status_code == 200

    def test_item_creation_for_non_existent_user(self, client: TestClient):
        response = client.post(
            self._ENDPOINT,
            json={
                "title": "Test title",
                "description": "Lorem ipsum dolor sit amet ...",
                "owner_id": 999,
            },
        )

        assert response.status_code == 409

    def test_items_list_with_single_item(
        self, client: TestClient, existing_item_id: int
    ):
        response = client.get(self._ENDPOINT)

        assert response.status_code == 200
