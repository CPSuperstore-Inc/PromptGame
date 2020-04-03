from PromptGame.database import conn, c, d, get_table_id
from PromptGame import category
import random


def get_category_questions(cid=None):
    if cid is None:
        cid = random.choice(category.get_filled_categories())["id"]
    d.execute("SELECT * FROM prompt WHERE category={}".format(cid))
    return d.fetchall()


def get_question_pair(cid=None):
    q = get_category_questions(cid)
    random.shuffle(q)
    return q[0], q[1]



def get_question(qid):
    d.execute("SELECT * FROM prompt WHERE id={}".format(qid))
    return d.fetchone()


def add_question(cid, text):
    text = text.replace('"', "'")
    c.execute("INSERT INTO prompt (category, text) VALUES ({}, \"{}\")".format(cid, text))
    conn.commit()


def get_all_questions():
    d.execute("SELECT * FROM prompt")
    return d.fetchall()


def edit_question(qid, cat, text):
    text = text.replace('"', "'")

    c.execute("UPDATE prompt SET category={}, text=\"{}\" WHERE id={}".format(cat, text, qid))
    conn.commit()


def delete_question(qid):
    c.execute("DELETE FROM prompt WHERE id={}".format(qid))
    conn.commit()
