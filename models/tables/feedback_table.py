from models.entities.feedback import Feedback
from utils.database_utils import DatabaseUtils


class FeedbackTable(object):
    TABLE_NAME = 'feedback'

    @staticmethod
    def create_table():
        return DatabaseUtils().create_table(FeedbackTable.TABLE_NAME, "id integer PRIMARY KEY, feedback_text text NOT NULL")

    @staticmethod
    def get_feedbacks():
        return [Feedback.fromTuple(tupl) for tupl in DatabaseUtils().get(FeedbackTable.TABLE_NAME)]

    @staticmethod
    def add_feedback(feedback):
        col_list = ['feedback_text']
        values = f"'{feedback.feedback_text}'"
        return DatabaseUtils().add(FeedbackTable.TABLE_NAME, col_list, values)

    @staticmethod
    def delete_all():
        return DatabaseUtils().delete_all(FeedbackTable.TABLE_NAME)