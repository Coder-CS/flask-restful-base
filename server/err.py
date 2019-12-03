from server.response import fail_response


class InvalidUsage(Exception):
    def __init__(self, msg, data):
        Exception.__init__(self)
        self.msg = msg
        self.data = data

    def to_dict(self):
        return fail_response(self.msg, self.data)


