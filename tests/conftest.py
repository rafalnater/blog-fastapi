import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from core.db import Base, get_db
from main import app


@pytest.fixture(scope="module")
def client():
    engine = create_engine(
        "sqlite:///./test.db", connect_args={"check_same_thread": False}
    )

    # enable foreign keys check in sqlite
    from sqlalchemy import event

    event.listen(
        engine,
        "connect",
        lambda dbapi_con, con_record: dbapi_con.execute("pragma foreign_keys=ON"),
    )

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # create testing database schema
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    # drop the testing database entirely afterwards
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def existing_user_id(client: TestClient) -> int:
    return client.post(
        "/v1/users/",
        json={
            "email": "dummy@example.com",
            "password": "Test123#",
        },
    ).json()["id"]


@pytest.fixture(scope="module")
def existing_item_id(client: TestClient, existing_user_id: int) -> int:
    return client.post(
        "/v1/items/",
        json={
            "title": "Test title",
            "description": "Lorem ipsum dolor sit amet ...",
            "owner_id": existing_user_id,
        },
    ).json()["id"]
