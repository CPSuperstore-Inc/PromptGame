import sqlite3

STARTING_ID = 1


def dict_factory(cursor, row):
    i = {}
    for idx, col in enumerate(cursor.description):
        i[col[0]] = row[idx]
    return i


def get_table_id(table, col_name="id"):
    c.execute("SELECT MAX({}) + 1 FROM {}".format(col_name, table))
    i = c.fetchone()[0]
    if i is None:
        return STARTING_ID
    return i


conn = sqlite3.connect("PromptGame/databases/database.db", check_same_thread=False)
c = conn.cursor()
conn.row_factory = dict_factory
d = conn.cursor()
