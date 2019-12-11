from flask import Flask, jsonify
from app.response import fail_response, error_response


class InvalidUsage(Exception):
    def __init__(self, msg, data):
        Exception.__init__(self)
        self.msg = msg
        self.data = data

    def to_dict(self):
        return fail_response(self.msg, self.data)


def register_error_handlers(app: Flask):
    app.errorhandler(InvalidUsage)(handle_invalid_usage)
    app.errorhandler(404)(page_not_found)
    app.errorhandler(405)(not_allowed)
    app.errorhandler(500)(internal_error)


def handle_invalid_usage(error):
    return jsonify(error.to_dict()), 500


def page_not_found(error):
    return error_response("无效的请求"), 404


def not_allowed(error):
    return error_response("未授权的访问"), 405


def internal_error(error):
    return error_response("系统正在维护"), 500
