from configclasses import configclass


@configclass
class Neo4j:
    host: str
    port: str
    scheme: str
    password: str


@configclass
class AppConfig:
    neo4j: Neo4j
