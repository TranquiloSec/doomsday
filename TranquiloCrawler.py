import requests
from bs4 import BeautifulSoup
import tldextract
from urllib.parse import urljoin
import time

# Global set to store visited links and avoid revisits
visited_links = set()

# List to store information about pages with the longest response times
maiores_headers = []

# Limit on how many slow pages will be kept in the maiores_headers list
limite_maiores_headers = 5

# Global dictionary of HTTP headers, which can be configured in underAttack mode
headers_g = {}

# Maximum number of pages to visit, preventing the crawler from running indefinitely
MAX_PAGES = 25

def parse_raw_headers(raw_headers):
    """
    Converts a set of raw headers (in bytes or string) into a dictionary.

    This method is useful when working with headers obtained directly from a raw HTTP response.
    It separates each header line and creates a dictionary where keys are header names 
    and values are their corresponding contents.
    """
    if isinstance(raw_headers, bytes):
        # If headers are in bytes, decode them into string
        headers_str = raw_headers.decode('utf-8')
    else:
        headers_str = raw_headers

    headers_lines = headers_str.split("\r\n")
    
    headers = {}
    for line in headers_lines:
        # Checks if the header line follows the "Key: Value" format
        if ': ' in line:
            key, value = line.split(': ', 1)
            headers[key] = value
    return headers

def realizar_crawl(url, underAttack=False, headers_g=headers_g):
    """
    Entry function to start the crawling process.

    From the initial URL, this function extracts the domain and calls the 'crawl' function
    to traverse internal pages. If underAttack mode is enabled, it assumes headers_g contains
    the necessary headers to bypass protections.

    Parameters:
    - url: Initial URL of the website to crawl.
    - underAttack: Boolean indicating whether to use special headers.
    - headers_g: Global HTTP headers dictionary.
    """
    # Extracts the registered domain from the given URL
    domain = tldextract.extract(url).registered_domain

    print(f"Crawling the domain: {domain}")
    # Starts the internal crawling process
    crawl(url, domain, headers_g, underAttack=underAttack)

def crawl(url, domain, headers_g, underAttack=False):
    """
    Recursive function to crawl within the same domain.

    For each visited URL, an HTTP request is made, the response time is measured,
    and the result is stored in 'maiores_headers' if it's one of the longest response times.
    Then, the HTML is analyzed to find internal links, calling 'crawl' again for each new link.

    Parameters:
    - url: Current URL to be accessed.
    - domain: Base domain to filter internal links.
    - headers_g: Global HTTP headers dictionary.
    - underAttack: Boolean indicating whether we are in underAttack mode, which may
      alter the behavior of headers.
    """

    # If we’ve already visited this URL or reached the page limit, return

    if url in visited_links:
        return
    if len(visited_links) >= MAX_PAGES:
        return

    # Mark the current URL as visited
    visited_links.add(url)

    try:
        # Mark the time before making the request to measure the response time
        start_time = time.time()
        # Make the HTTP request with possible custom headers
        response = requests.get(url, headers=headers_g, timeout=5)
        end_time = time.time()

        # Calculate the response time for the request
        response_time = end_time - start_time

        print(f"Accessing: {url} | Response time: {response_time:.2f} seconds")

        # Store information about this page (URL, headers, response time)
        maiores_headers.append({'url': url, 'headers': headers_g, 'response_time': response_time})
        # Store information about this page (URL, headers, response time)
        maiores_headers.sort(key=lambda x: x['response_time'], reverse=True)
        # Keep only the N pages with the longest response times (as defined in limite_maiores_headers)
        if len(maiores_headers) > limite_maiores_headers:
            maiores_headers.pop()

        # Attempt to parse the HTML content of the page
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Erro ao parsear HTML de {url}: {e}")
            return

        # Find all 'a' links with href attribute
        for link in soup.find_all('a', href=True):
            link_url = link['href']
            # Create the absolute URL from the found link
            full_url = urljoin(url, link_url)

            # If the link is from the same domain and hasn't been visited yet, continue crawling
            if is_same_domain(full_url, domain) and full_url not in visited_links:
                print(f"Subdiretório encontrado: {full_url}")
                crawl(full_url, domain, headers_g, underAttack=underAttack)

    except requests.exceptions.RequestException as e:
        # If a network error occurs (timeout, connection issue, etc.), the error is printed 
        # and the function returns without crashing the program.
        print(f"Error accessing {url}: {e}")

def is_same_domain(url, domain):
    """
    Checks if the provided URL belongs to the same base domain.

    Parameters:
    - url: URL to be checked.
    - domain: Base domain extracted from the initial URL.

    Return:
    - True if the domain of the URL is the same as 'domain', otherwise False.
    """
    extracted_domain = tldextract.extract(url).registered_domain
    return extracted_domain == domain

def iniciar_crawl(url, underAttack=False, cookie=None, userAgent=None):
    """
    High-level function to start the crawling process.

    If underAttack mode is enabled, it configures special headers 
    (such as cookies and user-agent) in the global 'headers_g' dictionary.
    Then, it starts the crawling process by calling 'realizar_crawl'.

    Parameters:
    - url: Initial URL to start the crawling.
    - underAttack: Boolean to indicate if special headers should be used.
    - cookie: Cookie to be used in requests, if underAttack is True.
    - userAgent: User-Agent to be used in requests, if underAttack is True.

    Return:
    - The 'maiores_headers' list containing information about pages with the longest response times.
    """

    global headers_g
    # If underAttack is enabled, adjusts the global headers
    if underAttack:
        headers_g = {
            'Cookie': cookie,
            'User-Agent': userAgent
        }

    # Starts the crawling process from the base URL
    realizar_crawl(url, underAttack=underAttack, headers_g=headers_g)

    # At the end of the crawling process, returns the list of pages with the longest response times
    return maiores_headers
