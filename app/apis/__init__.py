from app.apis.RestfulApis import *


def register_apis(app: Flask):
    LoginApi.register_api(app)
    LogoutApi.register_api(app)

