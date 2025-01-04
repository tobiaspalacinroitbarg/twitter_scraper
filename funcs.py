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
import os

def send_messages():
    None

def get_users(urls, username, password):
    if not os.path.exists('./backups'):
        os.makedirs('./backups')    
    final_list = []
    for index, url in enumerate(urls):
        driver = login(username, password)
        driver.get(url)
        time.sleep(3)
        temp_list = get_data(driver, url[23:28])
        temp_list = list(set(temp_list))
        final_list.extend(temp_list)
        with open(f"./backups/{url[23:28]}/final_{url[23:28]}.txt", "w") as f: 
            for item in temp_list:
                f.write(f"{item}\n")
    concat_total = len(final_list)
    final_list = list(set(final_list))
    concat_unique = len(final_list)
    print(f"Total de usuarios: {concat_total}, Total de usuarios únicos: {concat_unique}")
    with open("./users_list.txt", "w") as f: 
        for item in final_list:
            f.write(f"{item}\n")  
    driver.quit()
    return

def get_data(driver, busqueda):
    if not os.path.exists(f'./backups/{busqueda}'):
        os.makedirs(f'./backups/{busqueda}')
    users_list = []
    driver, posts_url = scroll_down_get(driver, iter=5)
    posts_url = list(set(posts_url))
    print(f"POST URLS:{len(posts_url)}, {posts_url}")
    for index, post_url in enumerate(posts_url):
        users_list.extend([post_url.split("/")[3]])
        driver.get(post_url)
        time.sleep(5)
        driver, comment_urls = scroll_down_get(driver=driver, iter=2)
        time.sleep(5)
        print(f"COMMENT URLS:{len(comment_urls)}, {comment_urls}")
        users_list.extend([url.split("/")[3] for url in comment_urls])
        users_list = list(set(users_list))
        if index%10==0:
            with open(f"./backups/{busqueda}/backup_{index}.txt", "w") as f:
                for item in users_list:
                    f.write(f"{item}\n")  
    return users_list

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

def get_urls():
    urls= []
    with open ("./busquedas.txt") as f:
        lines = f.readlines()
        busquedas = [line for line in lines]
    for busqueda in busquedas:
        if len(busqueda)>1:
            url = "https://x.com/search?q=" + urllib.parse.quote(busqueda) + "&src=typed_query&f=live"
            urls.append(url)
    return urls

def filter_users(driver):
        checked_users = []
        with open ("./users_list.txt") as f:
            lines = f.readlines()
            users = [line.strip() for line in lines]
        for user in users:
            driver.get(f"https://x.com/{user}")
            time.sleep(2)
            followers_count_raw = element_exists(driver, By.XPATH, f"//a[@href='/{user}/verified_followers']")
            if followers_count_raw:
                followers_count = followers_count_raw.text
                if("M" in followers_count):
                    print(f"USER: {user} no pasó los requisitos")
                    continue
                if("K" in followers_count):
                    if int(followers_count.strip("K").split(".")[0])<35:
                        checked_users.append(user)
                    else:
                        print(f"USER: {user} no pasó los requisitos")
                else:
                    int(followers_count.replace(" Followers", "").replace(",","").strip()) > 5
                    checked_users.append(user)
            else: 
                print(f"USER: {user} no pasó los requisitos")
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