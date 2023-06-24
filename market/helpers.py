from flask import session


def clear_session(string_array):
    for value in string_array:
        if value in session:
            del session[value]


def check_if_question_exists(user_score, question_id):
    for stat in user_score:
        if stat['question'] == question_id:
            print("Question exists")
            return True
    return False
