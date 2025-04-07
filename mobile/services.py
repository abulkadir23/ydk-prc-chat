import requests
from kivy.storage.jsonstore import JsonStore
from kivy.network.urlrequest import UrlRequest
from kivy.logger import Logger

class APIService:
    def __init__(self):
        self.base_url = "http://localhost:8000/api"  # Django API URL'si
        self.store = JsonStore('user_data.json')
        self.token = None
        self._load_token()

    def _load_token(self):
        try:
            self.token = self.store.get('auth')['token']
        except:
            self.token = None

    def _save_token(self, token):
        self.store.put('auth', token=token)
        self.token = token

    def _get_headers(self):
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        return headers

    def login(self, username, password, on_success, on_error):
        url = f"{self.base_url}/auth/login/"
        data = {
            'username': username,
            'password': password
        }
        
        def on_success_callback(req, result):
            if 'token' in result:
                self._save_token(result['token'])
                on_success(result)
            else:
                on_error("Token alınamadı")

        def on_error_callback(req, error):
            Logger.error(f"Login error: {error}")
            on_error(str(error))

        UrlRequest(
            url,
            req_body=json.dumps(data),
            req_headers=self._get_headers(),
            on_success=on_success_callback,
            on_error=on_error_callback,
            on_failure=on_error_callback
        )

    def register(self, username, password, email, on_success, on_error):
        url = f"{self.base_url}/auth/register/"
        data = {
            'username': username,
            'password': password,
            'email': email
        }

        UrlRequest(
            url,
            req_body=json.dumps(data),
            req_headers=self._get_headers(),
            on_success=lambda req, result: on_success(result),
            on_error=lambda req, error: on_error(str(error))
        )

    def get_parts(self, on_success, on_error):
        url = f"{self.base_url}/parts/"

        UrlRequest(
            url,
            req_headers=self._get_headers(),
            on_success=lambda req, result: on_success(result),
            on_error=lambda req, error: on_error(str(error))
        )

    def get_part_details(self, part_id, on_success, on_error):
        url = f"{self.base_url}/parts/{part_id}/"

        UrlRequest(
            url,
            req_headers=self._get_headers(),
            on_success=lambda req, result: on_success(result),
            on_error=lambda req, error: on_error(str(error))
        )

    def create_order(self, part_id, quantity, address, on_success, on_error):
        url = f"{self.base_url}/orders/"
        data = {
            'part_id': part_id,
            'quantity': quantity,
            'address': address
        }

        UrlRequest(
            url,
            req_body=json.dumps(data),
            req_headers=self._get_headers(),
            on_success=lambda req, result: on_success(result),
            on_error=lambda req, error: on_error(str(error))
        )

    def send_chat_message(self, message, on_success, on_error):
        url = f"{self.base_url}/chatbot/message/"
        data = {
            'message': message
        }

        UrlRequest(
            url,
            req_body=json.dumps(data),
            req_headers=self._get_headers(),
            on_success=lambda req, result: on_success(result),
            on_error=lambda req, error: on_error(str(error))
        )

    def logout(self):
        self.token = None
        self.store.delete('auth') 