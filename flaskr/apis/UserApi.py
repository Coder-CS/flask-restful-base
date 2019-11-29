from flaskr.apis import ApiBase


class UserApi(ApiBase):

    def get(self, id):
        print(id)
        if id is None:
            return "users"
        else:
            return "user"

    def post(self, id):
        return str(id)
