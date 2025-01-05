from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from urllib.parse import quote
import os
import json

def send_messages(driver):
    with open ("./checked_users_list.txt") as f:
        lines = f.readlines()
        users = [line.strip() for line in lines]
    for user in users:
        driver.get(f"https://x.com/{user}")
        time.sleep(2)
        sm_button = element_exists(driver, By.XPATH, f"//button[@aria-label='Message']")
        if sm_button:
            sm_button.click()
            time.sleep(2)
            input_button = element_exists(driver, By.XPATH, f"//div[@data-testid='dmComposerTextInput_label']") 
            if input_button:
                actions = ActionChains(driver)
                actions.move_to_element(input_button).click().send_keys(f"Hola {user}, cómo estás? Este mensaje esta hecho con un scraper por Tato. Te escribimos porque encontramos una propuesta muy interesante para ti..."+ Keys.ENTER).perform()
                
                time.sleep(5)
                continue
        print(f"ERROR en el usuario {user}")
    return

def get_users(busquedas, username, password):
    if not os.path.exists('./backups'):
        os.makedirs('./backups')    
    final_list = []
    for busqueda in busquedas:
        scrl_post, scrl_comment, url = busqueda[0], busqueda[1], busqueda[2]
        driver = login(username, password)
        driver.get(url)
        time.sleep(3)
        temp_list = get_data(driver, url[23:28], scrl_post, scrl_comment)
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
    return driver

def get_data(driver, busqueda, scrl_post, scrl_comment):
    if not os.path.exists(f'./backups/{busqueda}'):
        os.makedirs(f'./backups/{busqueda}')
    users_list = []
    driver, posts_url = scroll_down_get(driver, iter=scrl_post)
    posts_url = list(set(posts_url))
    print(f"POST URLS:{len(posts_url)}, {posts_url}")
    for index, post_url in enumerate(posts_url):
        users_list.extend([post_url.split("/")[3]])
        driver.get(post_url)
        time.sleep(5)
        driver, comment_urls = scroll_down_get(driver=driver, iter=scrl_comment)
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
    for _ in range(iter):
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
    """with open ("./busquedas.txt") as f:
            lines = f.readlines()
            busquedas = [line for line in lines]
        for busqueda in busquedas:
            if len(busqueda)>1:
                url = "https://x.com/search?q=" + urllib.parse.quote(busqueda) + "&src=typed_query&f=live"
                urls.append(url) """
    return urls

def filter_users(driver):
        checked_users = []
        with open ("./users_list.txt") as f:
            lines = f.readlines()
            users = [line.strip() for line in lines]
        for index, user in enumerate(users):
            driver.get(f"https://x.com/{user}")
            time.sleep(2)
            followers_count_raw = element_exists(driver, By.XPATH, f"//a[@href='/{user}/verified_followers']")
            if followers_count_raw:
                followers_count = followers_count_raw.text
                if("M" in followers_count):
                    print(f"USER: {user} no pasó los requisitos")
                    continue
                if("K" in followers_count):
                    if int(followers_count.split(" ")[0].split(".")[0].strip("K"))<35:
                        checked_users.append(user)
                    else:
                        print(f"USER: {user} no pasó los requisitos")
                else:
                    int(followers_count.replace(" Followers", "").replace(",","").strip()) > 5
                    checked_users.append(user)
            else: 
                print(f"USER: {user} no pasó los requisitos")
                continue
            if index%20==0:
                print(checked_users)
        with open(f"./checked_users_list.txt", "w") as f:
            for user in checked_users:
                f.write(f"{user}\n") 
        return

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

def load_config(filepath="config.json"):
    with open(filepath, "r") as f:
        config_file = json.load(f)
    
    username = config_file["username"]
    password = config_file["password"]
    busquedas = [
        [
            b["scroll_posts"],
            b["scroll_comments"],
            f"https://x.com/search?q={quote(b['query'])}&src=typed_query&f=live"
        ]
        for b in config_file["busquedas"]
    ]

    return username, password, busquedas