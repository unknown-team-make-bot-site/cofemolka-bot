from models.entities.feedback import Feedback
from utils.databaseutils import DatabaseUtils


class FeedbackTable(object):
    TABLE_NAME = 'feedback'

    @staticmethod
    def create_table():
        return DatabaseUtils().create_table(FeedbackTable.TABLE_NAME, "id integer PRIMARY KEY, description text NOT NULL")

    @staticmethod
    def get_feedbacks():
        return [Feedback(tupl) for tupl in DatabaseUtils().get(FeedbackTable.TABLE_NAME)]
