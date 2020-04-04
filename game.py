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


def get_summary_data(game_id):
    d.execute('select round.id, game, round, prompt.category, prompt.text as "real", p.text as "fake", c.text from round join prompt on prompt.id=round.regularQuestion join prompt p on round.falseQuestion=p.id join category c on prompt.category=c.id where game={}'.format(game_id))
    rs = d.fetchall()
    for r in rs:
        d.execute("select player.id, player.name, player.alien, response.response as 'response' from response join player on player.id=response.player where round={} and player.alien=0".format(r["id"]))
        r["humans"] = d.fetchall()

        d.execute("select player.id, player.name, player.alien, response.response as 'response' from response join player on player.id=response.player where round={} and player.alien=1".format(r["id"]))
        r["aliens"] = d.fetchall()

    return rs

