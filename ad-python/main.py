import ast
import datetime
import json
import time
import threading
from subprocess import call

from PIL import Image
from flask import Flask, render_template, request
from selenium import webdriver

from crawling import n_crawling, c_crawling
from utils import read, TimeMaker

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["CACHE_TYPE"] = "null"

pwd = '1'
cmd = 'ls'


@app.route('/foo', methods=['POST'])
def show_contents():
    ret = list()
    contents = request.data.decode('utf-8')
    contents = ast.literal_eval(contents)
    idx = 0
    for content in contents:
        ids = str(content).split("-")
        print(ids)
        browser = webdriver.Chrome()
        browser.get("https://www.coupang.com/vp/products/" + ids[0] + "?itemId=" + ids[1])
        # WebDriverWait(browser, 1)
        browser.fullscreen_window()
        browser.save_screenshot("./screenshot.png")

        _t = str(browser.title).split("| ")
        if len(_t) < 2:
            browser.close()
            continue
        title = _t[1]

        img = Image.open("./screenshot.png")
        area = (520, 190, 1450, 620)
        cropped_img = img.crop(area)
        cropped_img.save("./static/images/screenshot" + str(idx) + ".png")
        call('echo {} | sudo -S {}'.format(pwd,
                                           "cp ./static/images/screenshot" + str(
                                               idx) + ".png" + " /var/www/html/resource/screenshot" + str(ids[1]) + ".png"),
             shell=True)
        print(title)
        ret.append({"title": title, "link": "https://www.coupang.com/vp/products/" + ids[0] + "?itemId=" + ids[1]})
        idx += 1
        browser.close()
    return json.dumps(ret)


@app.route('/')
def home():
    return render_template("index.html", key_word_list=read())


def crawling(h, m):
    print("Start crawling")
    while True:
        now = datetime.datetime.now()
        if now.hour == h and now.minute == m:
            naver_ranked_keywords = n_crawling()
            c_crawling(naver_ranked_keywords)
        time.sleep(60)


if __name__ == '__main__':
    threading.Thread(target=crawling, args=(0, 0)).start()
    app.run(host="0.0.0.0", debug=False)
    # app.run(debug=True)
