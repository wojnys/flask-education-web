from flask import session


def clear_session(string_array):
    for value in string_array:
        if value in session:
            del session[value]
