from models.entities.feedback import Feedback
from models.tables.feedback_table import FeedbackTable
from models.tables.menu_table import MenuTable
from models.tables.type_dish_table import TypeDish

MenuTable.delete_table()
MenuTable.create_table()
TypeDish.create_table()
# MenuTable.delete_all()

