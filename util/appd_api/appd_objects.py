import marshmallow
from marshmallow_dataclass import dataclass


# ignore unknown properties
class SchemaBase(marshmallow.Schema):
    class Meta:
        unknown = getattr(marshmallow, "EXCLUDE", None)


@dataclass(base_schema=SchemaBase)
class Application:
    name: str
    id: int
