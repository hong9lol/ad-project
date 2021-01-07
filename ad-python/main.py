import datetime
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

chromeDriverPath = "/usr/bin/chromedriver"
key_words_list = list()
output = dict()


def crawling(title):
    num_of_categories = 11
    cid_value = 50000000
    browser = webdriver.Chrome(chromeDriverPath)

    # Get key words
    for i in range(num_of_categories):
        browser.get("https://datalab.naver.com/shoppingInsight/sCategory.naver?cid=" + str(cid_value))
        delay = 5
        try:
            WebDriverWait(browser, delay).until(lambda x: x.find_element_by_class_name("rank_top1000_num"))
        except TimeoutException:
            print("Loading took too much time!")
            continue

        top1000 = browser.find_element_by_class_name("rank_top1000_list").text
        top1000_list = str(top1000).split("\n")[1::2]
        top1000_list.insert(0, str(cid_value))
        key_words_list.append(top1000_list)
        cid_value += 1

    cid_value = 50000000
    # Rank key words
    for key_words in key_words_list:
        for idx, word in enumerate(key_words):
            if idx == 0:
                continue

            browser.get(
                "https://datalab.naver.com/shoppingInsight/sKeyword.naver?keyword=" + word + "&cid=" + str(cid_value))
            delay = 5
            try:
                WebDriverWait(browser, delay).until(lambda x: x.find_element_by_class_name("bb-circle"))
            except TimeoutException:
                print("Loading took too much time!")
                continue

            cy_list = list()
            cys = browser.find_elements_by_class_name("bb-circle")
            for cy in cys:
                cy_list.append(cy.get_attribute("cy"))

            _sum = 0
            for _idx in range(len(cy_list) - 7, len(cy_list)):
                _sum += float(cy_list[_idx])

            output[word] = _sum
        cid_value += 1

    ret = sorted(output.items(), key=(lambda x: x[1]))
    print(dict(ret))
    f = open("../data.txt"+title, 'w')
    f.write(str(dict(ret)))
    f.close()


if __name__ == '__main__':
    while True:
        now = datetime.datetime.now()
        if now.hour == 9 and now.minute == 0:
            crawling(str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2))
            time.sleep(60)
