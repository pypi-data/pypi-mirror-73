import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Dict, Optional

from py2neo import Graph


class Connection(ABC):
    def execute(self, query: str) -> Any:
        raise NotImplementedError


@dataclass(frozen=True)
class GraphConnection(Connection):
    graph: Graph

    @classmethod
    def to_neo4j(
        cls,
        uri: Optional[str] = None,
        name: Optional[str] = None,
        **settings: Dict[str, Any],
    ):
        return cls(Graph(uri, name, **settings))

    def execute(self, query: str) -> List[Dict[str, Any]]:
        return self.graph.run(query).data()


@dataclass(frozen=True)
class Query:
    connection: Connection

    @property
    @abstractmethod
    def cypher(self) -> str:
        raise NotImplementedError

    def run(self, log: bool = True) -> Any:
        if log:
            logging.info(f"Running query:\n {self.cypher}")
        return self.connection.execute(self.cypher)
