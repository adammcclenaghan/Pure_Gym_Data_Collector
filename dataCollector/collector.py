import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

EMAIL_PIN_FILE = "../resources/email_and_pin.txt"
OUTPUT_FILE = "../resources/collector_output.txt"
LOGIN_PAGE_URL = "https://puregym.com/login"
EMAIL_ELEMENT_ID = "email"
PIN_ELEMENT_ID = "pin"
BROWSER_WAIT_DELAY = 20
PEOPLE_IN_GYM_CSS_SELECTOR = "#main-content > div:nth-child(2) > div > div > div:nth-child(1) > div > div > div > " \
                           "div:nth-child(1) > div > p.para.para--small.margin-none > span"


def get_email_and_pin_from_file():
    """Return a list containing [email, pin]"""
    email_and_pin = []
    with open(EMAIL_PIN_FILE) as fp:
        for count, line in enumerate(fp):
            email_and_pin.append(line)
    return email_and_pin


def login_and_get_people_in_gym_text(email_and_pin):
    """Return string containing something like '30 people' or 'Fewer than 20 people' """
    browser = webdriver.Chrome()
    browser.get(LOGIN_PAGE_URL)
    email = browser.find_element_by_id(EMAIL_ELEMENT_ID)
    pin = browser.find_element_by_id(PIN_ELEMENT_ID)
    # Populate the email field with the value from email_and_pin.txt
    user_email = email_and_pin[0]
    email.send_keys(user_email)
    # Populate the PIN field with the value from email_and_pin.txt
    user_pin = email_and_pin[1]
    pin.send_keys(user_pin)
    # 'Click' the login button
    browser.find_element_by_id("login-submit").click()
    people_in_gym = -1
    try:
        people_in_gym = WebDriverWait(browser, BROWSER_WAIT_DELAY).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, PEOPLE_IN_GYM_CSS_SELECTOR)))\
            .text
    except TimeoutError:
        print("Loading took too much time")
    finally:
        browser.quit()
        return people_in_gym


def get_number_from_people_in_gym_text(people_in_gym_text):
    """Return the number of people in the gym, eg '20 people' -> '20'"""
    pattern = '\d+'
    return int(re.search(pattern, people_in_gym_text).group())


def save_number_to_output_file(number_of_people_in_gym):
    """Save the number of people in the gym to collector_output.txt in resources"""
    with open(OUTPUT_FILE, 'a') as fp:
        fp.write(number_of_people_in_gym + '\n')


if __name__ == '__main__':
    # Get the text containing the number of people in the gym
    people_in_gym_text = login_and_get_people_in_gym_text(get_email_and_pin_from_file())
    # Strip out anything other than the number object
    number_of_people = get_number_from_people_in_gym_text(people_in_gym_text)
    # Don't save the number of people to a file if it is -1 as that indicates we had a timeout error when logging in
    if number_of_people != -1:
        save_number_to_output_file(number_of_people)

