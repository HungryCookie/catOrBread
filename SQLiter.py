import sqlite3


class SQLiter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        with self.connection:
            self.cursor.execute("""create table if not exists user_state (
                                    user_id	INTEGER NOT NULL,
                                    state	INTEGER NOT NULL DEFAULT 0,
                                    finished_times	INTEGER NOT NULL DEFAULT 0,
                                    PRIMARY KEY(user_id)
                                )""")
            self.cursor.execute("""create table if not exists log_info (
                                    message_time DATE DEFAULT (datetime('now', 'localtime')),
                                    user_id	INTEGER NOT NULL,
                                    answer TEXT NOT NULL,
                                    prev_state INTEGER
                                )""")

    def get_user_info(self, user_id):
        with self.connection:
            return self.cursor.execute('select * from user_state where user_id = ?', (user_id,)).fetchall()[0]

    def set_new_user(self, user_id):
        with self.connection:
            self.cursor.execute('insert into user_state (user_id, state) values (?, ?)', (user_id, 0))

    def increment_user_state(self, user_id):
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

    def set_finished_times(self, user_id, finished_times):
        with self.connection:
            self.cursor.execute('update user_state set finished_times = ? where user_id = ?', (finished_times, user_id))

    def get_finished_times(self, user_id):
        with self.connection:
            return self.cursor.execute('select finished_times from user_state where user_id = ?', (user_id,)).fetchone()[0]

    def write_log(self, user_id, answer, previous_state):
        with self.connection:
            return self.cursor.execute('insert into log_info (user_id, answer, prev_state) '
                                       'values (?, ?, ?)', (user_id, answer, previous_state))

    def get_user_logs(self, user_id):
        with self.connection:
            return self.cursor.execute('select * from log_info where user_id = ?', (user_id,)).fetchall()[0]

    def close(self):
        self.connection.close()
