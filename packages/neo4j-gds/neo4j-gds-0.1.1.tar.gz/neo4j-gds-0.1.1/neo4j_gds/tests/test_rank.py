from neo4j_gds.algorithms.rank import (
    StreamPageRank,
    StreamArticleRank,
    WritePageRank,
    WriteArticleRank,
)
from neo4j_gds.algorithms.rank_configuration import RankConfiguration
from neo4j_gds.projection import Projection
from neo4j_gds.queries.basic import RemoveProperty
from neo4j_gds.query import Connection


def test_stream_pagerank(
    graph_connection: Connection, artist_user_projection: Projection
):
    results = StreamPageRank(
        graph_connection, artist_user_projection, RankConfiguration()
    ).run()
    assert results


def test_write_pagerank(
    graph_connection: Connection, artist_user_projection: Projection
):
    results = WritePageRank(
        graph_connection,
        artist_user_projection,
        RankConfiguration(write_property="test_1"),
    ).run()
    assert results
    RemoveProperty(graph_connection, "test_1").run()


def test_stream_articlerank(
    graph_connection: Connection, artist_user_projection: Projection
):
    results = StreamArticleRank(
        graph_connection, artist_user_projection, RankConfiguration()
    ).run()
    assert results


def test_write_articlerank(
    graph_connection: Connection, artist_user_projection: Projection
):
    results = WriteArticleRank(
        graph_connection,
        artist_user_projection,
        RankConfiguration(write_property="test_2"),
    ).run()
    assert results
    RemoveProperty(graph_connection, "test_2").run()
