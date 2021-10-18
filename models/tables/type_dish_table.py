from models.entities.dish_type import DishType
from utils.database_utils import DatabaseUtils

TABLE_NAME = "type_dish"

class TypeDish(object):

    @staticmethod
    def create_table():
        columns = "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "name TEXT NOT NULL"
        return DatabaseUtils().create_table(TABLE_NAME, columns)

    @staticmethod
    def delete_table():
        return DatabaseUtils.delete_table(TABLE_NAME)

    @staticmethod
    def delete_all():
        return DatabaseUtils.delete_all(TABLE_NAME)

    @staticmethod
    def add_types(name):
        col_list = ['name']
        values = name
        return DatabaseUtils.add_one_column(TABLE_NAME, col_list, values)

    @staticmethod
    def get_types():
        return [DishType.fromTuple(tuple) for tuple in DatabaseUtils.get(TABLE_NAME)]
