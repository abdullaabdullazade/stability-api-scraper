import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)


def create_email():
    domain = requests.get("https://api.mail.tm/domains").json()["hydra:member"][0][
        "domain"
    ]
    email = f"{int(time.time())}@{domain}"

    payload = {"address": email, "password": "StrongPass123"}
    response = requests.post("https://api.mail.tm/accounts", json=payload)

    if response.status_code == 201:
        return email, payload["password"]
    else:
        raise Exception("email cant be created")


def get_messages(email, password):
    token_response = requests.post(
        "https://api.mail.tm/token", json={"address": email, "password": password}
    )

    if token_response.status_code != 200:
        return "token cant be created"

    token = token_response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    for _ in range(30):
        response = requests.get("https://api.mail.tm/messages", headers=headers)
        messages = response.json()["hydra:member"]

        for msg in messages:
            email_response = requests.get(
                f"https://api.mail.tm/messages/{msg['id']}", headers=headers
            )
            email_content = email_response.json()["text"]

            if "https://stabilityai.us.auth0.com" in email_content:
                start_index = email_content.find("https://stabilityai.us.auth0.com")
                end_index = email_content.find("#", start_index)  #find url
                url = email_content[start_index : end_index + 1]
                return url

        time.sleep(5)

    return None


def run():
    try:
        email, password = create_email()
        print(f"email: {email}")

        driver.get("https://platform.stability.ai/")
        driver.find_element(By.XPATH, "//a[text()='Login']").click()
        driver.find_element(By.XPATH, "//a[contains(@href, 'signup')]").click()
        driver.implicitly_wait(5)

        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys("StrongPass123")
        driver.find_element(
            By.XPATH, "//button[@name='action' and @value='default']"
        ).click()

        link = get_messages(email, password)
        #print(email, password, link)
        if not link:
            raise Exception("link cant be found")

        driver.execute_script(f"window.open('{link}', '_blank');")
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element(
            By.XPATH, "//button[@name='action' and @value='accept']"
        ).click()

        driver.find_element(By.XPATH, "//a[@href='/account/keys']").click()
        time.sleep(10)
        driver.execute_script(
            """
        var elements = document.getElementsByClassName("flex items-center justify-center");
        if (elements.length > 5) {
            elements[5].click();
        } 
    """
        )
        """
        Fuck this moment :(


        """
        div_element = driver.find_element(
            By.XPATH,
            "//div[@class='col-span-3 text-left font-mono']//div[@class='truncate']",
        )
        value = div_element.text
        with open("apikeys.txt", "a+", encoding="utf-8") as a:
            print("\n" + value, file=a)

        driver.quit()

    except Exception as e:
        print(f"error: {e}")


run()
