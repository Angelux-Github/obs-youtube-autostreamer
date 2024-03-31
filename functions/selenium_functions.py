from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import sys
import os


def extract_video_id(url):
    # Extract the video ID from the URL
    return url.replace('https://studio.youtube.com/video/', '').replace('/livestreaming', '')

def get_driver(site):

    # Gets default user directory for cookies to load youtube channel.
    # Get the current user's home directory
    home_dir = os.path.expanduser('~')

    # Extract the username from the home directory path
    username = os.path.basename(home_dir)

    # Set options for the Chrome driver
    user_data_dir = "C:/Users/{}/AppData/Local/Google/Chrome/User Data".format(username)

    print(f"The current user is: {username}")
    print(f"Chrome cookies directory should be: {user_data_dir}")

    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_argument(f"user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=options)
    driver.get(site)

    return driver

def get_upcoming_stream_broadcast_id():
    driver = get_driver("https://studio.youtube.com/channel/UC/livestreaming")

    WebDriverWait(driver, 30).until(EC.url_contains('/video/'))
    current_url = driver.current_url
    print(f'New URL: {current_url}')

    selenium_id = extract_video_id(current_url)
    print(f"Selenium Broadcast ID is: {selenium_id}")

    # Create the directory if it does not exist
    os.makedirs('../user_data', exist_ok=True)

    with open('../user_data/broadcast_id.txt', 'w') as file:
        file.write(selenium_id)

    driver.quit()


def update_upcoming_stream_title(new_title):
    driver = get_driver("https://studio.youtube.com/channel/UC/livestreaming")

    # Wait for the upcoming streams section to load
    WebDriverWait(driver, 30).until(EC.url_contains('/video/'))
    sleep(1)

    # Click on the "Edit" button for the first upcoming stream
    edit_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'edit-button')))
    edit_button.click()

    # Use the TAB key to navigate to the title field
    actions = webdriver.ActionChains(driver)
    actions.send_keys(Keys.TAB * 3)
    actions.perform()

    # Wait for the title field to be clickable
    title_field = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//ytcp-social-suggestion-input[@id="input"]//div[@id="textbox"]')))

    # Clear the existing title and enter the new title
    title_field.click()  # Click to ensure the field is focused
    actions = webdriver.ActionChains(driver)
    actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()  # Select all text
    actions.send_keys(Keys.DELETE).perform()  # Delete selected text
    title_field.send_keys(new_title)

    # Save the changes
    save_button = driver.find_element(By.XPATH, '//ytcp-button[@id="save-button"]')
    save_button.click()

    # Wait for the changes to be saved
    WebDriverWait(driver, 30).until(EC.invisibility_of_element(save_button))

    print(f"Stream title updated to: {new_title}")
    driver.quit()


def send_whats_app_message(name, message):
    driver = get_driver('https://web.whatsapp.com/')

    # Wait for WhatsApp web to load
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true" and @title="Search input textbox"]')))

    search_bar = driver.find_element(By.XPATH, '//div[@contenteditable="true" and @title="Search input textbox"]')
    search_bar.click()
    sleep(1)
    search_bar.send_keys(name + Keys.ENTER)

    # Wait for the chat to open
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true" and @title="Type a message"]')))
    message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true" and @title="Type a message"]')
    message_box.click()

    #OPTIONAL CODE FOR MANUAL TYPING OF THE YOUTUBE LINK INTO THE MESSAGE
    try:
        with open('../user_data/broadcast_id.txt', 'r') as file:
            broadcast_id = file.read().strip()
            youtubelink = "https://www.youtube.com/watch?v=" + broadcast_id
    except FileNotFoundError:
        print("The file or directory does not exist. Please check the path and try again.")
        print("Try running the get_upcoming_stream_broadcast_id function to automatically create this id.")
        print("Aborting proccess - selenium_function.py Module - send_whats_app_message() Function.")
        driver.quit()

    message = message #REDUNDANT BUT HERE IN CASE YOU WANT TO INSERT YOUR MESSAGE MANUALLY HERE.

    # To avoid sending multiple messages for new lines, we will use selenium's built-in keys
    ln = Keys.SHIFT + Keys.ENTER + Keys.SHIFT
    message = message.replace('\n', ln)

    sleep(2)
    message_box.send_keys(message)

    #Wait for url preview to generate before sending the message
    sleep(15)
    message_box.send_keys(" " + Keys.ENTER)
    sleep(2)

    driver.quit()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "get_broadcast_id":
            get_upcoming_stream_broadcast_id()
        elif sys.argv[1] == "send_whatsapp_message":
            if len(sys.argv) == 4:
                name = sys.argv[2]
                message = sys.argv[3]
                send_whats_app_message(name, message)
            else:
                print("Usage: python.exe selenium_functions.py send_whatsapp_message 'Contact Name' 'Message'")
        elif sys.argv[1] == "update_title":
            if len(sys.argv) == 3:
                new_title = sys.argv[2]
                update_upcoming_stream_title(new_title)
            else:
                print("Usage: python.exe selenium_functions.py update_title 'your new title'")
        else:
            print("Invalid command. Available commands are: get_broadcast_id, send_whatsapp_message")
    else:
        print("Usage: python.exe selenium_functions.py [command]")