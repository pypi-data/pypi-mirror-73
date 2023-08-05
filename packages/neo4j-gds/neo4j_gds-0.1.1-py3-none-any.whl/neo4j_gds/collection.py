from dataclasses import dataclass
from typing import List, Tuple, Dict

from neo4j_gds.exceptions import ProjectionNotFound
from neo4j_gds.projection import TaggedProjection, Projection
from neo4j_gds.query import Connection


@dataclass(frozen=True)
class Collection:
    projections: List[TaggedProjection]

    @classmethod
    def create_from_projections_parameters(
        cls, connection: Connection, projections_parameters: Tuple[Dict[str, List[str]]]
    ):
        projections = [
            projection
            for projection_parameters in projections_parameters
            for projection in TaggedProjection.consolidate(
                connection, **projection_parameters
            )
        ]
        return Collection(projections)

    def get_projection_by_tag(self, tag: str) -> Projection:
        for projection in self.projections:
            if tag in projection.tags:
                return projection
        raise ProjectionNotFound(f"Projection with tag {tag} not found")

    def create(self, log: bool = True):
        for projection in self.projections:
            if not projection.exists(log):
                projection.create(log)
