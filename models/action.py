from dataclasses import dataclass
from typing import Optional


@dataclass
class Action:

    flow_id: Optional[str]

    tipo: Optional[str]

    tipo_logico: Optional[str]

    tipo_componente: Optional[str]

    modo: Optional[str]

    tag: Optional[str]

    texto: Optional[str]

    valor: Optional[str]

    field: Optional[str]

    placeholder: Optional[str]

    id: Optional[str]

    name: Optional[str]

    clase: Optional[str]

    url: Optional[str]

    timestamp: Optional[str]

    container_tag: Optional[str]

    container_class: Optional[str]

    index: int = 0