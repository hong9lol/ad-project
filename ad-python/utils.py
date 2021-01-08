import json

title = "20210108"


def save(_data):
    f = open("../data" + title + ".txt", 'w')
    f.write(str(_data))
    f.close()


def read():
    f = open("../data" + title + ".txt", 'r')
    _data = f.read()
    f.close()
    return json.loads(_data.replace("'", "\""))

