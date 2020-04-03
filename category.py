from PromptGame.database import conn, c, d, get_table_id



def get_categories():
    d.execute("SELECT * FROM category")
    return d.fetchall()


def get_filled_categories():
    d.execute("SELECT * FROM category WHERE (SELECT count(*) FROM prompt where category=category.id) >= 2")
    return d.fetchall()


def add_category(text):
    text = text.replace('"', "'")

    c.execute("INSERT INTO category (text) VALUES ('{}')".format(text))
    conn.commit()
