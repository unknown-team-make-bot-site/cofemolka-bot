from models.entities.dish import Dish
from models.tables.feedback_table import FeedbackTable
from utils.database_utils import DatabaseUtils


class MenuTable(object):
    TABLE_NAME = 'menu'

    @staticmethod
    def create_table():
        cols_str = """
        id integer PRIMARY KEY, name text NOT NULL, description text"""
        return DatabaseUtils().create_table(MenuTable.TABLE_NAME, cols_str)

    @staticmethod
    def get_dishes():
        return [Dish.fromTuple(tupl) for tupl in DatabaseUtils().get(MenuTable.TABLE_NAME)]
