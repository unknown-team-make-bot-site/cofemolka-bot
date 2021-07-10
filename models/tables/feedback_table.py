from utils.databaseutils import DatabaseUtils


class FeedbackTable(object):
    TABLE_NAME = 'feedback'

    @staticmethod
    def create_table():
        return DatabaseUtils().create_table(FeedbackTable.TABLE_NAME, "id integer PRIMARY KEY, description text NOT NULL")
