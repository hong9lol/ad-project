import ast
import datetime
import json
import time

from PIL import Image
from flask import Flask, render_template, request
from selenium import webdriver

from crawling import n_crawling, c_crawling
from utils import read

app = Flask(__name__)


@app.route('/foo', methods=['POST'])
def show_contents():
    ret = list()
    contents = request.data.decode('utf-8')
    contents = ast.literal_eval(contents)
    for idx, content in enumerate(contents):
        ids = str(content).split("-")
        print(ids)
        browser = webdriver.Chrome()
        browser.get("https://www.coupang.com/vp/products/" + ids[0] + "?itemId=" + ids[1])
        # WebDriverWait(browser, 1)
        browser.fullscreen_window()
        browser.save_screenshot("./screenshot.png")

        _t = str(browser.title).split("| ")
        if len(_t) < 2:
            continue
        title = _t[1]

        img = Image.open("./screenshot.png")
        area = (520, 190, 1450, 620)
        cropped_img = img.crop(area)
        cropped_img.save("./static/images/screenshot" + str(idx) + ".png")
        print(title)
        ret.append({"title": title, "link": "https://www.coupang.com/vp/products/" + ids[0] + "?itemId=" + ids[1]})

        browser.close()
    return json.dumps(ret)


@app.route('/')
def home():
    return render_template("index.html", key_word_list=read())


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    # app.run(debug=True)

    while True:
        now = datetime.datetime.now()
        if now.hour == 18 and now.minute == 00:
            title = str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2)
            naver_ranked_keywords = n_crawling()
            c_crawling(naver_ranked_keywords)
            time.sleep(60)
