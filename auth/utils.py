from core import *
import random, string
from functools import wraps
from flask import request, session

class LoginTracker():
    registered_identifiers = []
    maxidentifiers = 1000
    def registerLogin(self) -> None:
        newidentifier = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(32))
        session.get('user')['login_identifier'] = newidentifier
        self.registered_identifiers.append(newidentifier)
        if len(self.registered_identifiers) > self.maxidentifiers:
            self.registered_identifiers.pop(0)

    def verifyLogin(self) -> None:
        if session.get('user'):
            if session.get('user').get('login_identifier'):
                identifier = session.get('user').get('login_identifier')
                if identifier in self.registered_identifiers:
                    return
        session.clear()
        raise LoginError(request.method)
        
    def registerLogout(self) -> None:
        self.verifyLogin()
        identifier = session.get('user').get('login_identifier')
        self.registered_identifiers.remove(identifier)
        session.clear()

login_tracker = LoginTracker()

def requireLogin(f):
    @wraps(f)
    def wrapper(*args, **kw):
        # login_tracker.verifyLogin()
        if not session.get('user'):
            session.clear()
        return f(*args, **kw)
    return wrapper