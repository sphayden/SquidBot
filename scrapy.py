import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import json
def get_valid_coupons(valid_codes):
    try: 
        print('getting valid codes')
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.set_headless()
        driver = webdriver.Firefox(firefox_options=fireFoxOptions)
        #driver = webdriver.Firefox()
        driver.get('https://swq.jp/l/en-US/')
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        coupon_table = soup.find('tbody', id="coupons")
        for coupon in coupon_table.find_all('tr'):
            code_reward = []
            reward_amount = []
            row = coupon.find('i')
            if row['title'] == 'Verified':
                code_reward = []
                code_coupon = coupon.find("a")
                code_coupon = code_coupon['href']
                for i, image in enumerate(coupon.find_all("img")):
                    item_reward = image["src"].split("/")[3].split(".")[0]
                    amounts = coupon.find_all("span", class_='qty')
                    reward_amount = amounts[i].text.strip()
                    code_reward.append([item_reward, reward_amount])
                valid_codes.append({"Coupon_code": code_coupon, "Code_rewards": code_reward})
    except Exception as e:
        return f"Failed due to {e}"
    finally:
        driver.quit()


def get_expired_coupons(valid_codes):
    try: 
        driver = webdriver.Firefox()
        driver.get('https://swq.jp/l/en-US/')
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        coupon_table = soup.find('tbody', id="coupons")
        for coupon in coupon_table.find_all('tr'):
            row = coupon.find('i')
            code_name = coupon.find("td")
            if row['title'] == 'Expired':
                code_reward = []
                #reward_amount = []
                for i, image in enumerate(coupon.find_all("img")):
                    item_reward = image["src"].split("/")[3].split(".")[0]
                    amounts = coupon.find_all("span", class_='qty')
                    reward_amount = amounts[i].text.strip()
                    code_reward.append([item_reward, reward_amount])
                valid_codes.append({"Coupon_code": code_name.get_text(), "Code_rewards": code_reward})
                #print(f"{code_name.get_text()} -- {code_reward} -- {reward_amount}")
    except Exception as e:
        return f"Failed due to {e}"
    finally:
        driver.quit()

def main():
    valid_codes = []
    print("entered main functions")
    get_valid_coupons(valid_codes)
    print(f"Valid coupon code object {valid_codes}")
    return valid_codes
    

if __name__ == "__main__": 
    main()
else: 
    print ("Executed when imported")


