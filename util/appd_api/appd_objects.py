import dataclasses
import json
from dataclasses import field
from typing import List

import marshmallow
from marshmallow import post_dump, fields
from marshmallow_dataclass import dataclass


# ignore unknown properties
class SchemaBase(marshmallow.Schema):
    class Meta:
        unknown = getattr(marshmallow, "EXCLUDE", None)


def dataclass_to_json(dataclass: dataclasses.dataclass):
    return json.dumps(dataclasses.asdict(dataclass))


@dataclass(base_schema=SchemaBase)
class Application:
    name: str
    id: int


"""Used for call to get all existing SEP configs"""
@dataclass(base_schema=SchemaBase)
class ServiceEndpointMatchConfig:
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
