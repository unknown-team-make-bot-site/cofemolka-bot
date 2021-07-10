from dataclasses import dataclass


@dataclass
class Dish:
    dish_name: str
    description: str

    @staticmethod
    def fromTuple(tuple: tuple):
        # get rid of id
        return Dish(*tuple[1:])
