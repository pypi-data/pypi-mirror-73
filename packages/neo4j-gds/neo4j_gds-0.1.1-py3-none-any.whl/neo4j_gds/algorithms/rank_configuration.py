from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict

from neo4j_gds.algorithms.algorithm import AlgorithmConfiguration
from neo4j_gds.utils import build_match_clause


@dataclass(frozen=True)
class RankConfiguration(AlgorithmConfiguration):
    max_iterations: int = 20
    damping_factor: float = 0.80
    write_property: Optional[str] = None

    @property
    def match_lines(self):
        return ""

    @property
    def source_nodes(self) -> str:
        source_nodes = ""
        return f"[{source_nodes}]"

    def __str__(self):
        write_property_part = (
            f", writeProperty: '{self.write_property}'" if self.write_property else ""
        )
        return f"""{{
            maxIterations: {self.max_iterations},
            dampingFactor: {self.damping_factor}
            {write_property_part}
        }}"""


@dataclass(frozen=True)
class RankConfigurationWithFilter(RankConfiguration):
    filter_elements: Optional[List[Tuple[str, str, Dict[str, str]]]] = None

    @property
    def match_lines(self):
        return "".join(
            [
                build_match_clause(reference, label, filter)
                for reference, label, filter in self.filter_elements
            ]
        )

    @property
    def source_nodes_names(self) -> Optional[List[str]]:
        return [filter_element[0] for filter_element in self.filter_elements]

    @property
    def source_nodes(self) -> str:
        source_nodes = ", ".join(self.source_nodes_names)
        return f"[{source_nodes}]"

    def __str__(self):
        write_property_part = (
            f", writeProperty: '{self.write_property}'" if self.write_property else ""
        )

        return f"""{{
            maxIterations: {self.max_iterations},
            dampingFactor: {self.damping_factor},
            sourceNodes: {self.source_nodes}
            {write_property_part}
        }}"""
