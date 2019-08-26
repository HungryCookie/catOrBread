import config
from SQLiter import SQLiter


class Main:

    response = ""

    def __init__(self, user_id, answer):
        # print(user_id)
        # print(answer)
        self.user_id = user_id
        self.answer = answer

        if answer.lower() == '/start':
            self.start()
        else:
            self.dialog()

    def get_response(self):
        return self.response

    def start(self):
        db = SQLiter(config.DATABASE_NAME)
        if not db.check_user(self.user_id):
            db.set_new_user(self.user_id)
        else:
            db.set_user_state(self.user_id, 0)
        db.close()
        self.response = config.WELCOME_MESSAGE

    def dialog(self):
        db = SQLiter(config.DATABASE_NAME)
        if self.answer.lower() in config.NEGATIVE_STATEMENTS:
            if db.get_user_state(self.user_id) == 0:  # The tutorial is completed TODO statistics
                db.set_user_state(self.user_id, -1)
                self.response = config.NOT_BREAD_MESSAGE

            elif db.get_user_state(self.user_id) == 1:
                db.set_user_state(self.user_id, -1)
                self.response = config.NOT_CAT_MESSAGE

        elif self.answer.lower() in config.POSITIVE_STATEMENTS:
            if db.get_user_state(self.user_id) == 0:
                db.set_user_state(self.user_id, 1)
                self.response = config.MAYBE_CAT_BREAD_MESSAGE

            elif db.get_user_state(self.user_id) == 1:
                db.set_user_state(self.user_id, -1)
                self.response = config.NOT_BREAD_MESSAGE
        db.close()



#
# a = Main(3, 'yes')
# a.start()
