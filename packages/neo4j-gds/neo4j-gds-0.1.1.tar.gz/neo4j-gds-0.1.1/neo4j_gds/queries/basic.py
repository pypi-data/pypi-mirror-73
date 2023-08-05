from dataclasses import dataclass

from neo4j_gds.query import Query


@dataclass(frozen=True)
class RemoveProperty(Query):
    name: str

    @property
    def cypher(self) -> str:
        return f"""MATCH (n)
        REMOVE n.{self.name}"""
