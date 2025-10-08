from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
from dotenv import load_dotenv
import time

load_dotenv()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)
url = os.getenv("GYM_URL") 
driver.get(url)

wait = WebDriverWait(driver, 5)

def login():

    login_button = wait.until(ec.element_to_be_clickable((By.ID, "login-button")))
    login_button.click()

    fill_email = driver.find_element(By.NAME, value="email")
    fill_email.clear()
    fill_email.send_keys(os.getenv("ACCOUNT_EMAIL"), Keys.ENTER)

    fill_password = driver.find_element(By.NAME, value="password")
    fill_password.clear()
    fill_password.send_keys(os.getenv("ACCOUNT_PASSWORD"), Keys.ENTER)

    wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))


def retry(func, retries=7):
    while retries :
        try:
            return func()
        except Exception as e:
            retries -= 1
            if retries == 0:
                print("Failed to connect")
                raise e
                

# logging in
retry(login)

# counters for summary
total_bookings = 0
total_waitlists = 0
already_booked = 0

days_to_book = ["Tue", "Thu"]

# getting the id attribute for a specific day of the week
next_bookings = driver.find_elements(By.CLASS_NAME, value="Schedule_dayTitle__YBybs")
for day in days_to_book:
    for next_booking in next_bookings:
        if next_booking.text.find(day) != -1:
            date_id = next_booking.get_attribute("id")

    class_id = date_id.replace("title", "group")

    # getting all the events on that specific day
    events = driver.find_elements(
        By.XPATH,
        f'//div[@id="{class_id}"]//div[contains(@class, "ClassCard_card__KpCx5")]'
    )

    for event in events:
        event_id = event.get_attribute("id")
        time_id = event_id.replace("card", "time")
        time_event = driver.find_element(By.ID, value=time_id)
        book_id = event_id.replace("class-card", "book-button")
        book_button = driver.find_element(By.ID, value=book_id)

        # getting the class name and date
        class_name_id = event_id.replace("card", "name")
        class_name = driver.find_element(By.ID, value=class_name_id)
        date = driver.find_element(By.ID, value=date_id)
    
        # checking availability and booking if possible
        if time_event.text.find("6:00 PM") != -1:
            if book_button.text == "Booked":
                message = "✓ Already booked: "
                already_booked += 1
            
            elif book_button.text == "Waitlisted":
                message = "✓ Already on waitlist: "
                already_booked += 1

            elif book_button.text == "Join Waitlist":
                book_button.click()
                message = "✓ Joined waitlist for: "
                total_waitlists += 1
                time.sleep(0.5)

            else:
                book_button.click()
                message = "✓ Booked for: "
                total_bookings += 1
                time.sleep(0.5)
            
            print(f"{message}{class_name.text} on {date.text}") 


print("\n" * 3)
print(f"""--- BOOKING SUMMARY ---
Classes booked: {total_bookings}
Waitlists joined: {total_waitlists}
Already booked/waitlisted: {already_booked}
Total Tuesday 6pm classes processed: {total_bookings  +total_waitlists + already_booked}""")
