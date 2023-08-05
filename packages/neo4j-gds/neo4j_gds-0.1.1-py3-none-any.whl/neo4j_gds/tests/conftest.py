import pytest

from neo4j_gds.projection import ProjectionIdentity, NativeProjection
from neo4j_gds.query import GraphConnection
from neo4j_gds.tests.config import AppConfig


@pytest.fixture(scope="session")
def app_config():
    return AppConfig.from_path("neo4j_gds/tests/.env")


@pytest.fixture(scope="session")
def graph_connection(app_config) -> GraphConnection:
    return GraphConnection.to_neo4j(
        uri=f"{app_config.neo4j.scheme}://{app_config.neo4j.host}:{app_config.neo4j.port}",
        password=app_config.neo4j.password,
    )


@pytest.fixture(scope="session")
def artist_user_projection(graph_connection):
    projection = NativeProjection(
        graph_connection, ProjectionIdentity(labels=("Artist", "User"))
    )
    projection.create()
    yield projection

    projection.delete()
