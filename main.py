import time
from createEmail import create_email, get_messages
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options


options = Options()
options.add_argument("--headless")  
options.add_argument("--disable-gpu") 



service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service,options=options)
def run():
 try:
    email = create_email()


    driver.get("https://platform.stability.ai/")

    driver.find_element(By.XPATH, "//a[text()='Login']").click()
    driver.find_element(By.XPATH, "//a[contains(@href, 'signup')]").click()

    driver.implicitly_wait(5) 

    email_input = driver.find_element(By.XPATH, "//input[@name='email']") 
    email_input.send_keys(email)

    password_input = driver.find_element(By.XPATH, "//input[@name='password']")  
    password_input.send_keys(email+"1") 

    continue_button = driver.find_element(By.XPATH, "//button[@name='action' and @value='default']")
    continue_button.click()


    link = get_messages(email=email)


    driver.execute_script(f"window.open('{link}', '_blank');")

    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(By.XPATH, "//button[@name='action' and @value='accept']").click() #authorization

    path_element = driver.find_element(By.XPATH, "//a[@href='/account/keys']")
    path_element.click()


    #driver.get('https://platform.stability.ai/account/keys')
    time.sleep(15)
    driver.execute_script("""
    var elements = document.getElementsByClassName("flex items-center justify-center");
    if (elements.length > 5) {
         elements[5].click();
    } 
""")
    """
    Fuck this moment :(


    """
    div_element =  driver.find_element(By.XPATH, "//div[@class='col-span-3 text-left font-mono']//div[@class='truncate']")
    value = div_element.text
    with open('apikeys.txt','a+',encoding='utf-8') as a:
        print("\n"+value,file=a)

    driver.quit()

 except:
    return 'error'

if __name__ == "__main__":
    run()

