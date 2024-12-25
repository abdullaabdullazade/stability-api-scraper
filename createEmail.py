import requests
import time

BASE_URL = "https://www.1secmail.com/api/v1/"

def create_email():
    response =  requests.get(f"{BASE_URL}?action=genRandomMailbox&count=1")
    if response.status_code == 200:
        email = response.json()[0]
        return email
    else:
        return None

def get_messages(email):
    username, domain = email.split("@")
    url = f"{BASE_URL}?action=getMessages&login={username}&domain={domain}"
    
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            messages = response.json()
            if messages:
                break
        else:
            return None
        time.sleep(1)  

    for message in messages:
        message_content = read_message(email, message['id'])
        if not message_content:
            continue

        body = message_content.get("body", "")
        if "https://stabilityai.us.auth0.com" in body:
            start_index = body.find("https://stabilityai.us.auth0.com")
            end_index = body.find('"', start_index)  # Find email url
            url = body[start_index:end_index]
            return url
    return None

def read_message(email, message_id):
    username, domain = email.split("@")
    url = f"{BASE_URL}?action=readMessage&login={username}&domain={domain}&id={message_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

if __name__ == "__main__":
    email = create_email()
    
