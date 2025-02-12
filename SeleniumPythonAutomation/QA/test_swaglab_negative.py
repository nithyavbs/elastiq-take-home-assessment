import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

def wait_for_element(driver, by, value, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
    except TimeoutException:
        pytest.fail(f"Element {value} not found within {timeout} seconds")

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()

# Test login with invalid credentials
def test_invalid_login(driver):
    username = wait_for_element(driver, By.ID, "user-name")
    username.clear()
    username.send_keys("invalid_user")

    password = driver.find_element(By.ID, "password")
    password.clear()
    password.send_keys("wrong_password")

    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

    error_message = wait_for_element(driver, By.CLASS_NAME, "error-message-container")
    assert "Epic sadface" in error_message.text



# Test login with empty credentials
def test_empty_login(driver):
    username = wait_for_element(driver, By.ID, "user-name")
    username.clear()

    password = driver.find_element(By.ID, "password")
    password.clear()

    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

    error_message = wait_for_element(driver, By.CLASS_NAME, "error-message-container")
    assert "Epic sadface" in error_message.text

# Test checkout with missing details (Negative Case)
def test_checkout_missing_details(driver):
    # Ensure login fields exist before sending values
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name")))

    username = driver.find_element(By.ID, "user-name")
    username.clear()
    username.send_keys("standard_user")

    password = driver.find_element(By.ID, "password")
    password.clear()
    password.send_keys("secret_sauce")

    driver.find_element(By.ID, "login-button").click()

    # Ensure the inventory page loads before interacting
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
    )

    # Click on the cart icon only when it's clickable
    cart_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
    )
    cart_icon.click()

    # Ensure checkout button is visible before clicking
    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "checkout"))
    )
    checkout_button.click()

    # Click the continue button without entering details
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "continue"))
    )
    continue_button.click()

    # Check for the expected error message
    error_message = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "error-message-container"))
    )
    assert "Error" in error_message.text





# Test logout without opening menu (Edge Case)
def test_logout_without_menu(driver):
    try:
        # Check if menu is closed and open it
        menu_button = wait_for_element(driver, By.ID, "react-burger-menu-btn")
        menu_button.click()

        # Wait for logout button to appear
        logout_link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        
        logout_link.click()

        # Verify that we are back on the login page
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "login-button"))
        )
    except TimeoutException:
        pytest.fail("Logout button was not interactable, menu might not be open")
