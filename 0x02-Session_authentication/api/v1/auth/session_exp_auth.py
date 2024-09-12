from os import getenv
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth

class SessionExpAuth(SessionAuth):
    """ a class SessionExpAuth that inherits from SessionAuth """
    def __init__(self):
        """Initialize session duration from environment variable."""
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session with expiration time."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dict = {
                "user_id": user_id,
                "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_data
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user_id from session, checking if it's expired."""
        if not session_id or session_id not in self.user_id_by_session_id:
            return None

        session_data = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_data.get("user_id")

        if "created_at" not in session_data:
            return None

        created_at = session_data["created_at"]
        if created_at + timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return session_data.get("user_id")
