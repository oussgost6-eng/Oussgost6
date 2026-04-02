import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import subprocess
def load_cookies(driver, file):
    with open(file, 'r') as f:
        for line in f:
            if not line.startswith('#'):
                parts = line.strip().split('\t')
                if len(parts) >= 7:
                    driver.add_cookie({
                        'domain': parts[0],
                        'name': parts[5],
                        'value': parts[6],
                        'path': parts[2],
                    })

# Configuration Chrome pour Railway
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

chromedriver_path = subprocess.getoutput("which chromedriver")
print("Chemin de chromedriver :", chromedriver_path)

chrome_service = Service(chromedriver_path)
driver = webdriver.Chrome(service=chrome_service, options=options)

# Accéder à Facebook et charger les cookies
driver.get("https://www.facebook.com")
time.sleep(5)

load_cookies(driver, "cookies.txt")
driver.refresh()
time.sleep(5)

# Accéder à Messenger
driver.get("https://www.facebook.com/messages")
time.sleep(10)

replied = set()

# Boucle principale
while True:
    try:
        conversations = driver.find_elements(By.XPATH, "//div[@role='row']")

        for conv in conversations[:5]:
            try:
                conv.click()
                time.sleep(5)

                messages = driver.find_elements(By.XPATH, "//div[@role='gridcell']")
                last_msg = messages[-1].text

                # Vérifie si ce message n'a pas déjà été répondu
                if last_msg not in replied:
                    box = driver.find_element(By.XPATH, "//div[@role='textbox']")
                    
                    # Message standard
                    response = "Salam 7biba ça va 3lik"
                    
                    box.send_keys(response)
                    box.send_keys(Keys.RETURN)
                    
                    replied.add(last_msg)
                    time.sleep(10)

            except:
                continue

        time.sleep(20)

    except:
        time.sleep(10)