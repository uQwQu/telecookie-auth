import pickle
from datetime import datetime

import pytz
import redis
from django.contrib.auth import get_user_model

User = get_user_model()
redis_client = redis.StrictRedis(host="redis", port=6379, db=0)


def get_sessions_data(profile):
    user_pkid = profile.user.pkid
    sessions_data = []

    session_keys = redis_client.scan_iter(match=":1:django.contrib.sessions.cache*")
    for session_key in session_keys:
        try:
            session_data = redis_client.get(session_key)
            session = pickle.loads(session_data)

            if session.get("_auth_user_id") == str(user_pkid):
                session_key = session_key.decode("utf-8")
                session_id = session_key.split("cache")[-1].strip()

                creation_time = session.get("_creation_time")
                creation_datetime = datetime.fromtimestamp(
                    creation_time, tz=pytz.utc
                )
                sessions_data.append((session, session_id, creation_datetime))
        except Exception as e:
            print(f"Error processing session {session_key}: {e}")

    return sessions_data


def get_user_from_session(session_id):
    session_data = redis_client.get(f":1:django.contrib.sessions.cache{session_id}")
    if session_data:
        session = pickle.loads(session_data)
        auth_user_id = session.get("_auth_user_id")
        if auth_user_id:
            return User.objects.filter(pkid=auth_user_id).first()


def get_active_sessions(profile):
    active_sessions = [session_id for _, session_id, _ in get_sessions_data(profile)]
    return active_sessions
