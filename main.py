from funcs import get_urls, get_users,send_messages,login, filter_users 

USERNAME ="NftScpr"
PASSWORD = "scrapperbot25"

if __name__=="__main__":
    urls = get_urls()
    driver = get_users(urls, USERNAME, PASSWORD)
    filter_users(driver)
    #send_messages(driver)
    