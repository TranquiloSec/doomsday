import os
from sys import stdout
import requests

def get_proxies(pasta='./resources'):
    if not os.path.exists(f"{pasta}/proxy.txt"):
        stdout.write(f" Sem Proxies em {pasta}/proxy.txt\n")
        if not os.path.isdir(pasta):
            os.mkdir(pasta)
        downloadProxys()
    
    proxies = open(f"{pasta}/proxy.txt", 'r').read().split('\n')
    return proxies

def count_proxies(pasta='./resources'):
    try:
        proxies = sum(1 for line in open(f"{pasta}/proxy.txt", 'r'))
        return proxies
    except Exception as Error:
        return Error
                            
def downloadProxys(pasta='./resources'):
    try:
        with open(f'{pasta}/proxy.txt', 'w') as f:
            pass
        
        stdout.write(" Download de Proxies Iniciado\n")
        for site in proxy_resources:
            pegar_proxies(site)
            
        pr = count_proxies()
        stdout.write(" Proxies Baixados: " + f"{pr}\n")
        
    except Exception as Error:
        
        stdout.write(".proxies command Error " + f" [{Error}] \n")

def pegar_proxies(site):
    try:
        data = requests.get(site)
        text_for_parse = data.text
        res = text_for_parse.split()
        with open('./resources/proxy.txt', 'a') as proxy_file:
            proxy_file.writelines('\n'.join(res))
        return True
    except Exception as Error:
        return Error

def usar_fonte(arquivo):
    if os.path.exists(arquivo):
        proxy_resources = []
        with open(arquivo, 'r') as proxy_source:
            for line in proxy_source:
                proxy_resources.append(line)
    else:
        print(" Arquivo Não Encontrado - Usando Proxies Padrão")


def definir_proxies(userList=None, custom_list=False, arquivo='./resources/proxy.txt'):
    if custom_list:
        if os.path.exists(userList):
            proxies = []
            with open(userList, 'r') as origem:
                conteudo = origem.read()
            
            with open(arquivo, 'w') as destino:
                destino.write(conteudo)
                
            proxies = open(arquivo, 'r').read().split('\n')
            #proxies = open('./resources/usuarioDefiniuListaCustom', 'w')
            print(' Lista de Proxies do Usuário Carregada com Sucesso')
        else:
            print(" Erro - Lista De Proxy do Usuario Não Encontrada - Usando Lista Anterior")
            proxies = get_proxies()
            
        return proxies
    
    else:
        if os.path.exists('./resources/usuarioDefiniuListaCustom'):
            os.remove('./resources/usuarioDefiniuListaCustom')
            deletar_lista()
        proxies = get_proxies()
        return proxies



def deletar_lista(arquivo='./resources/proxy.txt'):
    if os.path.exists(arquivo):
        os.remove(arquivo)

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