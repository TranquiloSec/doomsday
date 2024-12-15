# DoomsDay

**DoomsDay** is an advanced load and DDoS testing toolkit designed for research, academic, and controlled testing scenarios. Developed by the TranquiloSec team for a college project, this tool provides flexible configuration options and supports a variety of environments and techniques, including multi-threading, multi-processing, dynamic headers, proxy usage, optional crawler-based target selection, and bypass methods for cloud protection layers.

**Important:** This software is intended solely for legitimate testing, research, or academic purposes on systems you own or have explicit permission to test. Misuse of this software may be illegal and is strictly discouraged. Always comply with local laws and regulations.

---

## Key Features

- **Multi-Process and Multi-Thread Attacks:**  
  Utilize multiprocessing and threading to send large volumes of simultaneous requests, enhancing stress and load testing.

- **Dynamic Headers and Under-Attack Mode:**  
  Generate randomized HTTP headers and optionally bypass under-attack protection (e.g., Cloudflare UAM) by incorporating special cookies and user-agents.

- **Proxy Support (Optional):**  
  Integrate SOCKS5 proxies to anonymize requests, simulating more realistic and complex scenarios.

- **Automated Crawler (Optional):**  
  Crawl the target domain to find the "heaviest" or slowest URLs, allowing for more focused testing on high-load endpoints.

- **Resource Validation:**  
  Automatically ensure required directories and files (e.g., `resources`, `ua.txt`, `proxy.txt`, `headers.txt`) exist before running tests.

---

## Requirements

- **Python 3:** Required on Unix/Linux/WSL or Windows environments.
- **Git:** For cloning the repository.
- **Internet Connection:** For optional proxy downloading and crawling.
- **Proper Authorization:** Ensure you have permission to test the target system.

---

## Installation

### Common Steps

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/ConfettiOnTheWall/DoomsDay.git
    ```

2. **Navigate into the Project Directory:**
    ```bash
    cd DoomsDay
    ```

### On Windows

1. Run the provided setup file:
    ```bash
    DoomsDay_setup.bat
    ```
    This script installs dependencies and configures the environment.

### On Unix/Linux or WSL

1. **Create a Virtual Environment:**
    ```bash
    python3 -m venv venv
    ```

2. **Activate the Virtual Environment:**
    ```bash
    source venv/bin/activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

Your environment is now set up and ready for use.

---

## Usage

Once your environment is prepared, run DoomsDay with various command-line options:

```bash
python3 TranquiloDDoS.py --url "https://targetdomain.com" --thread 500
````

**Other Options:**

- `--underAttack`: Attempt to bypass Cloudflare Under Attack Mode.
- `--useProxy`: Enable proxy usage via a provided proxy list.
- `--useCrawler`: Crawl the target domain to find heavy endpoints before initiating tests.
- `--numHeaders`: Specify the number of dynamically generated header sets.
- `--proxyList`: Provide a custom proxy list file.

For a full list of options:

```bash
python3 TranquiloDDoS.py --help
```

**Deactivate the Virtual Environment:**

```bash
deactivate
```

## Contributing

Contributions are welcome! Submit issues, open pull requests, or share ideas in the GitHub repository. Any improvements or features are appreciated.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Disclaimer

**This tool is intended solely for educational and authorized testing purposes.** Unauthorized use may violate laws and regulations. The authors and contributors assume no liability for misuse or damage. Always adhere to local laws and obtain proper authorization before conducting any stress or DDoS tests.
