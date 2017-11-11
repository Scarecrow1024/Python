from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.taobao.com/")
#assert "Python" in driver.title
elem = driver.find_element_by_xpath('//*[@id="q"]')
#elems = driver.find_elements_by_css_selector('.service-bd li')
#print(elems)
#for e in elems:
#    print(e.get_attribute('data-groupid'))
elem.send_keys("小米6")
btn = driver.find_element_by_class_name('btn-search')
print(btn)
btn.click()
#elem.send_keys(Keys.RETURN)
#print(driver.page_source)
#driver.close()
