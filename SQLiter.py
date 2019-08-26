import sqlite3
import config


class SQLiter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_user(self, user_id):
        with self.connection:
            return self.cursor.execute('select * from user_state where user_id = ?', (user_id,)).fetchall()[0]

    def set_new_user(self, user_id):
        with self.connection:
            self.cursor.execute('insert into user_state (user_id, state) values (?, ?)', (user_id, 0))

    def update_user_state(self, user_id):
        with self.connection:
            new_state = self.get_user_state(user_id) + 1
            self.cursor.execute('update user_state set state = ? where user_id = ?', (new_state, user_id))

    def get_user_state(self, user_id):
        with self.connection:
            return self.cursor.execute('select state from user_state where user_id = ?', (user_id,)).fetchone()[0]

    def set_user_state(self, user_id, new_state):
        with self.connection:
            self.cursor.execute('update user_state set state = ? where user_id = ?', (new_state, user_id))

    def check_user(self, user_id):
        with self.connection:
            self.cursor.execute('select user_id from user_state where user_id = ?', (user_id,))
            if self.cursor.fetchall():
                return True
        return False





    def close(self):
        self.connection.close()


# db = SQLiter(config.DATABASE_NAME)
# db.update_user_state(1)
# print(db.get_state(1))
# db.close()