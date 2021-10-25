from models.entities.feedback import Feedback
from utils.database_utils import DatabaseUtils

TABLE_NAME = 'feedback'
class FeedbackTable(object):

    @staticmethod
    def create_table():
        return DatabaseUtils().create_table(
            TABLE_NAME, "id integer PRIMARY KEY AUTOINCREMENT, "
                        "feedback_text text NOT NULL")

    @staticmethod
    def get_feedbacks():
        return [Feedback.fromTuple(tupl) for tupl in DatabaseUtils().get(TABLE_NAME)]

    @staticmethod
    def add_feedback(text):
        col_list = ['id', 'feedback_text']
        values = str(text)
        return DatabaseUtils().add_one_column(TABLE_NAME, col_list=col_list, values=values)

    @staticmethod
    def delete_all():
        return DatabaseUtils().delete_all(TABLE_NAME)
