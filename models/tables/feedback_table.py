from models.entities.feedback import Feedback
from utils.database_utils import DatabaseUtils

TABLE_NAME = 'feedback'
class FeedbackTable(object):

    @staticmethod
    def create_table():
        return DatabaseUtils().create_table(TABLE_NAME, "id integer PRIMARY KEY, feedback_text text NOT NULL")

    @staticmethod
    def get_feedbacks():
        return [Feedback.fromTuple(tupl) for tupl in DatabaseUtils().get(TABLE_NAME)]

    @staticmethod
    def add_feedback(text):
        col_list = ['feedback_text']
        values = text
        return DatabaseUtils().add(TABLE_NAME, col_list, values)

    @staticmethod
    def delete_all():
        return DatabaseUtils().delete_all(TABLE_NAME)
