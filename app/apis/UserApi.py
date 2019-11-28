from flask.views import MethodView


class ApiBase(MethodView):
    endpoint = __name__
    url = __name__
    pk: str = "id"
    pk_type: str = "int"


class UserApi(ApiBase):

    def get(self):
        pass

    def post(self):
        pass
