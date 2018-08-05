import datetime
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display

EMAIL_PIN_FILE = "../resources/email_and_pin.txt"
OUTPUT_FILE = "../resources/collector_output.txt"
LOGIN_PAGE_URL = "https://puregym.com/login"
EMAIL_ELEMENT_ID = "email"
PIN_ELEMENT_ID = "pin"
BROWSER_WAIT_DELAY = 10
PEOPLE_IN_GYM_CSS_SELECTOR = "#main-content > div:nth-child(2) > div > div > div:nth-child(2) > div > div > div > " \
                             "div:nth-child(1) > div > p.para.para--small.margin-none > span "
SKIP_SURVEY_CSS_SELECTOR = "#canSkip"
GO_TO_DASHBOARD_CSS_SELECTOR = "#main-content > div.page__content > div > div > div.col-xs-12.col-sm-5.col-md-4 > " \
                               "div:nth-child(1) > a "


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
    # Sometimes there is a survey, handle this
    handle_survey(browser)
    # The first time you login, a different screen is shown than the default
    # /members/first-login/
    handle_first_login(browser)
    people_in_gym = "Invalid"
    try:
        people_in_gym = WebDriverWait(browser, BROWSER_WAIT_DELAY).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, PEOPLE_IN_GYM_CSS_SELECTOR)))\
            .text
    except TimeoutException:
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
    now = datetime.datetime.now()
    with open(OUTPUT_FILE, 'a') as fp:
        fp.write(str(now.date()) + ',' + str(now.strftime("%H:%M")) + ',' + str(number_of_people_in_gym) + '\n')


def handle_survey(browser):
    """Attempt to click the 'skip' button on a survey in the event that it appears"""
    wait_for_element_then_click(browser, SKIP_SURVEY_CSS_SELECTOR, "canSkip")


def handle_first_login(browser):
    """Handle the page shown under /members/first-login/"""
    # Untested
    wait_for_element_then_click(browser, GO_TO_DASHBOARD_CSS_SELECTOR, GO_TO_DASHBOARD_CSS_SELECTOR)


def wait_for_element_then_click(browser, css_selector, element_id):
    """Wait for a defined amount of time before trying to click on a specified element"""
    wait_for_element_then_click_custom_timeout(browser, css_selector, element_id, BROWSER_WAIT_DELAY)


def wait_for_element_then_click_custom_timeout(browser, css_selector, element_id, timeout):
    """Wait for a defined amount of time before trying to click on a specified element"""
    try:
        WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        browser.find_element_by_id(element_id).click()
    except TimeoutException:
        pass


if __name__ == '__main__':
    display = Display(visible=0, size=(800, 600))
    display.start()
    # Get the text containing the number of people in the gym
    people_in_gym_text = login_and_get_people_in_gym_text(get_email_and_pin_from_file())
    # Only continue if we didn't encounter a TimeoutException
    if people_in_gym_text != "Invalid":
        # Strip out anything other than the number object
        number_of_people = get_number_from_people_in_gym_text(people_in_gym_text)
        save_number_to_output_file(number_of_people)
    display.stop()
