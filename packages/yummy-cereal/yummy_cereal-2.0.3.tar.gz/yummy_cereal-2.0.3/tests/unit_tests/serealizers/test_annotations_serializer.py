from dataclasses import dataclass

from yummy_cereal import AnnotationsSerializer


@dataclass
class House:
    number: int
    street: str


@dataclass
class Person:
    name: str
    house: House


def test_AnnotationsSerializer() -> None:
    house_serializer = AnnotationsSerializer(House)
    person_serializer = AnnotationsSerializer(
        Person, specified_serializers={House: house_serializer}
    )

    house = House("1", "Sesame street")
    person = Person("Joel", house)
    serialized_person = person_serializer(person)

    assert serialized_person["name"] == "Joel"
    assert serialized_person["house"]["number"] == 1
    assert serialized_person["house"]["street"] == "Sesame street"
