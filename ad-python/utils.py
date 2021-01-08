import datetime
import json

title = ""


def save(_data):
    f = open("../data" + title + ".txt", 'w')
    f.write(str(_data))
    f.close()


def read():
    global title
    if title == "":
        now = datetime.datetime.now()
        title = str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2)
    f = open("../data" + title + ".txt", 'r')
    _data = f.read()
    f.close()
    return json.loads(_data.replace("'", "\""))
