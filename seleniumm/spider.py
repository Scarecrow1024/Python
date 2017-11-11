import re
import math
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import gevent
from gevent import monkey

monkey.patch_all()

browser = webdriver.PhantomJS(service_args=['--load-images=false', '--disk-cache=true'])
browser.set_window_size(1366,768)
wait = WebDriverWait(browser, 10)
def search():
    browser.get('https://www.taobao.com')
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))
        )
        input.send_keys('美食')
        #input.send_keys(Keys.ENTER )
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
        )
        parse_page()
        return total
    except TimeoutError:
        #browser.quit()
        #pass
        return search()

def next_page(page_num):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"))
        )
        input.clear()
        input.send_keys(page_num)
        #input.send_keys(Keys.ENTER )
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > li.item.active > span"), str(page_num))
        )
        parse_page()
    except TimeoutError:
        next_page(page_num)

def parse_page():
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-itemlist .items .item"))
    )
    html = browser.page_source
    doc = pq(html)
    items = doc.find('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'title':item.find('.title').text(),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text(),
            'shop':item.find('.shop').text()
        }
        print(product)

def main():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total.text).group(1))
        #print(total)
        l = []
        for page in range(2, total+1):
            l.append(gevent.spawn(next_page, page))
            #next_page(page)
        gevent.joinall(l)
    except Exception as e:
        print(e)
    finally:
        browser.close()

if __name__ == "__main__":
    main()
