from funcs import get_urls, get_users,send_messages,login, filter_users 

USERNAME ="NftScpr"
PASSWORD = "scrapperbot25"

if __name__=="__main__":
    urls = get_urls()
    get_users(urls, USERNAME, PASSWORD)
    """
    PARA CORRER LÓGICA DE FILTROS SE TIENE QUE DESCOMENTAR ESTO Y COMENTAR LÍNEA 7 Y 8
    driver = login(USERNAME, PASSWORD)

    filter_users(driver)
    
    send_messages()
    """