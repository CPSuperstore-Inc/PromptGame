from PromptGame.database import conn, c, d, get_table_id


def set_response(rid, player, text):
    text = text.replace('"', "'")
    c.execute("INSERT INTO response (round, player, response) VALUES ({}, {}, \"{}\")".format(
        rid, player, text
    ))
    conn.commit()