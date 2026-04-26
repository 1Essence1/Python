import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def connect():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def setup_database():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def get_or_create_player(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING;",
        (username,)
    )
    cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
    player_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()
    return player_id


def save_result(username, score, level_reached):
    player_id = get_or_create_player(username)

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (%s, %s, %s);
        """,
        (player_id, score, level_reached)
    )

    conn.commit()
    cur.close()
    conn.close()


def get_top_scores(limit=10):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT p.username, gs.score, gs.level_reached,
               TO_CHAR(gs.played_at, 'YYYY-MM-DD HH24:MI') AS played_at
        FROM game_sessions gs
        JOIN players p ON p.id = gs.player_id
        ORDER BY gs.score DESC, gs.level_reached DESC, gs.played_at ASC
        LIMIT %s;
        """,
        (limit,)
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_personal_best(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COALESCE(MAX(gs.score), 0)
        FROM game_sessions gs
        JOIN players p ON p.id = gs.player_id
        WHERE p.username = %s;
        """,
        (username,)
    )

    best = cur.fetchone()[0]
    cur.close()
    conn.close()
    return best
