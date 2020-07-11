import dataclasses
import json
from typing import List

import marshmallow
from marshmallow_dataclass import dataclass


class SchemaBase(marshmallow.Schema):
    """Ignore unknown properties"""

    class Meta:
        unknown = getattr(marshmallow, "EXCLUDE", None)


def dataclass_to_json(clzz: dataclasses.dataclass):
    return json.dumps(dataclasses.asdict(clzz))


@dataclass(base_schema=SchemaBase)
class Application:
    name: str
    id: int


@dataclass(base_schema=SchemaBase)
class ServiceEndpointMatchConfig:
    """Used for call to get all existing SEP configs"""

    @dataclass(base_schema=SchemaBase)
    class DiscoveryConfig:
        @dataclass(base_schema=SchemaBase)
        class Property:
            id: int
            version: int
            name: str
            value: str

        namingSchemeType: str
        properties: List[Property]

    @dataclass(base_schema=SchemaBase)
    class AttachedEntity:
        id: int
        version: int
        entityType: str
        entityId: int

    id: int
    version: int
    name: str
    nameUnique: bool
    applicationComponentId: int
    enabled: bool
    discoveryConfig: DiscoveryConfig
    entryPointType: str
    entryPointTypeString: str
    attachedEntity: AttachedEntity
    agentType: str
