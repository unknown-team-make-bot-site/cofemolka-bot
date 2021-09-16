from models.entities.dish import Dish
from models.tables.feedback_table import FeedbackTable
from utils.database_utils import DatabaseUtils

TABLE_NAME = 'menu'
class MenuTable(object):

    @staticmethod
    def create_table():
        cols_str = """id integer PRIMARY KEY AUTOINCREMENT,  
        name text NOT NULL, 
        description text, 
        type text, 
        cost integer, 
        volume integer"""
        return DatabaseUtils().create_table(TABLE_NAME, cols_str)

    @staticmethod
    def get_dishes():
        return [Dish.fromTuple(tupl) for tupl in DatabaseUtils().get(TABLE_NAME)]

    @staticmethod
    def add_dishes(name, cost, type, volume=0, description="nothing"):
        col_list = ['name', 'description', 'type', 'cost', 'volume']
        values = [f'{name}', f'{description}', f'{type}', cost, volume]
        return DatabaseUtils().add(TABLE_NAME, col_list, values)

    @staticmethod
    def delete_all():
        DatabaseUtils().delete_all(TABLE_NAME)

    @staticmethod
    def delete_table():
        DatabaseUtils().delete_table(TABLE_NAME)
