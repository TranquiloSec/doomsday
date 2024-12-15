import undetected_chromedriver as webdriver
import time

def get_cookie(url, user):
    """
    Retrieves the 'cf_clearance' cookie and the current browser User-Agent when accessing a URL.
    
    Parameters:
    - url (str): The target website's URL.
    - user (str): The User-Agent to be used by the browser.
    
    Returns:
    - (cookie, useragent): Returns the cookie in the format 'name=value' and the User-Agent.
    - (False, False): If the cookie is not found within 60 seconds.
    """
    
    pegou = True # Flag indicating whether the cookie has been obtained.
    options = webdriver.ChromeOptions() # Initializes Chrome options.
    
    # List of arguments to configure the browser to be less detectable and set language, etc.
    arguments = [
        '--no-sandbox', '--disable-setuid-sandbox', '--disable-infobars', '--disable-logging',
        '--disable-login-animations', '--disable-notifications', '--disable-gpu', '--lang=pt_br', 
        '--start-maxmized', f'--user-agent={user}'  # Sets the language and User-Agent.
    ]
    
    # Adds the configured arguments to the browser options.
    for argument in arguments:
        options.add_argument(argument)
    
    # Initializes the browser driver with the configured options.
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)  # Sets an implicit wait of 5 seconds for elements to load.
    
    # Accesses the specified URL.
    driver.get(url)
    
    # Tries to find the 'cf_clearance' cookie within a maximum time of 60 seconds.
    for _ in range(60):
        cookies = driver.get_cookies()  # Retrieves the page cookies.
        tryy = 0  # Index used to iterate through the cookies.
        
        # Iterates through the cookies to find 'cf_clearance'.
        for i in cookies:
            if i['name'] == 'cf_clearance':
                # When found, formats the cookie and retrieves the User-Agent.
                cookieJAR = driver.get_cookies()[tryy]
                # Execute JavaScript on browser to obtain real User-Agent.
                useragent = driver.execute_script("return navigator.userAgent")
                # Format the cookie ass 'nome=valor'
                cookie = f"{cookieJAR['name']}={cookieJAR['value']}"
                pegou = False
                driver.quit()  #closes browser when cookies found
                return cookie, useragent
            else:
                # If the current cookie is not the desired one, increment the index and continue.
                tryy += 1
                pass
        
        # If the cookie is not found, waits 1 second and tries again.
        if pegou:
            time.sleep(1)
    
    # If the cookie is not found after 60 attempts (60s), closes the browser and returns False.
    driver.quit()
    return False, False
