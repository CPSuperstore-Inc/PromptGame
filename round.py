from PromptGame.database import conn, c, d, get_table_id

import PromptGame.question as question


def get_round(rid, game):
    d.execute("SELECT * FROM round WHERE round={} AND game={}".format(rid, game))
    rs = d.fetchone()
    if rs is None:
        return new_round(rid, game)
    return rs


def new_round(rid, game):
    p = question.get_question_pair()
    c.execute("INSERT INTO round (game, round, regularQuestion, falseQuestion) VALUES ({}, {}, {}, {})".format(
        game, rid, p[0]["id"], p[1]["id"]
    ))
    conn.commit()
    return get_round_id(c.lastrowid)


def get_round_id(rid):
    d.execute("SELECT * FROM round WHERE id={}".format(rid))
    return d.fetchone()


def get_responses(rid):
    d.execute("select * from response join player on player.id=response.player where round={}".format(rid))
    return d.fetchall()
