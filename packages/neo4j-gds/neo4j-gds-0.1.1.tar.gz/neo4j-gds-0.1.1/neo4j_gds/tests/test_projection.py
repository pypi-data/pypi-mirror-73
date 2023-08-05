from neo4j_gds.projection import Projection


def test_check_projection(artist_user_projection: Projection):
    if artist_user_projection.exists():
        artist_user_projection.delete()
    artist_user_projection.create()
    assert artist_user_projection.exists()
