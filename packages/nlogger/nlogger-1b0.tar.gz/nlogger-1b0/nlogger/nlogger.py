import requests

class NLogger:
    def __init__(self):
        self.data = {}
        self.url = "https://us-central1-nlogger-microple.cloudfunctions.net/NLogger"

    def user_id(self, email):
        if email is not None:
            self.data["username"] = email
        else:
            f"user_id not initialized-{email} or it is None"

    def project_key(self, api_key):
        if api_key is not None:
            self.data['APIKey'] = api_key
        else:
            f"api_key not initialized-{api_key} or it is None"

    def send_message(self, message):
        self.data['message'] = message
        if message is not None and self.data['username'] and self.data['APIKey'] is not None:
            response = requests.post(self.url, data=self.data)
            return response.content
        else:
            f"api_key or userid is not initialized."
