import typing
from dataclasses import is_dataclass, dataclass


class CreateFromDictMixin:
    @classmethod
    def is_list_of_dataclass(cls, field_type) -> bool:
        if typing.get_origin(field_type) is list:
            element_type = typing.get_args(field_type)[0]
            return is_dataclass(element_type)
        return False

    @classmethod
    def get_field_type(cls, field_type) -> typing.Optional[type]:
        if typing.get_origin(field_type) is list:
            element_type = typing.get_args(field_type)[0]
            return element_type
        return None

    @classmethod
    def create(cls, data: dict):
        dataclass_fields = cls.__dataclass_fields__
        processed_data = dict()

        for name, field in dataclass_fields.items():
            if not field.init:
                continue

            value = data.get(name)
            if isinstance(value, dict) and is_dataclass(field.type) and hasattr(field.type, 'create'):
                value = field.type.create(value)

            if isinstance(value, list) and cls.is_list_of_dataclass(field.type):
                field_type = cls.get_field_type(field.type)
                if hasattr(field_type, 'create'):
                    value = [field_type.create(element) for element in value]

            processed_data[name] = value

        return cls(**processed_data)


@dataclass
class RuleSet(CreateFromDictMixin):
    """
    Ref https://docs.battlesnake.com/api/objects/ruleset
    """
    name: str
    version: str


@dataclass
class GameObject(CreateFromDictMixin):
    """
    Ref https://docs.battlesnake.com/api/objects/game
    """
    id: str
    ruleset: RuleSet
    map: str
    timeout: int
    source: str

@dataclass
class PositionObject(CreateFromDictMixin):
    """
    Ref https://docs.battlesnake.com/api/objects/position
    """
    x: int
    y: int

@dataclass
class SnakeObject(CreateFromDictMixin):
    """
    Ref https://docs.battlesnake.com/api/objects/snake
    """
    id: str
    name: str
    health: int
    body: typing.List[PositionObject]
    head: PositionObject
    length: int
    shout: str
    squad: str

@dataclass
class BoardObject(CreateFromDictMixin):
    """
    Ref https://docs.battlesnake.com/api/objects/board
    """
    height: int
    width: int
    food: typing.List[PositionObject]
    hazards: typing.List[PositionObject]
    snakes: typing.List[SnakeObject]

@dataclass
class MoveRequestObject(CreateFromDictMixin):
    game: GameObject
    turn: int
    board: BoardObject
    you: SnakeObject