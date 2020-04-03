from PromptGame.database import conn, c, d, get_table_id
from PromptGame import category
import random


def get_category_questions(cid=None):
    if cid is None:
        cid = random.choice(category.get_categories())["id"]
    d.execute("SELECT * FROM prompt WHERE category={}".format(cid))
    return d.fetchall()


def get_question_pair(cid=None):
    q = get_category_questions(cid)
    random.shuffle(q)
    return q[0], q[1]



def get_question(qid):
    d.execute("SELECT * FROM prompt WHERE id={}".format(qid))
    return d.fetchone()
