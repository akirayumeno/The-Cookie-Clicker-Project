from selenium import webdriver
from selenium.webdriver.common.by import By
import time

ChromeOptions = webdriver.ChromeOptions()
ChromeOptions.add_experimental_option('detach', True)

driver = webdriver.Chrome()
driver.get("https://orteil.dashnet.org/experiments/cookie/")

#get money amount
money = int(driver.find_element(By.CSS_SELECTOR, "#money").text)
#get cookie to click on
cookie = driver.find_element(By.CSS_SELECTOR, "#cookie")

#get upgrade item ids
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5 # 5s from now
five_min = time.time() + 60 * 5

while True:
    cookie.click()
    # Every 5 seconds:
    if time.time() > timeout:
        #get all upgrade <b> tags
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        #Convert <b> text into an integer price
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = element_text.split("-")[1].strip().replace(",", "")
                item_prices.append(int(cost))

        # Create dictionary of store items and price
        cookie_upgrade = {}
        for n in range(len(item_prices)):
            cookie_upgrade[item_ids[n]] = item_prices[n]

        # Get current cookie count
        money_element = driver.find_element(By.CSS_SELECTOR, "#money").text
        if "," in money_element:
            money_element = money_element.replace(",","")
        cookie_amount = int(money_element)

        # Find upgrades that we can currently afford
        afford_upgrades = {}
        for item_id,item_price in cookie_upgrade.items():
            if cookie_amount > item_price:
                afford_upgrades[item_price] = item_id

        #  Purchase the most expensive affordable upgrade
        highest_upgrade = max(afford_upgrades)
        to_purchase_id = afford_upgrades[highest_upgrade]
        driver.find_element(By.ID, to_purchase_id).click()

        # Add another 5 seconds until the next check
        timeout = time.time() + 5
    if time.time() > five_min:
        cps = driver.find_element(By.CSS_SELECTOR, "#cps").text
        print(cps)
        break

driver.quit()