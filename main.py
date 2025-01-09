from funcs import get_users,send_messages, filter_users, load_config, login
from urllib.parse import quote
import time

if __name__=="__main__":
    mail, username, password, busquedas = load_config()
    #print(busquedas)
    #driver = get_users(busquedas, mail, username, password)
    driver = login(mail, username, password)
    filter_users(driver, mail, username, password)
    #send_messages(driver)
    