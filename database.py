import sqlite3


class DatabaseConnection:
    def __init__(self, host: str):
        self.connection = None
        self.host = host

    def __enter__(self) -> sqlite3.Connection:
        self.connection = sqlite3.connect(self.host)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()


class Database:
    def __init__(self):
        with DatabaseConnection('scoreboard.db') as connection:
            cursor = connection.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS scoreboard (score INT)')

    def add_record(self, score):
        with DatabaseConnection('scoreboard.db') as connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO scoreboard VALUES (?)', (score,
                                                                 ))

    def get_top_five(self):
        with DatabaseConnection('scoreboard.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM scoreboard ORDER BY score DESC LIMIT 5")
            top_ten = cursor.fetchall()
        return top_ten
