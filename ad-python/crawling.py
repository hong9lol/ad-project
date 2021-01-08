
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from utils import title, save

chromeDriverPath = "/usr/bin/chromedriver"
key_words_list = list()
key_words_dict = dict()
delay = 5

def n_crawling():
    num_of_categories = 11
    cid_value = 50000000
    browser = webdriver.Chrome(chromeDriverPath)

    # Get key words
    for i in range(num_of_categories):
        browser.get("https://datalab.naver.com/shoppingInsight/sCategory.naver?cid=" + str(cid_value))
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
        browser.close()
    cid_value = 50000000

    # Rank key words
    for key_words in key_words_list:
        for idx, word in enumerate(key_words):
            if idx == 0:
                continue

            browser.get(
                "https://datalab.naver.com/shoppingInsight/sKeyword.naver?keyword=" + word + "&cid=" + str(cid_value))
            try:
                WebDriverWait(browser, delay).until(lambda x: x.find_element_by_class_name("bb-circle"))
            except TimeoutException:
                print("Loading took too much time!")
                continue

            cy_list = list()
            cys = browser.find_elements_by_class_name("bb-circle")
            for cy in cys:
                cy_list.append(cy.get_attribute("cy"))

            # sum ratio for a week
            _sum = 0
            for _idx in range(len(cy_list) - 7, len(cy_list)):
                _sum += float(cy_list[_idx])

            key_words_dict[word] = _sum
            browser.close()
        cid_value += 1


    ret = sorted(key_words_dict.items(), key=(lambda x: x[1]))
    print("[쇼핑 트랜드 키워 분석드 정렬]")
    print(ret)
    return dict(ret)


def c_crawling(ranked_keywords):
    browser = webdriver.Chrome(chromeDriverPath)
    output = dict()
    for key in ranked_keywords:
        browser.get(
            "https://www.coupang.com/np/search?component=&q=" + key + "&channel=user")
        try:
            WebDriverWait(browser, delay).until(lambda x: x.find_element_by_class_name("search-product"))
        except TimeoutException:
            print("Loading took too much time!")
            continue

        cnt = 1
        product_id_list = list()
        products = browser.find_elements_by_class_name("search-product")
        for product in products:
            try:
                if product.find_element_by_class_name("no-" + str(cnt)) is not None:
                    product_id_list.append(product.get_attribute("id") + "-" + product.find_element_by_class_name(
                        "search-product-link").get_attribute("data-item-id"))
                    cnt += 1
            except:
                continue
        output[key] = product_id_list
        browser.close()

    print("[쿠팡 식별 아디디 정보]")
    print(output)
    save(output)
