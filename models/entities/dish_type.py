class DishType:
    name: str

    @staticmethod
    def fromTuple(tuple: tuple):
        return DishType(*tuple[1:])
