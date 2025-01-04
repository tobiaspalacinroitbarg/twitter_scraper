from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import urllib.parse

def scroll_down_get(driver: webdriver, iter):
    posts_list = []
    count_error=0
    feed = element_exists(driver=driver, by=By.XPATH,ref='//div[@aria-label="Home timeline"]',time=20)
    for index in range(0,iter):
        try:
            feed.send_keys(Keys.PAGE_DOWN)
            feed.send_keys(Keys.PAGE_DOWN)
            feed.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            post_elements = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a')
            post_urls = [element.get_attribute("href") for element in post_elements]
            posts_list.extend(post_urls)
        except:
            count_error+=1
            print(f"Error en i = {count_error}")
            break
    return driver, posts_list

def element_exists(driver:webdriver, by:By, ref:str, time=4, refresh=False):
    ret = False
    try:    # Check si existen más opciones que las del inicio - hacer click en caso de existir
        ret = WebDriverWait(driver, time).until(EC.presence_of_element_located((by,ref)))
        if refresh == True:
            driver.refresh()
        try:
            ret = WebDriverWait(driver, time).until(EC.presence_of_element_located((by,ref)))
        except :
            pass
    except TimeoutException:
        pass
    return ret

def get_url(busquedas):
    urls= []
    for busqueda in busquedas:
        if len(busqueda)>1:
            url = "https://x.com/search?q=" + urllib.parse.quote(busqueda) + "&src=typed_query&f=live"
            urls.append(url)
    return urls

def filter_users(driver, users):
        checked_users = []
        for user in users:
            driver.get(f"https://x.com/{user}")
            time.sleep(2)
            followers_count_raw = element_exists(driver, By.XPATH, f"//a[@href=/{users}/verified_followers]")
            if followers_count:
                followers_count = followers_count_raw.text
            if("M" in followers_count):
                continue
            if("K" in followers_count):
                followers_k_int = int(followers_count.strip("K").split(".")[0])
                if followers_k_int<35:
                    checked_users.append(user)
                continue
            elif int(followers_count.replace(",","")) > 5:
                checked_users.append(user)
            else: 
                continue
        return checked_users

def login(username, password):
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://x.com/i/flow/login")
    we_email=element_exists(driver=driver,by=By.XPATH, ref='//input[@autocomplete="username"]',time=20)
    we_email.send_keys(username)
    we_email.send_keys(Keys.ENTER)

    we_password = element_exists(driver=driver, by=By.XPATH,ref='//input[@name="password"]',time=20)
    we_password.send_keys(password)
    we_password.send_keys(Keys.ENTER)
    
    time.sleep(5)
    return driver