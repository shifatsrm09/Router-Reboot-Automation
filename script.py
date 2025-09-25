import json
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Load router metadata ---
with open("meta-data.json", "r") as f:
    data = json.load(f)

router_name = "TP-Link_Archer_C7"   # the key in your JSON
router_data = data[router_name]      # now router_data points inside the router dict

driver_path = router_data["Driver"]["path"]
url = router_data["router_url"]
username = router_data["credentials"]["username"]
password = router_data["credentials"]["password"]


# --- Setup headless Firefox ---
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

service = Service(driver_path)
driver = webdriver.Firefox(service=service, options=options)
try:
    driver.get(url)
    print(f"Portal Accessed: {url}")

    # --- Enter password ---
    password_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, router_data["login"]["password_field"]))
    )
    password_box.send_keys(password)
    print("Parsing Data")

    # --- Click LOGIN ---
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, router_data["login"]["login_button"]))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
    driver.execute_script("arguments[0].click();", login_button)
    print("Logged in successfully.")

    # --- Click main REBOOT button ---
    reboot_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, router_data["reboot"]["main_button"]))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", reboot_button)
    driver.execute_script("arguments[0].click();", reboot_button)

    # --- Click confirmation popup ---
    confirm_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, router_data["reboot"]["confirm_button"]))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", confirm_button)
    driver.execute_script("arguments[0].click();", confirm_button)
    print("REBOOTING...")

    print("Reboot successful.")

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()

