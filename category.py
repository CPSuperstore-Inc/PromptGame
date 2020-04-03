from PromptGame.database import conn, c, d, get_table_id



def get_categories():
    d.execute("SELECT * FROM category")
    return d.fetchall()
