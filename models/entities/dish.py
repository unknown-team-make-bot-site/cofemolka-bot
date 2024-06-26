from dataclasses import dataclass


@dataclass
class Dish:
    dish_name: str
    description: str
    type_id: int
    cost: int
    volume: int
    image: str

    @staticmethod
    def fromTuple(tuple: tuple):
        # get rid of id
        print(tuple)
        print(*tuple[1:])
        return Dish(*tuple[1:])
