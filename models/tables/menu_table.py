from models.entities.dish import Dish
from models.tables.feedback_table import FeedbackTable
from utils.database_utils import DatabaseUtils

TABLE_NAME = 'menu'
class MenuTable(object):

    @staticmethod
    def create_table():
        cols_str = """
        id integer PRIMARY KEY, name text NOT NULL, description text, type text, cost integer, volume integer"""
        return DatabaseUtils().create_table(TABLE_NAME, cols_str)

    @staticmethod
    def get_dishes():
        return [Dish.fromTuple(tupl) for tupl in DatabaseUtils().get(TABLE_NAME)]
