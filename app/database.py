import sqlite3
from datetime import datetime

db = sqlite3.connect('fer.db')
cur = db.cursor()


async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS users ("
                "id integer primary key autoincrement, "
                "user_id integer)")

    cur.execute("CREATE TABLE IF NOT EXISTS user_history ("
                "id integer primary key autoincrement,"
                "user_id integer,"
                "emotion text,"
                "date text)")

    db.commit()


async def cmd_start_db(user_id: int):
    user = cur.execute(f"SELECT * FROM users WHERE user_id == {user_id}").fetchone()
    if not user:
        cur.execute(f"INSERT INTO users (user_id) VALUES ({user_id})")
        db.commit()


async def extend_emotion(user_id: int, emotion_type: str):
    date_time = str(datetime.now())[:-7]
    cur.execute(f"INSERT INTO user_history (user_id, emotion, date) "
                f"VALUES ({user_id}, '{emotion_type}', '{date_time}')")
    db.commit()


async def emotion_history(user_id: int, date_range: str = '5 year'):
    emotion = cur.execute(f"SELECT emotion, COUNT(emotion) AS emotion_count FROM user_history "
                          f"WHERE user_id == {user_id} and DATE(date) >= DATE('now', '-{date_range}') "
                          f"GROUP BY emotion "
                          f"ORDER BY emotion").fetchall()

    return emotion
