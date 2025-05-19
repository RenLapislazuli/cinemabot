import typing as tp
import sqlite3

con = sqlite3.connect("./dbs.db")
cur = con.cursor()

async def insert(user_name: str, message_text: str, res_kinopoisk_id: int, film_name: str) -> None:
    global cur
    cur.execute(f"""
        INSERT INTO History (UserName, QueryText, KinopoiskId, FilmName)
        VALUES ("{user_name}", "{message_text}", {res_kinopoisk_id}, "{film_name}");
    """)
    con.commit()

async def get_user_history(user_name: str) -> list[tp.Any]:
    global cur
    res = cur.execute(f"""
        SELECT * FROM History
        WHERE UserName="{user_name}"
    """)
    return res.fetchall()


def print_all():
    global cur
    res = cur.execute("""
        SELECT * FROM History
    """)
    print(res.fetchall())
