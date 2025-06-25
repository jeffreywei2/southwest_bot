# Southwest Auto Check-In Bot

Automates the check-in process for Southwest Airlines flights using Selenium and Python.

## Features

- Automatically checks in at a specified time (typically 24 hours before departure)
- Retries every 30 seconds for up to 10 minutes if check-in fails
- Detects CAPTCHA and stops retries if triggered
- Command-line interface (CLI) with `argparse`
- Headless browser support (ChromeDriver)
- Compatible with cron jobs or Task Scheduler for scheduled runs
- Portable setup using `webdriver-manager`

## Tech Stack

- Python 3
- Selenium for browser automation
- ChromeDriver for controlling Chrome
- argparse for command-line interface
- webdriver-manager for managing browser drivers
- Optional: Shell scripting and cron for system-level scheduling

## Usage

### 1. Install dependencies

```bash
pip install selenium webdriver-manager


Run the bot

    python sw_checkin_bot.py \
    --confirmation ABC123 \
    --first John \
    --last Doe \
    --checkin_time "2025-06-25 06:55:00"


Run every 30 seconds for 10 minutes

    The script includes a built-in retry mechanism. Simply run it once, and it will retry check-in every 30 seconds for up to 10 minutes. Times are variable and can be changed

Automate with cron
    Edit your crontab with:
    crontab -e

Add a line to schedule it:
    55 6 24 6 * /usr/bin/python3 /path/to/sw_checkin_bot.py --confirmation ABC123 --first John --last Doe --checkin_time "2025-06-25 06:55:00"
