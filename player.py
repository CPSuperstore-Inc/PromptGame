from PromptGame.database import conn, c, d, get_table_id
import PromptGame.game as game
import random


def join_game(player_name:str, game_id):
    player_name = player_name.replace('"', "'")

    c.execute("INSERT INTO player (game, name) VALUES ('{}', \"{}\")".format(game_id, player_name))
    conn.commit()
    return c.lastrowid


def get_game_info(player_id):
    d.execute("select * from game where id=(select game from player where id={})".format(player_id))
    return d.fetchone()


def is_alien(pid):
    d.execute("SELECT alien FROM player WHERE id={}".format(pid))
    return d.fetchone()["alien"] == 1


def select_alien(g):
    m = game.get_members(g)
    if m[0]["alien"] is None:
        random.shuffle(m)
        set_alien_status(m[0]["id"], 1)
        for i in m[1:]:
            set_alien_status(i["id"], 0)


def set_alien_status(pid, status):
    c.execute("UPDATE player SET alien={} WHERE id={}".format(status, pid))
    conn.commit()
