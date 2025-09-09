# Ticketmaster Event Monitor

This script monitors a specific Ticketmaster event page for a status change. When "Em breve" status is removed, that indicates that the ticket queue is open. When this change is detected, it sends an email notification.

## Setup

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd ticketmaster
    ```

2.  **Create a Virtual Environment**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **`URL`**: Set the `URL` variable to the Ticketmaster event page you want to monitor.
    ```python
    URL = 'https://www.ticketmaster.com.br/event/your-event-here'
    ```

2.  **Email Settings**: Configure the email settings to enable notifications.
    ```python
    SENDER_EMAIL = 'your_email@gmail.com'
    SENDER_PASSWORD = 'your_gmail_app_password' # Use an App Password, not your regular password
    RECIPIENT_EMAIL = 'email_to_notify@example.com'
    ```
- [Learn how to create an App Password](https://support.google.com/accounts/answer/185833).

3.  **Monitor Settings (Optional)**: You can adjust the check interval and page load timeout if needed.
    ```python
    CHECK_INTERVAL_SECONDS = 300  # 5 minutes
    PAGE_LOAD_TIMEOUT = 20
    ```
    
### Note for International Users

In case you're not from Brazil, you will probably have to change the "Em breve" string to how Ticketmaster writes it in your language.

## Usage

Once configured, run the script from your terminal:

```bash
python ticket.py
```

## Dependencies

- [Selenium](https://www.selenium.dev/)
- [Undetected Chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
