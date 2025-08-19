import argparse
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

RETRY_DURATION_SECONDS = 120
RETRY_INTERVAL_SECONDS = 5

def is_captcha_present(driver):
    try:
        if driver.find_elements(By.XPATH, "//iframe[contains(@src, 'recaptcha')]"):
            return True
        if "captcha" in driver.page_source.lower():
            return True
    except:
        pass
    return False

def attempt_check_in(confirmation, first, last):
    print(f"[{datetime.datetime.now()}] Trying check-in...")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Remove this to see browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.southwest.com/air/check-in/index.html")
        time.sleep(2)

        driver.find_element(By.ID, "confirmationNumber").send_keys(confirmation)
        driver.find_element(By.ID, "firstName").send_keys(first)
        driver.find_element(By.ID, "lastName").send_keys(last)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Check In')]").click()
        time.sleep(3)

        if is_captcha_present(driver):
            print("[!] CAPTCHA detected. Manual intervention required.")
            return False

        if "boarding pass" in driver.page_source.lower():
            print("[✓] Check-in successful!")
            return True
        else:
            print("[!] Check-in may not have completed. Retrying...")
            return False

    except Exception as e:
        print("Error during check-in:", e)
        return False
    finally:
        driver.quit()

def retry_check_in(confirmation, first, last):
    start_time = time.time()
    while time.time() - start_time < RETRY_DURATION_SECONDS:
        success = attempt_check_in(confirmation, first, last)
        if success:
            break
        time.sleep(RETRY_INTERVAL_SECONDS)
    else:
        print("[✗] Could not complete check-in within time limit.")

def schedule_checkin(confirmation, first, last, checkin_time):
    run_time = datetime.datetime.strptime(checkin_time, "%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now()
    delay = (run_time - now).total_seconds()

    if delay > 0:
        print(f"[🕓] Waiting until {checkin_time} to start check-in...")
        time.sleep(delay)
        retry_check_in(confirmation, first, last)
    else:
        print("[!] The scheduled time is in the past.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Southwest Check-In Bot")
    parser.add_argument("--confirmation", required=True, help="Confirmation number")
    parser.add_argument("--first", required=True, help="First name")
    parser.add_argument("--last", required=True, help="Last name")
    parser.add_argument("--checkin_time", required=True,
                        help="Check-in time (format: YYYY-MM-DD HH:MM:SS)")

    args = parser.parse_args()

    schedule_checkin(args.confirmation, args.first, args.last, args.checkin_time)