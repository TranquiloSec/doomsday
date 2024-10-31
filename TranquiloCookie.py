import undetected_chromedriver as webdriver
import time

def get_cookie(url, user):
        pegou = True
        options = webdriver.ChromeOptions()
        arguments = [
            '--no-sandbox', '--disable-setuid-sandbox', '--disable-infobars', '--disable-logging',
            '--disable-login-animations',
            '--disable-notifications', '--disable-gpu', '--lang=pt_br', '--start-maxmized',
            f'--user-agent={user}'
        ]
        for argument in arguments:
            options.add_argument(argument)
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(5)
        driver.get(url)
        for _ in range(60):
            cookies = driver.get_cookies()
            tryy = 0
            for i in cookies:
                if i['name'] == 'cf_clearance':
                    cookieJAR = driver.get_cookies()[tryy]
                    useragent = driver.execute_script("return navigator.userAgent")
                    cookie = f"{cookieJAR['name']}={cookieJAR['value']}"
                    pegou = False
                    driver.quit()
                    return cookie, useragent
                else:
                    tryy += 1
                    pass
            if pegou:
                time.sleep(1)
        driver.quit()
        return False, False

# def testar():
    
#     user_agents_list=[
#     'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.32.63',
#     'Mozilla/5.0 (Linux; Android 11; moto e20 Build/RONS31.267-94-14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.70 Mobile Safari/537.31.75',
#     'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.30.88'
#     ]
    
#     user = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
#     print("")
#     print(" ---======---")
#     print(" " + str(user) + " ")
#     print(" ---======---")
#     print("")
#     url = 'https://www.tranquilosec.com.br/'
#     cokie, agent = get_cookie(url, user)

#     print('')
#     print('UserAgent-')
#     print(str(agent))
#     print('')
#     print('Cookie-')
#     print(str(cokie))
#     print('')