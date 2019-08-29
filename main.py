import const
import datetime


class Main:

    response = ""

    def __init__(self, user_id, answer, database):

        self.user_id = user_id
        self.answer = answer
        self.db = database
        self.logging()
        if answer.lower() == '/start':
            self.start()
        else:
            self.dialog()

    def get_response(self):
        return self.response

    def start(self):
        if not self.check_user():
            self.db.set_new_user(self.user_id)

        else:
            self.db.set_user_state(self.user_id, 0)

        self.response = const.WELCOME_MESSAGE

    def check_user(self):
        return self.db.check_user(self.user_id)

    """
    State 0 - /start initialization
    State 1 - positive answer track
    State -1 - end of the track   
    """
    def dialog(self):
        if self.check_user():
            if self.answer.lower() in const.NEGATIVE_STATEMENTS:
                if self.db.get_user_state(self.user_id) == 0:
                    self.db.set_user_state(self.user_id, -1)
                    self.response = const.NOT_BREAD_MESSAGE
                    self.increase()

                elif self.db.get_user_state(self.user_id) == 1:
                    self.db.set_user_state(self.user_id, -1)
                    self.response = const.NOT_CAT_MESSAGE
                    self.increase()

                elif self.db.get_user_state(self.user_id) == -1:
                    self.response = const.END_GAME_MESSAGE

                else:
                    self.response = const.HELP_MESSAGE

            elif self.answer.lower() in const.POSITIVE_STATEMENTS:
                if self.db.get_user_state(self.user_id) == 0:
                    self.db.set_user_state(self.user_id, 1)
                    self.response = const.MAYBE_CAT_BREAD_MESSAGE

                elif self.db.get_user_state(self.user_id) == 1:
                    self.db.set_user_state(self.user_id, -1)
                    self.response = const.NOT_BREAD_MESSAGE
                    self.increase()

                elif self.db.get_user_state(self.user_id) == -1:
                    self.response = const.END_GAME_MESSAGE

                else:
                    self.response = const.HELP_MESSAGE

            else:
                self.response = const.INAPPROPRIATE_MESSAGE

        else:
            self.response = const.HELP_MESSAGE

    """
    Accumulating info about user's overall walkthrough's
    """
    def increase(self):
        finished_times = self.db.get_finished_times(self.user_id) + 1
        self.db.set_finished_times(self.user_id, finished_times)

    """
    Tracking all operations users do
    """
    def logging(self):
        if self.check_user():
            previous_state = self.db.get_user_state(self.user_id)

        else:
            previous_state = None
        self.db.write_log(self.user_id, self.answer, previous_state)