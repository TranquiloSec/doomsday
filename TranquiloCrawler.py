import requests
from bs4 import BeautifulSoup
import tldextract
from urllib.parse import urljoin
import time

visited_links = set()
maiores_headers = []
limite_maiores_headers = 5 

headers_g = {}

# Função para converter headers de bytes ou strings para dicionário
def parse_raw_headers(raw_headers):
    if isinstance(raw_headers, bytes):
        headers_str = raw_headers.decode('utf-8')
    else:
        headers_str = raw_headers  # Já está em formato de string

    headers_lines = headers_str.split("\r\n")
    
    headers = {}
    for line in headers_lines:
        if ': ' in line:
            key, value = line.split(': ', 1)
            headers[key] = value
    return headers

# Função para rastrear e coletar links dentro do domínio
def realizar_crawl(url, underAttack=False):
    domain = tldextract.extract(url).registered_domain
    
    print(f" Rastreando o domínio: {domain}")
    crawl(url, domain, underAttack=underAttack)

#Função auxiliar para realizar o crawl dentro do domínio
def crawl(url, domain, underAttack=False):

    if url in visited_links:
        return
    visited_links.add(url)

    try:
        
        # Medir o tempo de resposta da requisição
        start_time = time.time()
        response = requests.get(url, headers=headers_g, timeout=5)
        end_time = time.time()
        response_time = end_time - start_time

        print(f" Acessando: {url} | Tempo de resposta: {response_time:.2f} segundos")
         # Adiciona os headers à lista maiores_headers e ordena pela maior response_time
         
        maiores_headers.append({'url': url, 'headers': headers_g, 'response_time': response_time})
        maiores_headers.sort(key=lambda x: x['response_time'], reverse=True)
        
        # Mantém apenas os top N maiores headers
        if len(maiores_headers) > limite_maiores_headers:
            maiores_headers.pop()
            
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            link_url = link['href']
            full_url = urljoin(url, link_url)  # Cria a URL absoluta

            if is_same_domain(full_url, domain) and full_url not in visited_links:
                # Extrai apenas os subdiretórios
                path = tldextract.extract(full_url).suffix + full_url.split(domain)[-1]
                if path.startswith('/'):
                    print(f" Subdiretório encontrado: {full_url}")
                crawl(full_url, domain, headers_g)
                
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")


# Função para verificar se o link está no mesmo domínio
def is_same_domain(url, domain):
    extracted_domain = tldextract.extract(url).registered_domain
    return extracted_domain == domain

def iniciar_crawl(url, underAttack=False, cookie=None, userAgent=None):
    if underAttack:
        global headers_g
        headers_g = {
        'Cookie': cookie,
        'User-Agent' : userAgent
        }
        realizar_crawl(url, underAttack=underAttack)
    else:
        realizar_crawl(url)
    return maiores_headers