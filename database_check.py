from models.entities.feedback import Feedback
from models.tables.feedback_table import FeedbackTable
from models.tables.menu_table import MenuTable
from models.tables.type_dish_table import TypeDish
from utils import database_utils
import psycopg2 as psql

def connect():
        print("Connection to postgresql database...")
        conn = psql.connect("dbname = dishes user=postgres password=baguvix")
        cur = conn.cursor()
        print('Postgresql database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

        cur.close()

connect()
# MenuTable.delete_all()

