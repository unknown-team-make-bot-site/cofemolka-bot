from models.entities.dish import Dish
from models.tables.feedback_table import FeedbackTable
from utils.database_utils import DatabaseUtils

# for containing image in database we need to convert file into binary format
'''
example of binary data:
10 1010 0101 0010 1001 0101 0101
'''
def convertToBinaryData(filename):
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

TABLE_NAME = 'menu'
class MenuTable(object):

    @staticmethod
    def create_table():
        cols_str = """id integer PRIMARY KEY AUTOINCREMENT,  
        name text NOT NULL, 
        description text, 
        type_id integer, 
        cost integer, 
        volume integer,
        image text"""
        return DatabaseUtils().create_table(TABLE_NAME, cols_str)

    @staticmethod
    def get_dishes():
        return [Dish.fromTuple(dishes) for dishes in DatabaseUtils().get(TABLE_NAME)]

    @staticmethod
    def get_dishes_with_type(type):
        return [Dish.fromTuple(dishes_with_type) for dishes_with_type
                in DatabaseUtils().get_dishes_with_type(TABLE_NAME, type)]

    @staticmethod
    def get_count_dishes(type_id):
        column = "type_id"
        return DatabaseUtils().get_rows_count_with_param(TABLE_NAME,column, type_id)

    @staticmethod
    def add_dishes(name, cost, type_id, image, volume=0, description="nothing"):
        col_list = ['name', 'description', 'type_id', 'cost', 'volume', 'image']
        # image = convertToBinaryData(image)
        values = [f'{name}', f'{description}', f'{type_id}', cost, volume, image]
        return DatabaseUtils().add(TABLE_NAME, col_list, values)

    @staticmethod
    def delete_all():
        DatabaseUtils().delete_all(TABLE_NAME)

    @staticmethod
    def delete_table():
        DatabaseUtils().delete_table(TABLE_NAME)


# SELECT name FROM DISH_TYPE where id = (SELECT type_id from Dish where id = :type)
