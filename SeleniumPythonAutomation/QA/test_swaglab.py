import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
@pytest.mark.usefixtures("driver")

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()

def test_login(driver):
    username = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")
    
    username.send_keys("standard_user")
    password.send_keys("secret_sauce")
    login_button.click()
    
    assert "inventory.html" in driver.current_url

def test_sorting(driver):
    sort_dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
    sort_dropdown.click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "product_sort_container")))
    
    sort_dropdown.send_keys(Keys.ARROW_DOWN)
    sort_dropdown.send_keys(Keys.RETURN)
    
    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_name")))

    products = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    assert len(products) > 0

def test_product_display(driver):
    products = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(products) > 0

def test_add_to_cart(driver):
    add_to_cart_buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")
    add_to_cart_buttons[0].click()
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert cart_badge.text == "1"

def test_checkout(driver):
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()
    checkout_button = driver.find_element(By.ID, "checkout")
    checkout_button.click()
    
    first_name = driver.find_element(By.ID, "first-name")
    last_name = driver.find_element(By.ID, "last-name")
    postal_code = driver.find_element(By.ID, "postal-code")
    
    first_name.send_keys("Test")
    last_name.send_keys("User")
    postal_code.send_keys("12345")
    
    continue_button = driver.find_element(By.ID, "continue")
    continue_button.click()
    
    finish_button = driver.find_element(By.ID, "finish")
    finish_button.click()
    
    assert "checkout-complete.html" in driver.current_url

def test_logout(driver):
    menu_button = driver.find_element(By.ID, "react-burger-menu-btn")
    menu_button.click()
    
    # Wait until the logout button is visible and clickable
    logout_link = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
    )
    
    logout_link.click()

    # Verify user is redirected to login page
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "login-button"))
    )

    assert "saucedemo.com" in driver.current_url


