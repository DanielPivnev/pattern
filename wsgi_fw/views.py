from wsgi_fw.constants import STUDENT, ADMIN
from wsgi_fw.observers import ViewObserver


class BaseView(ViewObserver):
    def __init__(self):
        self.request = None
        self.authorisation = None
        self.controller = None
        self.user_id = None

    def get_request(self):
        if self.request and self.request.method == 'POST':
            wsgi_input = self.request.environ['wsgi.input'].read(
                int(self.request.environ['CONTENT_LENGTH']))
            wsgi_input = wsgi_input.decode('utf-8')
            wsgi_input = wsgi_input.split('&')
            wsgi_input = [w_i.split('=') for w_i in wsgi_input]
            wsgi_dict = {}
            for k, v in wsgi_input:
                wsgi_dict[k] = v
            self.post(wsgi_dict)

    def get_user_id(self):
        return self.user_id

    def post(self, wsgi_dict):
        pass

    def update(self, state, u_id):
        self.authorisation = state
        self.user_id = u_id

    def set_controller(self, controller):
        self.controller = controller

    def auth(self, state, user):
        self.controller.auth(state, user.id)
        self.user_id = user.id

    def logout(self):
        self.controller.logout()

    def is_student(self):
        if self.is_auth():
            return True if self.authorisation.get_state() == STUDENT else False
        else:
            return False

    def is_admin(self):
        if self.is_auth():
           return True if self.authorisation.get_state() == ADMIN else False
        else:
            return False

    def is_auth(self):
        return True if self.authorisation else False
