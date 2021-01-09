import datetime
import json


class TimeMaker:
    title = ""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, data):
        self.title = ""
        cls = type(self)
        if not hasattr(cls, "_init"):
            self.data = data
            cls._init = True

    @classmethod
    def get_title(cls):
        if cls.title == "":
            cls.update_title()
        return cls.title

    @classmethod
    def update_title(cls):
        now = datetime.datetime.now()
        cls.title = str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2)

    @classmethod
    def update_and_get_title(cls):
        cls.update_title()
        return cls.get_title()


def save(_data):
    f = open("../data" + TimeMaker.update_and_get_title() + ".txt", 'w')
    f.write(str(_data))
    f.close()


def read():
    f = open("../data" + TimeMaker.get_title() + ".txt", 'r')
    _data = f.read()
    f.close()
    return json.loads(_data.replace("'", "\""))
