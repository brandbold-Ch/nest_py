from typing import NamedTuple, Callable, Any, Dict


class RouteDefinition(NamedTuple):
    handler: Callable[..., Any]
    metadata: Dict[str, Any]
