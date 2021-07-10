from models.tables.feedback_table import FeedbackTable
from utils.databaseutils import DatabaseUtils


class MenuTable(object):
    TABLE_NAME = 'feedback'

    @staticmethod
    def create_table():
        cols_str = """
        id integer PRIMARY KEY, name text NOT NULL, description text"""
        return DatabaseUtils().create_table(FeedbackTable.TABLE_NAME, cols_str)

    @staticmethod
    def get_dishes():
        return [Feedback(tupl[1]) for tupl in DatabaseUtils().get(FeedbackTable.TABLE_NAME)]
