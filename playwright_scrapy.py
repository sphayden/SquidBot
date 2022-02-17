#import requests
import time
from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup
#rom selenium import webdriver
import json
async def get_valid_coupons(valid_codes):
    try: 
        print('getting valid codes')
        async with async_playwright() as p:
            browser = await p.firefox.launch()
            page = await browser.new_page()
            await page.goto("https://swq.jp/l/en-US/")
            await page.wait_for_timeout(5000)
            print(await page.content())
            #time.sleep(5)
            #page.
            html = await page.content()
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
            await browser.close()
    except Exception as e:
        return f"Failed due to {e}"
    finally:
        await browser.close()


async def get_expired_coupons(valid_codes):
    try: 
        print('getting valid codes')
        async with async_playwright() as p:
            browser = await p.firefox.launch()
            page = await browser.new_page()
            await page.goto("https://swq.jp/l/en-US/")
            await page.wait_for_timeout(5000)
            #print(await page.content())
            #time.sleep(5)
            #page.
            html = await page.content()
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
            await browser.close()
    except Exception as e:
        return f"Failed due to {e}"
    finally:
        await browser.close()


def main():
    valid_codes = []
    print("entered main functions")
    asyncio.run(get_valid_coupons(valid_codes))
    print(f"Valid coupon code object {valid_codes}")
    return valid_codes
    

if __name__ == "__main__": 
    main()
else: 
    print ("Executed when imported")