from core import *
import random, string
from functools import wraps
from flask import request, session, url_for
from datetime import datetime, timedelta

logindb = client.login

class LoginHandler():
    def registerLogin(self, logindata: dict) -> None:
        user_email = logindata['userinfo']['email']
        user = logindb.userinfo.find_one({'email': user_email}, {'_id': 0})
        current_time = datetime.utcnow().strftime(datetime_format)
        if not user:
            logindb.userinfo.insert_one({
                'name': logindata['userinfo']['name'],
                'username': logindata['userinfo']['nickname'],
                'nickname': logindata['userinfo']['nickname'],
                'picture': logindata['userinfo']['picture'],
                'phone': '',
                'email': user_email,
                'createdAt': current_time,
                'lastLogin': current_time,
            })
        new_token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(128))
        session['token'] = new_token
        session_entry = {
            'token': new_token,
            'email': user_email,
            'isLoggedIn': True,
            'userAgent': str(request.user_agent),
            'createdip': str(request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)),
            'lastip': str(request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)),
            'createdAt': current_time,
            'lastActive': current_time,
        }
        logindb.userinfo.update_one({'email': user_email}, {'$set': {'lastLogin': current_time}})
        logindb.sessions.insert_one(session_entry)

    def isLoggedin(self):
        if session.get('token'):
            session_entry = logindb.sessions.find_one({'token': session.get('token')}, {'_id': 0})
            if session_entry:
                if session_entry['isLoggedIn']:
                    lastlogintime = session_entry['lastActive']
                    if datetime.utcnow() < (datetime.strptime(lastlogintime, datetime_format) + timedelta(minutes=10)): # change it to days=5
                        return session_entry
                    raise LoginError(request.method, getredirecturl='/logout/')

    def verifyLogin(self, loginrequired: bool, passUserinfo: bool, urlstate: str) -> None:
        sessiondata = self.isLoggedin()
        current_time = datetime.utcnow().strftime(datetime_format)
        if sessiondata:
            if passUserinfo:
                logindb.sessions.update_one({'token': sessiondata['token']}, {'$set': {'lastActive': current_time, 'lastip': str(request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr))}})
                return logindb.userinfo.find_one({'email': sessiondata['email']}, {'_id': 0})
            return None
        session.clear()
        if loginrequired:
            lurl = url_for('login.login')
            lurl += ('&', '?')[urlparse(lurl).query == ''] + urlencode({'us': urlstate})
            raise LoginError(request.method, getredirecturl=lurl)
        
    def registerLogout(self) -> None:
        if session.get('token'):
            session_entry = logindb.sessions.find_one({'token': session.get('token')}, {'_id': 0})
            session.clear()
            if session_entry:
                if session_entry['isLoggedIn']:
                    logindb.sessions.delete_one({'token': session_entry['token']})
                    return
        raise LoginError(request.method, getredirecturl='/')
    
    def handleLogin(self, loginrequired: bool, passUserinfo: bool = True, urlstate: str = '/'):
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kw):
                userinfo = self.verifyLogin(loginrequired, passUserinfo, urlstate)
                return f(userinfo, *args, **kw)
            return wrapper
        return decorator

loginhandler = LoginHandler()
