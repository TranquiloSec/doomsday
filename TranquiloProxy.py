import os
from sys import stdout
import requests

def get_proxies(pasta='./resources'):
    """
    Returns the list of proxies from the 'proxy.txt' file in the specified folder.
    If the file does not exist, creates the folder (if it doesn't exist) and downloads proxies.
    
    Parameters:
    - pasta (str): path of the folder where the proxy file should be.
    
    Returns:
    - list: list of proxies read from proxy.txt.
    """
    if not os.path.exists(f"{pasta}/proxy.txt"):
        stdout.write(f" No Proxies in {pasta}/proxy.txt\n")
        if not os.path.isdir(pasta):
            # Creates the folder if it doesn't exist
            os.mkdir(pasta)
        # Downloads the proxies if the file does not exist
        downloadProxys()
    
    # Reads the content of proxy.txt and splits by lines
    proxies = open(f"{pasta}/proxy.txt", 'r').read().split('\n')
    return proxies

def count_proxies(pasta='./resources'):
    """
    Counts how many proxies are in the 'proxy.txt' file.
    
    Parameters:
    - pasta (str): path of the folder containing the proxy.txt file.
    
    Returns:
    - int or Exception: number of lines (proxies) or error object if failed.
    """
    try:
        proxies = sum(1 for line in open(f"{pasta}/proxy.txt", 'r'))
        return proxies
    except Exception as Error:
        return Error
                            
def downloadProxys(pasta='./resources'):
    """
    Downloads proxies from various sources listed in proxy_resources.
    Creates/cleans the 'proxy.txt' file before adding new proxies.
    Finally, reports how many proxies were obtained.
    """
    try:
        # Creates/cleans the proxy.txt file
        with open(f'{pasta}/proxy.txt', 'w') as f:
            pass
        
        stdout.write(" Proxy Download Started\n")
        # For each URL in proxy_resources, calls pegar_proxies()
        for site in proxy_resources:
            pegar_proxies(site)
            
        pr = count_proxies()
        stdout.write(" Proxies Downloaded: " + f"{pr}\n")
        
    except Exception as Error:
        stdout.write(".proxies command Error " + f" [{Error}] \n")

def pegar_proxies(site):
    """
    Makes a GET request to the provided site and obtains the list of proxies.
    Writes these proxies to the proxy.txt file.
    
    Parameters:
    - site (str): URL that provides the list of proxies.
    
    Returns:
    - bool or Exception: True if successful, or error if failed.
    """
    try:
        data = requests.get(site)
        text_for_parse = data.text
        res = text_for_parse.split()  # Splits the text into lines
        with open('./resources/proxy.txt', 'a') as proxy_file:
            proxy_file.writelines('\n'.join(res))
        return True
    except Exception as Error:
        return Error

def usar_fonte(arquivo):
    """
    Loads proxy source URLs from a specific file.
    If the file does not exist, uses the default sources (defined in proxy_resources).
    
    Parameters:
    - arquivo (str): path of the proxy sources file.
    """
    if os.path.exists(arquivo):
        proxy_resources = []
        with open(arquivo, 'r') as proxy_source:
            for line in proxy_source:
                proxy_resources.append(line)
    else:
        print(" File Not Found - Using Default Proxies")


def definir_proxies(userList=None, custom_list=False, arquivo='./resources/proxy.txt'):
    """
    Defines the list of proxies to be used.
    If custom_list is True, it tries to load the user's list.
    If the user's list does not exist, continues with the previous list.
    If custom_list is False, uses the default list.
    
    Parameters:
    - userList (str): path to the user's proxy file.
    - custom_list (bool): if True, uses the user's custom list.
    - arquivo (str): path to the main proxy file (default is ./resources/proxy.txt).
    
    Returns:
    - list: list of proxies to be used.
    """
    if custom_list:
        if os.path.exists(userList):
            # Loads the content of the user's file and overwrites proxy.txt
            proxies = []
            with open(userList, 'r') as origem:
                conteudo = origem.read()
            
            with open(arquivo, 'w') as destino:
                destino.write(conteudo)
                
            proxies = open(arquivo, 'r').read().split('\n')
            print(' User Proxy List Loaded Successfully')
        else:
            print(" Error - User Proxy List Not Found - Using Previous List")
            proxies = get_proxies()
            
        return proxies
    
    else:
        # If a custom list has been previously defined, removes it
        if os.path.exists('./resources/usuarioDefiniuListaCustom'):
            os.remove('./resources/usuarioDefiniuListaCustom')
            deletar_lista()
        proxies = get_proxies()
        return proxies


def deletar_lista(arquivo='./resources/proxy.txt'):
    """
    Removes the specified proxy file, if it exists.
    
    Parameters:
    - arquivo (str): path of the proxy file to be deleted.
    """
    if os.path.exists(arquivo):
        os.remove(arquivo)

# Global list of pre-defined proxy sources.       
proxy_resources = [
    'https://www.proxy-list.download/api/v1/get?type=socks4',
    'https://www.proxyscan.io/download?type=socks4',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt',
    'https://api.openproxylist.xyz/socks4.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt',
    'https://www.freeproxychecker.com/result/socks4_proxies.txt',
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all&simplified=true',
    'https://www.proxy-list.download/api/v1/get?type=socks5',
    'https://www.proxyscan.io/download?type=socks5',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
    'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt',
    'https://api.openproxylist.xyz/socks5.txt',
    'https://www.freeproxychecker.com/result/socks5_proxies.txt',
    'https://api.proxyscrape.com/?request=displayproxies&proxytype=http',
    'https://www.proxy-list.download/api/v1/get?type=http',
    'https://www.proxyscan.io/download?type=http',
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt',
    'https://api.openproxylist.xyz/http.txt',
    'https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt',
    'http://alexa.lr2b.com/proxylist.txt',
    'http://rootjazz.com/proxies/proxies.txt',
    'https://www.freeproxychecker.com/result/http_proxies.txt',
    'http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt',
    'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
    'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
    'https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt',
    'https://proxy-spider.com/api/proxies.example.txt',
    'https://multiproxy.org/txt_all/proxy.txt',
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
    'https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/http.txt',
    'https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/https.txt',
    'https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&country=all'
]
