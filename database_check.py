from models.entities.feedback import Feedback
from models.tables.feedback_table import FeedbackTable

FeedbackTable.create_table()
FeedbackTable.delete_all()
assert len(FeedbackTable.get_feedbacks()) == 0
f_txt = 'text!!!'
f1 = Feedback(f_txt)
row_id = FeedbackTable.add_feedback(f1)
print(row_id)
got_feedbacks = FeedbackTable.get_feedbacks()
print(got_feedbacks)
assert len(got_feedbacks) == 1
assert got_feedbacks[0].feedback_text == f_txt