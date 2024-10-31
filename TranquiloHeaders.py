import ast
import random
from urllib.parse import urlparse

user_agents_list=[
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.32.63',
    'Mozilla/5.0 (Linux; Android 11; moto e20 Build/RONS31.267-94-14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.70 Mobile Safari/537.31.75',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.30.88',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.332.43',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.7.72',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.3.6',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.31.54',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.1.03',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.1.03',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 OpenWave/93.4.3888.30.51',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.351.75'
]

def create_headers_file(url, underAttack=False, num_headers=2000, filename='./resources/headers.txt', cookies=None, agent=None):
    headers_list = []
    
    for _ in range(num_headers):
        headers_list.append(build_http_request(url=url, underAttack=underAttack, cookies=cookies, uAgent=agent))
            
            
    vezes = len(headers_list)
    
    with open(filename, 'w') as file:
        for h in headers_list:
            if vezes > 1:
                file.write(str(h) + "\n")
            else:
                file.write(str(h)) 
            vezes -= 1

def build_http_request(url, underAttack=False, cookies=None, uAgent=None, seed=None):
    
    if ((cookies==None or uAgent==None) and underAttack == True):
        return "Erro - Modo Sob Ataque ativo porem sem Cookie ou User-Agent - TranquiloCrawler.build_http_request()"
    
    if seed is not None:
        random.seed(seed)

    # Extraindo o host da URL
    host = extract_host(url)
    # Gerando linha de requisição
    request_line = f"GET / HTTP/1.1\r\n"
    
    # Gerando cabeçalhos essenciais
    if underAttack:
        headers = f"Host: {host}\r\n"
        headers += "Cookie: " + str(cookies) + "\r\n"
        headers += "User-Agent:" + str(uAgent) + "\r\n"
        headers += f"Referer: {generate_referer(url)}\r\n"
        headers += "Cache-Control: no-cache\r\n"
        headers += "Connection: keep-alive\r\n"
    else:
        headers = f"Host: {host}\r\n"
        headers += f"User-Agent: {random_user_agent()}\r\n"  # Certifique-se de que random_user_agent funcione corretamente
        headers += f"Referer: {generate_referer(url)}\r\n"
        headers += "Cache-Control: no-cache\r\n"
        headers += "Connection: keep-alive\r\n"
    
    # Adicionando cabeçalhos opcionais aleatoriamente
    addHeaders = random_extra_header()
    
    if addHeaders is not None:
        headers += addHeaders
    
    header_final = request_line + headers + "\r\n"
    return str.encode(header_final)


def carrega_Headers(url, num_headers=2000, underAttack=False, filename='./resources/headers.txt', cookie=None, agent=None):
    create_headers_file(url=url, underAttack=underAttack, num_headers=num_headers, filename=filename, cookies=cookie, agent=agent)
    with open(filename, 'r') as file:  # Abrindo o arquivo em modo texto
        hlist = file.read().split('\n')  # Dividindo as linhas como strings
    
    # Convertendo as strings para objetos binários (bytes) com ast.literal_eval
    hlist = [ast.literal_eval(line) for line in hlist if line.strip()]  # Ignora linhas vazias
    return hlist

def extract_host(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def random_extra_header():
    headers = ""
    if random.choice([True, False]):
        headers += f"X-Forwarded-For: {random_x_forwarded_for()}\r\n"
    if random.choice([True, False]):
        headers += f"DNT: {random_dnt()}\r\n"
    if headers != "":
        return headers
    else:
        return None


def pick_random_header(filename='./resources/headers.txt'):
    with open(filename, 'r') as file:
        headers = file.read().splitlines()
    return random.choice(headers)


def random_x_forwarded_for():
    num_ips = random.randint(1, 4)
    ips = [ ".".join(str(random.randint(0, 255)) for _ in range(4)) for _ in range(num_ips) ]
    return ", ".join(ips)


def random_dnt():
    return "1" if random.choice([True, False]) else "0"


def generate_referer(url):
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme or "http"
    return f"{scheme}://{parsed_url.netloc}/"


def random_user_agent():
    return random.choice(user_agents_list)