import ast
import random
from urllib.parse import urlparse

# List of predefined user-agents to be randomly selected
user_agents_list = [
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
    """
    Generates a file containing a specified number (num_headers) of formatted HTTP requests.
    Each request is created by build_http_request and then saved to the file.
    
    Parameters:
    - url (str): Target host URL.
    - underAttack (bool): Indicates if the "under attack" mode is active (uses cookies and agent).
    - num_headers (int): Number of requests to generate.
    - filename (str): Output filename.
    - cookies (str): Cookies to use if underAttack is True.
    - agent (str): User-agent to use if underAttack is True.
    """
    headers_list = []
    
    # Generates each request by calling build_http_request
    for _ in range(num_headers):
        headers_list.append(build_http_request(url=url, underAttack=underAttack, cookies=cookies, uAgent=agent))
            
    vezes = len(headers_list)
    
    # Writes the requests to the file, each on a new line
    with open(filename, 'w') as file:
        for h in headers_list:
            if vezes > 1:
                file.write(str(h) + "\n")
            else:
                file.write(str(h))
            vezes -= 1

def build_http_request(url, underAttack=False, cookies=None, uAgent=None, seed=None):
    """
    Creates an HTTP request in byte format, including basic and optional headers.
    If underAttack is True, uses provided cookies and user-agent.
    Otherwise, selects a random user-agent.
    
    Parameters:
    - url (str): Target host URL.
    - underAttack (bool): Indicates use of cookies and specific agent.
    - cookies (str): Cookies to be used if underAttack=True.
    - uAgent (str): User-agent to be used if underAttack=True.
    - seed (int): Optional seed for random number generator.
    
    Returns:
    - bytes: The final HTTP request in byte representation.
    """
    if ((cookies is None or uAgent is None) and underAttack == True):
        return "Error - Attack mode active but no Cookie or User-Agent - TranquiloCrawler.build_http_request()"
    
    if seed is not None:
        random.seed(seed)

    # Extracts the host from the URL
    host = extract_host(url)
    # First line of the HTTP request
    request_line = f"GET / HTTP/1.1\r\n"
    
    # Required headers
    if underAttack:
        headers = f"Host: {host}\r\n"
        headers += "Cookie: " + str(cookies) + "\r\n"
        headers += "User-Agent:" + str(uAgent) + "\r\n"
        headers += f"Referer: {generate_referer(url)}\r\n"
        headers += "Cache-Control: no-cache\r\n"
        headers += "Connection: keep-alive\r\n"
    else:
        headers = f"Host: {host}\r\n"
        headers += f"User-Agent: {random_user_agent()}\r\n"
        headers += f"Referer: {generate_referer(url)}\r\n"
        headers += "Cache-Control: no-cache\r\n"
        headers += "Connection: keep-alive\r\n"
    
    # Adds optional headers randomly
    addHeaders = random_extra_header()
    if addHeaders is not None:
        headers += addHeaders
    
    # Joins the request line with the headers and finishes with \r\n
    header_final = request_line + headers + "\r\n"
    return str.encode(header_final)

def carrega_Headers(url, num_headers=2000, underAttack=False, filename='./resources/headers.txt', cookie=None, agent=None):
    """
    Generates the header file by calling create_headers_file and then loads these headers 
    into memory. Converts each line of the file into a byte object, ready for use.
    
    Parameters:
    - url (str): Target host URL.
    - num_headers (int): Number of requests to generate.
    - underAttack (bool): If True, uses provided cookies and agent.
    - filename (str): File where headers are saved.
    - cookie (str): Cookie for underAttack mode.
    - agent (str): User-agent for underAttack mode.
    
    Returns:
    - list: List of requests in bytes.
    """
    # First creates the header file
    create_headers_file(url=url, underAttack=underAttack, num_headers=num_headers, filename=filename, cookies=cookie, agent=agent)
    
    # Reads the file in text mode
    with open(filename, 'r') as file:
        hlist = file.read().split('\n')  # Each line is a string
    
    # Converts each line to bytes using ast.literal_eval
    hlist = [ast.literal_eval(line) for line in hlist if line.strip()]  # Ignores empty lines
    return hlist

def extract_host(url):
    """
    Extracts the host (domain) from the URL.
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc

def random_extra_header():
    """
    Randomly adds optional headers X-Forwarded-For and DNT.
    Might return None if no header is selected.
    """
    headers = ""
    if random.choice([True, False]):
        headers += f"X-Forwarded-For: {random_x_forwarded_for()}\r\n"
    if random.choice([True, False]):
        headers += f"DNT: {random_dnt()}\r\n"
    return headers if headers != "" else None

def pick_random_header(filename='./resources/headers.txt'):
    """
    Selects a random header from the specified file.
    (Not necessarily used in the main flow, but could be useful.)
    """
    with open(filename, 'r') as file:
        headers = file.read().splitlines()
    return random.choice(headers)

def random_x_forwarded_for():
    """
    Generates a random set of 1 to 4 IPs, separated by commas, for the X-Forwarded-For header.
    """
    num_ips = random.randint(1, 4)
    ips = [".".join(str(random.randint(0, 255)) for _ in range(4)) for _ in range(num_ips)]
    return ", ".join(ips)

def random_dnt():
    """
    Returns '1' or '0' for the DNT (Do Not Track) header randomly.
    """
    return "1" if random.choice([True, False]) else "0"

def generate_referer(url):
    """
    Generates a basic referer from the URL itself, using the same domain.
    """
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme or "http"
    return f"{scheme}://{parsed_url.netloc}/"

def random_user_agent():
    """
    Selects a random user-agent from the predefined list.
    """
    return random.choice(user_agents_list)
