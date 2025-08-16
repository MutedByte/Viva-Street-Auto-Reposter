import json
import time
import random
import signal
import sys
from DrissionPage import ChromiumPage, ChromiumOptions
from CloudflareBypasser import CloudflareBypasser

EMAIL = "youremail@example.com"
PASSWORD = "yourpassword"
LOGIN_URL = "https://www.vivastreet.co.uk/user/login?authorize_refer=/user/account/ads"
COOKIE_FILE = "vivastreet_cookies.json"

driver = None

def load_cookies():
    try:
        with open(COOKIE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_cookies(cookies):
    with open(COOKIE_FILE, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=4)


def login(cf_bypasser):
    driver.get(LOGIN_URL)
    cf_bypasser.bypass()
    time.sleep(2)

    driver.ele("#email").clear().input(EMAIL)
    time.sleep(7)
    driver.ele("#current-password").clear().input(PASSWORD + '\n')
    try:
        driver.ele("@data-automation=urD_Login").click()
    except:
        pass
    time.sleep(5)

    adult_cookie = {
        "domain": ".vivastreet.co.uk",
        "expirationDate": 1755906260.049803,
        "hostOnly": False,
        "httpOnly": False,
        "name": "adult_disclaimer",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "value": "adult_services"
    }
    new_ads_cookie = {
        "domain": ".vivastreet.co.uk",
        "expirationDate": 1755907745.534947,
        "hostOnly": False,
        "httpOnly": False,
        "name": "kiwii_show_new_my_ads",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "value": "false",
    }
    driver.set.cookies([adult_cookie, new_ads_cookie])
    print("Extra cookies set.")

    driver.refresh()
    time.sleep(2)

    cookies = driver.cookies()
    save_cookies(cookies)
    print(f"Cookies saved to {COOKIE_FILE}")


def ensure_logged_in(cf_bypasser):
    while True:
        try:
            driver.get("https://www.vivastreet.co.uk/account_classifieds.php")
            cf_bypasser.bypass()
            time.sleep(3)

            logout_button = driver.ele('#vs_user_menu_logout_link', timeout=5)
            if logout_button:
                print("Already logged in.")
                return True

            cookies = load_cookies()
            if cookies:
                driver.set.cookies(cookies)
                driver.refresh()
                time.sleep(3)
                logout_button = driver.ele('#vs_user_menu_logout_link', timeout=5)
                if logout_button:
                    print("Logged in with saved cookies.")
                    return True

            print("Logging in with credentials...")
            login(cf_bypasser)
            time.sleep(3)
            logout_button = driver.ele('#vs_user_menu_logout_link', timeout=5)
            if logout_button:
                print("Login successful.")
                return True
        except Exception as e:
            print(f"Login attempt failed: {e}")

        print("Retrying login in 15s...")
        time.sleep(15)


def get_repost_buttons(driver):
    repost_buttons = driver.eles('@data-automation=aUserActionsRepost')
    if not repost_buttons:
        print("No repost buttons found.")
        return []
    return repost_buttons


def repost_all():
    repost_buttons = get_repost_buttons(driver)
    for btn in repost_buttons:
        submitted = False
        while not submitted:
            repost_buttons2 = get_repost_buttons(driver)
            if not repost_buttons2:
                break
            btn2 = repost_buttons2[repost_buttons.index(btn)]
            try:
                btn2.click()
                print("Clicked a repost button.")
                time.sleep(1)
                driver.ele('@value=Submit', timeout=5).click()
                print("Submitted the repost.")
                time.sleep(1)
                submitted = True
            except:
                print("Reposting is on cooldown. Retrying in 30s...")
                time.sleep(30)
                driver.refresh()


def start_loop(cf_bypasser):
    while True:
        ensure_logged_in(cf_bypasser)

        try:
            try:
                driver.ele("#onetrust-accept-btn-handler").click()
                time.sleep(1)
            except:
                pass

            repost_all()

        except Exception as loop_err:
            print(f"Loop error: {loop_err}")

        delay = (15 * 60) #+ random.randint(0, 30) 
        print(f"Waiting {delay//60} min {delay%60} sec before next repost...")
        time.sleep(delay)


def cleanup_and_exit(sig, frame):
    global driver
    print("\nExit signal received. Closing browser...")
    try:
        if driver:
            driver.quit()
    except:
        pass
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, cleanup_and_exit)
    signal.signal(signal.SIGTERM, cleanup_and_exit)

    co = ChromiumOptions()
    co.auto_port(True)
    co.headless()  
    driver = ChromiumPage(co)
    cf_bypasser = CloudflareBypasser(driver)

    try:
        start_loop(cf_bypasser)
    except Exception as e:
        print(f"Fatal error: {e}")
        cleanup_and_exit(None, None)
