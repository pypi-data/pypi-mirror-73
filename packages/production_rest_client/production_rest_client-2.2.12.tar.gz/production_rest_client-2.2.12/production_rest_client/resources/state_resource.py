# coding=utf-8
# pylint: disable=import-error, eval-used
from resources.models.helper import rest_get_call


class StateResource(object):

    def __init__(self, host, port, session, time_out):
        self.host = host
        self.port = port
        self.session = session
        self.time_out = time_out

    def get_state(self, type_="ALL"):
        url_ = "http://{0}:{1}/state/{2}".format(self.host, self.port, type_)
        result = rest_get_call(url_, self.session, self.time_out)
        if result["resource"]["data"] is not None and len(result["resource"]["data"]) > 3:
            result["resource"]["data"][3] = eval(result["resource"]["data"][3])
        return result["resource"]


