import random
import string
from PromptGame.database import conn, c, d, get_table_id


def get_game_code(length=5):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


def new_game():
    c.execute("INSERT INTO game (code) VALUES ('{}')".format(get_game_code()))
    conn.commit()
    return c.lastrowid


def get_members(game_id):
    d.execute("SELECT * FROM player WHERE game={}".format(game_id))
    return d.fetchall()


def get_game(game_id):
    d.execute("SELECT * FROM game WHERE code='{}'".format(game_id))
    return d.fetchone()


def remove_code(game_id):
    d.execute("UPDATE game SET code=NULL WHERE id={}".format(game_id))
    conn.commit()
