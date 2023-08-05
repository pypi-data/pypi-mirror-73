from typing import Dict, Any


def build_match_clause(reference: str, label: str, filter: Dict[str, Any]):
    strings = [
        f'{key}: "{value}"' if isinstance(value, str) else f"{key}: {value}"
        for key, value in filter.items()
    ]
    filter_string = f"{{{', '.join(strings)}}}"
    return f"MATCH ({reference}: {label} {filter_string})\n"
