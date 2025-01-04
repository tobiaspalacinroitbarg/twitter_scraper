import pandas as pd
from funcs import login, scroll_down_get, get_url, filter_users
import time 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os

def scraper(urls):
    os.makedirs(f'./backups/busquedas')    
    final_list = []
    for index, url in enumerate(urls):
        driver = login("NftScpr","scrapperbot25")
        """ checked_users = filter_users(driver,["Alien_Designer","WokeCoinAda","Stellz84751083"])
        print(checked_users) """
        driver.get(url)
        time.sleep(5)
        temp_list = get_data(driver, url[23:28])
        temp_list = list(set(temp_list))
        final_list.extend(temp_list)
        with open(f"./backups/busquedas/busqueda_{url[23:28]}.txt", "w") as f: 
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

if __name__=="__main__":
    with open ("./busquedas.txt") as f:
        lines = f.readlines()
        busquedas = [line for line in lines]
    urls = get_url(busquedas)
    print(urls)
    scraper(urls)
