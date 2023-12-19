import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import NoSuchWindowException

# URL of the Calendly page to check
url = "https://calendly.com/anisha-musti"


def check_event_type_availability():
    driver = None
    try:
        # Initialize Selenium WebDriver
        driver = webdriver.Chrome(
            executable_path='C:\\Users\\pavan\\Downloads\\Compressed\\chromedriver_win32\\chromedriver.exe')
        driver.get(url)

        # Wait and click on "1-1 Meeting"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-id='event-type-marker']"))).click()

        # Check for available date
        dates_selector = "td[role='gridcell'] > button[aria-label*='Times available']"
        next_month_button_selector = "button.u1xbh6v5 > div.JICvU8LFSnVyM9JTRhN0.GNWiGTfCxuJVairsth3Q"

        try:
            available_date = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, dates_selector)))
            available_date.click()
        except TimeoutException:
            # Check if "View next month" button is not present
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, next_month_button_selector)))
            except TimeoutException:
                print("No 'View next month' button found. Trying again...")
                driver.quit()
                return False

            # If the "View next month" button is present, then click it
            next_month_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, next_month_button_selector)))
            next_month_button.click()

            # Now wait for the next month's calendar to load
            time.sleep(5)

            # Retry checking for an available date in the next month
            try:
                available_date = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, dates_selector)))
                available_date.click()
            except TimeoutException:
                print("No available dates for scheduling.")
                driver.quit()
                return False

        # Check for available time slot
        timeslot_selector = "button[data-container='time-button']"
        try:
            available_timeslot = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, timeslot_selector)))
            available_timeslot.click()
        except TimeoutException:
            print("No available time slots for the selected date.")
            driver.quit()
            return False

        # Wait and click on the "Next" button
        next_button_selector = "button[role='button'][aria-label^='Next']"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, next_button_selector))).click()

        # Fill in the Name field
        name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='full_name']")))
        name_input.send_keys("Anisha Musti")

        # Fill in the Email field
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email']")))
        email_input.send_keys("anisha.musti@gmail.com")

        # Wait and click on the "Schedule Event" button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[type='submit']"))).click()

        # Check for confirmation message
        confirmation_selector = "h1.G6pzpWWDZVBxS7o1DEVf.xnAUNtpDwlToi_A5N6eW"
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, confirmation_selector)))
        except TimeoutException:
            print("Failed to detect the confirmation page within the given time frame.")
            driver.quit()
            return False

        driver.quit()  # Closing the browser session after confirming the scheduling
        return True

    except NoSuchWindowException:
        print("Browser has been closed by user. Retrying...")
        return False

    except Exception as e:
        print(f"Error: {str(e)}")
        if driver:  # Ensure driver object exists before trying to quit it
            driver.quit()  # Close the browser in case of an error to avoid memory leaks
        return False


# Check for event type availability every second
while not check_event_type_availability():
    time.sleep(1)

# Once an appointment is scheduled, the loop will break
print("An appointment is scheduled!")
