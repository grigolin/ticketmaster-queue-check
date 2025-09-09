import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- CONFIG

# 1. page to monitor
URL = 'https://www.ticketmaster.com.br/event/ufc-fight-night-rj-pre-venda-cadastrados-parceiros'

# 2. email settings 
SENDER_EMAIL = ''
SENDER_PASSWORD = ''
RECIPIENT_EMAIL = ''

# 3. monitor settings
CHECK_INTERVAL_SECONDS = 300  # 300 seconds = 5 minutes
PAGE_LOAD_TIMEOUT = 20  # seconds to wait for element to appear on the page

# --- END OF CONFIG


def send_notification_email():
    """sends an email notification when the queue is open."""
    subject = "Ticketmaster: Event Update!"
    body = f"""
    The status of the event has changed.

    The queue might be open now!

    Go to the page immediately: {URL}
    """
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        print("Connecting to email server...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("✅ Notification email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email. Error: {e}")


def check_ticket_status():
    """
    checks the Ticketmaster page
    returns True if the 'Em breve' status is GONE (queue open), False otherwise.
    """
    driver = None
    try:
        print("Initializing stealth browser...")
        options = uc.ChromeOptions()
        options.headless = True
        driver = uc.Chrome(options=options)
        print(f"Navigating to {URL}...")
        driver.get(URL)
        print(
            f"Waiting up to {PAGE_LOAD_TIMEOUT} seconds for the 'Em breve' element...")

        css_selector = "div.event-status.status-comingsoon"

        wait = WebDriverWait(driver, PAGE_LOAD_TIMEOUT)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, css_selector)))


        print("Status: 'Em breve' found. Queue is not open yet.")
        return False

    except TimeoutException:

        print("✅ Status: 'Em breve' element NOT FOUND! Queue might be open!")
        return True
    except Exception as e:
        print(f"❌ An unexpected error occurred during the browser check: {e}")
        return False
    finally:
        if driver:
            print("Closing browser.")
            driver.quit()


if __name__ == "__main__":
    print("--- Ticketmaster Selenium Monitor Started ---")
    try:
        while True:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n[{current_time}] Running check...")

            is_queue_open = check_ticket_status()

            if is_queue_open:
                send_notification_email()
                print("Notification sent. Stopping monitor.")
                break

            print(
                f"Waiting for {CHECK_INTERVAL_SECONDS / 60:.0f} minutes before next check...")
            time.sleep(CHECK_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\n--- Monitor stopped by user. ---")
