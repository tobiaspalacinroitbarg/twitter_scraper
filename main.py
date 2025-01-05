from funcs import get_urls, get_users,send_messages,login, filter_users, load_config
from urllib.parse import quote

if __name__=="__main__":
    username, password, busquedas = load_config()
    print(busquedas)
    #urls = get_urls()
    driver = get_users(busquedas, username, password)
    filter_users(driver)
    #send_messages(driver)
    